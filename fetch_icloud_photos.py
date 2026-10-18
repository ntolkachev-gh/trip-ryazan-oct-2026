#!/usr/bin/env python3
"""Download new photos from the public iCloud shared album into img/diary/<YYYY-MM-DD>/ (does NOT publish).
New-style albums (photos.icloud.com/shared/album/<id>) are CloudKit-based; the old sharedstreams webstream API returns 404 for them.
Flow: public/records/resolve -> anonymous public token + partition -> shared/records/query CPLAssetAndMasterByAddedDate.
Images: resJPEGMed (or original) -> max 1600px JPEG, all EXIF (incl. GPS) stripped. Tokens are never printed."""
import json, os, io, sys, urllib.request, datetime as dt
from PIL import Image, ImageOps
ALBUM = '03bWMPXnr0KrpCv4BcEtFH9nA'
ROOT = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(ROOT, 'img', 'diary')
SEEN = os.path.join(OUT, '.icloud_seen.json')
H = {'Content-Type': 'text/plain;charset=UTF-8', 'Origin': 'https://photos.icloud.com', 'Referer': 'https://photos.icloud.com/', 'User-Agent': 'Mozilla/5.0'}
DB = 'database/1/com.apple.photos.cloud/production'
def post(url, body):
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=H, method='POST')
    return json.load(urllib.request.urlopen(req, timeout=30))
def main(dry=False):
    r = post(f'https://ckdatabasews.icloud.com/{DB}/public/records/resolve?remapEnums=true&sharing_url_key={ALBUM}', {'shortGUIDs': [{'value': ALBUM}]})['results'][0]
    acc, zone = r['anonymousPublicAccess'], r['zoneID']
    q = f"{acc['databasePartition']}/{DB}/shared/records/query?remapEnums=true&sharing_url_key={ALBUM}&publicAccessAuthToken={urllib.parse.quote(acc['token'])}"
    cnt = post(q, {'query': {'recordType': 'HyperionIndexCountLookup', 'filterBy': [{'fieldName': 'indexCountID', 'comparator': 'IN', 'fieldValue': {'value': ['CPLAssetByAddedDate'], 'type': 'STRING_LIST'}}]}, 'zoneID': zone})
    total = cnt['records'][0]['fields']['itemCount']['value']; print('photos in album:', total)
    seen = set(json.load(open(SEEN))) if os.path.exists(SEEN) else set(); rank, new = 0, 0
    while rank < total:
        recs = post(q, {'query': {'recordType': 'CPLAssetAndMasterByAddedDate', 'filterBy': [
            {'fieldName': 'direction', 'comparator': 'EQUALS', 'fieldValue': {'value': 'ASCENDING', 'type': 'STRING'}},
            {'fieldName': 'startRank', 'comparator': 'EQUALS', 'fieldValue': {'value': rank, 'type': 'INT64'}}]}, 'zoneID': zone, 'resultsLimit': 200})['records']
        masters = {x['recordName']: x for x in recs if x['recordType'] == 'CPLMaster'}
        assets = [x for x in recs if x['recordType'] == 'CPLAsset']
        if not assets: break
        for a in assets:
            rank += 1; f = a['fields']; m = masters.get(f['masterRef']['value']['recordName'])
            if not m or a['recordName'] in seen: continue
            mf = m['fields']
            if mf.get('itemType', {}).get('value', '').startswith(('com.apple.quicktime', 'public.mpeg')): continue  # skip videos
            res = mf.get('resJPEGMedRes') or mf.get('resOriginalRes')
            ts = (f['assetDate']['value'] / 1000) + f.get('timeZoneOffset', {}).get('value', 10800)
            day = dt.datetime.fromtimestamp(ts, dt.timezone.utc).strftime('%Y-%m-%d')
            if dry: print('would save', day); continue
            raw = urllib.request.urlopen(res['value']['downloadURL'].replace('${f}', 'photo.jpg'), timeout=60).read()
            im = ImageOps.exif_transpose(Image.open(io.BytesIO(raw))).convert('RGB'); im.thumbnail((1600, 1600))
            os.makedirs(os.path.join(OUT, day), exist_ok=True)
            p = os.path.join(OUT, day, f"{dt.datetime.fromtimestamp(ts, dt.timezone.utc).strftime('%H%M%S')}_{a['recordName'][:8]}.jpg")
            im.save(p, 'JPEG', quality=85)  # saved without EXIF -> no GPS
            seen.add(a['recordName']); new += 1; print('saved', os.path.relpath(p, ROOT))
    if not dry:
        os.makedirs(OUT, exist_ok=True); json.dump(sorted(seen), open(SEEN, 'w'))
    print('new:', new)
if __name__ == '__main__': main('--dry' in sys.argv)
