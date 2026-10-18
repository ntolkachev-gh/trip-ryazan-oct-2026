#!/usr/bin/env python3
"""Fetch Open-Meteo daily forecast for each trip day -> weather.json.
Keeps last good data on failure; past dates are kept (not overwritten); freezes entirely after 31.10.2026."""
import json, os, urllib.request, datetime as dt
MSK = dt.timezone(dt.timedelta(hours=3))
LOC = {'2026-10-23':('Санкт-Петербург',59.94,30.31),'2026-10-24':('Рязань',54.63,39.74),'2026-10-25':('Константиново',54.83,39.57),
 '2026-10-26':('Солотча',54.79,39.83),'2026-10-27':('Брыкин Бор',54.75,40.84),'2026-10-28':('Суздаль',56.42,40.45),
 '2026-10-29':('Суздаль',56.42,40.45),'2026-10-30':('Владимир',56.13,40.41)}
F = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'weather.json')
DAILY = 'weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,precipitation_sum,wind_speed_10m_max,sunrise,sunset'
now = dt.datetime.now(MSK); today = now.date().isoformat()
old = json.load(open(F)) if os.path.exists(F) else {'days': {}}
if today > '2026-10-31' and old.get('days'):
    print('trip over: weather.json frozen'); raise SystemExit(0)
days = dict(old.get('days', {})); changed = False
for date, (place, lat, lon) in LOC.items():
    if date < today and date in days: continue  # keep last forecast for past days
    url = (f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily={DAILY}'
           f'&timezone=Europe/Moscow&start_date={date}&end_date={date}')
    try:
        r = json.load(urllib.request.urlopen(url, timeout=20))['daily']
        if r['temperature_2m_max'][0] is None: raise ValueError('no data')
        days[date] = dict(place=place, **{k: r[k][0] for k in DAILY.split(',')}); changed = True
    except Exception as e:
        print(date, 'not updated:', e)
if changed:
    json.dump(dict(fetched_at=now.strftime('%d.%m.%Y %H:%M'), source='Open-Meteo', days=days), open(F, 'w'), ensure_ascii=False, indent=1)
print('ok', len(days), 'days')
