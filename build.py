#!/usr/bin/env python3
"""Генерирует все страницы сайта из data.json. Запуск: python3 build.py"""
import json,os
D=json.load(open('data.json',encoding='utf8'))
NAV=[('index.html','Главная'),('tickets.html','Билеты'),('plan.html','План'),('map.html','Карта'),('food.html','Еда'),('cuisine.html','Кухня'),('checklist.html','Чек-лист'),('diary.html','Дневник'),('guide.html','Путеводитель')]
WD={'2026-10-24':'Сб','2026-10-25':'Вс','2026-10-26':'Пн','2026-10-27':'Вт','2026-10-28':'Ср','2026-10-29':'Чт','2026-10-30':'Пт'}
W=json.load(open('weather.json')) if os.path.exists('weather.json') else {'days':{}}
WMO={0:('☀️','ясно'),1:('🌤','преимущественно ясно'),2:('⛅','переменная облачность'),3:('☁️','пасмурно'),45:('🌫','туман'),48:('🌫','изморозь, туман'),51:('🌦','слабая морось'),53:('🌦','морось'),55:('🌧','сильная морось'),56:('🌧','ледяная морось'),57:('🌧','ледяная морось'),61:('🌧','небольшой дождь'),63:('🌧','дождь'),65:('🌧','сильный дождь'),66:('🌧','ледяной дождь'),67:('🌧','ледяной дождь'),71:('🌨','небольшой снег'),73:('🌨','снег'),75:('❄️','сильный снег'),77:('🌨','снежная крупа'),80:('🌦','ливень'),81:('🌧','ливни'),82:('⛈','сильный ливень'),85:('🌨','снегопад'),86:('❄️','сильный снегопад'),95:('⛈','гроза'),96:('⛈','гроза с градом'),99:('⛈','гроза с градом')}
WUPD=f'Обновлено: {W.get("fetched_at","—")} МСК · <a href="https://open-meteo.com/">Open-Meteo</a>'
def wx(date): return W['days'].get(date)
def wchip(date):
    w=wx(date)
    if not w: return '<span class="chip wxc">🌡 прогноз позже</span>'
    return f'<span class="chip wxc">{WMO.get(w["weather_code"],("🌡",""))[0]} {round(w["temperature_2m_max"])}°/{round(w["temperature_2m_min"])}°</span>'
def hint(w):
    lo,hi=w['temperature_2m_min'],w['temperature_2m_max'];h=[]
    h.append('тёплая куртка, шапка и перчатки' if lo<3 else 'тёплая куртка' if hi<10 else 'лёгкая куртка или свитер')
    if (w['precipitation_probability_max'] or 0)>=40 or (w['precipitation_sum'] or 0)>=1: h.append('зонт и непромокаемая обувь')
    if w['wind_speed_10m_max']/3.6>=8: h.append('ветровка — ветрено')
    return ', '.join(h).capitalize()
def wcard(date):
    w=wx(date)
    if not w: return f'<div class="box wx rv"><b>🌡 Погода</b><p>Прогноз появится ближе к дате.</p><p class="wu">{WUPD}</p></div>'
    e,t=WMO.get(w['weather_code'],('🌡','—'))
    return (f'<div class="box wx rv"><div class="wi">{e}</div><div><b>Погода · {w["place"]}: {t}</b>'
      f'<p class="wt">{round(w["temperature_2m_min"])}…{round(w["temperature_2m_max"])} °C</p>'
      f'<p>☔ {w["precipitation_probability_max"]}% · {w["precipitation_sum"]} мм · 💨 до {w["wind_speed_10m_max"]/3.6:.0f} м/с · 🌅 {w["sunrise"][-5:]} · 🌇 {w["sunset"][-5:]}</p>'
      f'<p>👕 {hint(w)}</p><p class="wu">Прогноз, может измениться. {WUPD}</p></div></div>')
PA=D.get('photo_album')
PACARD=f'<a class="pa rv" href="{PA["url"]}" target="_blank" rel="noopener"><span class="pai">📷</span><span><b>{PA["title"][2:]}</b><br><small>{PA["sub"]}</small></span><span class="paa">→</span></a>' if PA else ''
PALINK=f'<p class="pal"><a href="{PA["url"]}" target="_blank" rel="noopener">📷 Все фото — в фотопотоке поездки →</a></p>' if PA else ''
def chips(c): return ''.join(f'<span class="chip{" t" if x.startswith("!") else ""}">{x.lstrip("!")}</span>' for x in c)
import hashlib as _h
CSSV=_h.md5(open("assets/style.css","rb").read()).hexdigest()[:8]
import glob as _g
from PIL import Image as _I
def gphotos(date):
    ds={date}|({'2026-10-23'} if date=='2026-10-24' else set())|({'2026-10-31'} if date=='2026-10-30' else set())
    out=[]
    for x in sorted(ds):
        for f in sorted(_g.glob(f'img/diary/{x}/*.jpg')):
            t=f'img/diary/{x}/t/'+os.path.basename(f)
            if not os.path.exists(t):
                os.makedirs(os.path.dirname(t),exist_ok=True);im=_I.open(f);im.thumbnail((600,600));im.save(t,'JPEG',quality=80)
            out.append((f,t))
    return out
def gal(d):
    P=gphotos(d['date'])
    if not P: return ''
    return f'<div class="gal rv">'+''.join(f'<a href="{f}" target="_blank" rel="noopener"><img src="{t}" alt="{d["title"]}" loading="lazy"></a>' for f,t in P)+'</div>'
def page(path,title,body,active,needmap=False):
    r='../'*path.count('/')
    nav=''.join(f'<a href="{r}{h}"{" class=on" if h==active else ""}>{t}</a>' for h,t in NAV)
    mp='<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"><script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>' if needmap else ''
    data=f'<script>window.TRIP={json.dumps(dict(points=D["points"],colors=D["colors"],food=FOODPTS),ensure_ascii=False)}</script>' if needmap else ''
    html=f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} · Рязань и Владимир, октябрь 2026</title><meta name="description" content="Рязань и Владимир: поездка 23–31 октября 2026 — Рязань, Константиново, Мещёра, Суздаль, Владимир"><meta property="og:title" content="{title} · Рязань и Владимир"><meta property="og:description" content="Поездка 23–31 октября 2026: Рязань, Константиново, Мещёра, Суздаль, Владимир"><link rel="icon" href="{r}favicon.svg"><link rel="apple-touch-icon" sizes="180x180" href="{r}apple-touch-icon.png?v=2"><link rel="icon" type="image/png" sizes="192x192" href="{r}icon-192.png"><link rel="manifest" href="{r}site.webmanifest"><meta name="apple-mobile-web-app-title" content="Рязань"><meta name="theme-color" content="#1f3d2b">
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,800;1,600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
{mp}<link rel="stylesheet" href="{r}assets/style.css?v={CSSV}"></head><body>
<nav><b>Рязань · Владимир ’26</b><button class="burger" aria-label="Меню">☰</button><div class="lnk">{nav}</div></nav>
{body.replace('img/',r+'img/').replace('href="day/','href="'+r+'day/')}
<footer><div class="wrap">Собрано в октябре 2026. Время везде московское.<br><br>Фото: Wikimedia Commons — {D["credits_html"]}</div></footer>
{data}<script src="{r}assets/app.js"></script></body></html>'''
    os.makedirs(os.path.dirname(path) or '.',exist_ok=True);open(path,'w',encoding='utf8').write(html)
def head(t,sub): return f'<header class="ptitle"><h1>{t}</h1><p>{sub}</p></header>'
days=D['days']
H=D['hotel']
FOODPTS=[dict(name=p['name'],addr=p['addr'],lat=p['lat'],lon=p['lon']) for g,L in D['food'] for p in L if p.get('lat')]+[dict(name=b['name'],addr=b['city']+', '+b['addr'],lat=b['lat'],lon=b['lon'],book=True) for b in D.get('book_spots',[])]+[dict(name=H['name']+' (жильё)',addr=H['addr'],lat=H['lat'],lon=H['lon'],hotel=True)]
HOTEL=f'''<section id="stay"><h2 class="rv">Жильё</h2><div class="box rv"><span class="badge b-o">Почти решено</span><h3 style="color:var(--g);font-size:24px;margin:8px 0 4px">🏨 {H['name']}</h3><p style="margin:0"><b>{H['addr']}</b> · {H['dates']}</p><p style="color:var(--mut)">{H['info']}</p><p><a href="tel:{H['phone'].replace(' ','')}">{H['phone']}</a> · <a href="{H['url']}">Островок</a></p></div></section>'''
def stt(d): return '<span class="st ok">✓ прошёл</span>' if d.get('status')=='done' else '<span class="st ok">✓ подтверждено</span>' if d.get('status')=='confirmed' else '<span class="st">план</span>'
def dlink(d): return f'day/{d["date"][-2:]}.html'
strip=''.join(f'<a class="sd rv" href="{dlink(d)}" style="background-image:url(img/{d["img"]}.jpg)"><span><b>{d["dt"]}</b>{d["title"]}<br>{stt(d)} {wchip(d["date"])}</span></a>' for d in days)
tiles=[('tickets.html','🎫','Билеты','Оба поезда куплены'),('plan.html','🗓️','План','Рязань, Солотча, три ночи в Суздале, Владимир'),('map.html','🗺️','Карта','Все точки, фильтр по дням'),('checklist.html','✅','Чек-лист','Сборы и полезные ссылки'),('diary.html','📔','Дневник','Заметки и фото из поездки')]
page('index.html','Главная',f'''<header class="hero"><div class="in"><div class="kick">Осеннее путешествие</div><h1>Рязань <i>и Владимир</i></h1><p>{D["dates"]}</p></div></header>
<div class="wrap"><div class="note rv">{D["note"]}</div>
<section><h2 class="rv">Коротко</h2><p class="sub rv">Ночным поездом в Рязань: кремль, есенинское Константиново и Солотча с Мещёрой. Затем ночным поездом во Владимир и три ночи в Суздале; последний день — Владимир и поезд домой 30→31 октября.</p>
<div class="grid">{''.join(f'<a class="tile rv" href="{h}"><div class="ic">{i}</div><h3>{t}</h3><p>{p}</p></a>' for h,i,t,p in tiles)}</div></section>
<section><h2 class="rv">7 дней</h2><p class="sub rv">Нажмите на день, чтобы открыть подробный план.</p><div class="strip">{strip}</div></section><section>{PACARD}</section></div>''','index.html')
page('tickets.html','Билеты',head('Билеты','Оба билета куплены.')+f'''<div class="wrap"><section>{D["ticket_html"].replace('href="#return"','href="#return"')}</section>{HOTEL}</div>''','tickets.html')
tl=''.join(f'<div class="day rv"><div class="dot">{d["n"]}</div><div class="ph" style="background-image:url(img/{d["img"]}.jpg)"></div><div class="bd"><div class="dt">{d["dt"]} {stt(d)}</div><h3>{d["title"]}</h3><div class="chips">{wchip(d["date"])}{chips(d["chips"])}</div><p style="margin:6px 0 0;font-size:15px">{d["items"][0] if d["n"]!=1 else d["items"][1]}</p><a class="more" href="{dlink(d)}">Подробнее о дне →</a></div></div>' for d in days)
bk=''.join(f'<div class="tile rv" style="cursor:default"><h3>{t}</h3><p style="color:var(--ink)">{a}</p><p style="margin-top:8px">{b}</p></div>' for t,a,b in D.get('backups',[]))
page('plan.html','План',head('План по дням','7 дней: Рязань и выезды, ночь в поезде до Владимира, три ночи в Суздале (27–29.10), 30.10 Владимир и поезд домой. Окский заповедник выпал. Учтены выходные музеев.')+f'<div class="wrap"><section><div class="tl">{tl}</div></section><section id="backup"><h2 class="rv">Запасные варианты</h2><p class="sub rv">Всё, что не вошло в основной план.</p><div class="grid">{bk}</div></section></div>','plan.html')
for i,d in enumerate(days):
    pv=f'<a href="{days[i-1]["date"][-2:]}.html">← {days[i-1]["dt"]}<br><b>{days[i-1]["title"]}</b></a>' if i else '<a href="../plan.html">← Весь план</a>'
    nx=f'<a class="nx" href="{days[i+1]["date"][-2:]}.html">{days[i+1]["dt"]} →<br><b>{days[i+1]["title"]}</b></a>' if i<len(days)-1 else '<a class="nx" href="../tickets.html">Билеты →</a>'
    diary=d.get('diary') or '<div class="diary">Здесь появятся заметки и фото из поездки</div>'
    page(f'day/{d["date"][-2:]}.html',d['dt']+' · '+d['title'],f'''<header class="phead" style="background-image:url(img/{d["img"]}.jpg)"><div class="in"><div class="kick">День {d["n"]} · {d["dt"]} · {"✓ прошёл" if d.get("status")=="done" else "✓ подтверждено" if d.get("status")=="confirmed" else "план"}</div><h1>{d["title"]}</h1></div></header>
<div class="wrap"><section>{wcard(d["date"])}<div class="chips rv">{chips(d["chips"])}</div><div class="box rv"><h2 style="font-size:26px">План</h2><ul>{''.join(f"<li>{x}</li>" for x in d["items"])}</ul></div></section>
<section><h2 class="rv" style="font-size:28px">Точки дня</h2><div class="mini rv" data-map="{d["n"]}"></div></section>
<section id="was"><h2 class="rv" style="font-size:28px">Как было</h2>{diary}{gal(d)}{PALINK}</section>
<div class="pn">{pv}{nx}</div></div>''','plan.html',True)
flt=''.join(f'<button class="on" data-d="{k}" style="--c:{D["colors"][k]}">{k} · {v}</button>' for k,v in D['legend'].items())+'<button class="on" data-d="food" style="--c:#c8641e">🍴 Еда и жильё</button>'
page('map.html','Карта',head('Карта','Цвет и номер метки — день поездки. Нажмите на день, чтобы скрыть или показать его точки.')+f'<div class="wrap"><section><div class="flt">{flt}</div><div id="bigmap" data-map="all"></div></section></div>','map.html',True)

def fcard(p):
    tag=' <span class="st">не подтверждено</span>' if p.get('unver') else ''
    lk=f' · <a href="{p["url"]}">ссылка</a>' if p.get('url') else ''
    dish=f'<p><b>Попробовать:</b> {p["dish"]}</p>' if p.get('dish') else ''
    q=''.join(f'<blockquote>{x}</blockquote>' for x in p.get('quotes',[]))
    ph=f'<figure class="fig"><img src="{p["photo"]}" alt="{p["name"]}" loading="lazy"><figcaption>{p["photo_cap"]}</figcaption></figure>' if p.get('photo') else f'<figure class="fig"><div class="ico">{p.get("icon","🍴")}</div></figure>'
    return f'<div class="fc rv"'+(f' id="{p["id"]}"' if p.get('id') else '')+f'>{ph}<div class="fb"><h3>{p["name"]}{tag}</h3><div class="rt">★ {p.get("rating","рейтинг не найден")}</div><p class="why">{p["why"]}</p>{dish}{q}<p class="meta">📍 {p["addr"]}{" (на карте примерно)" if p.get("approx") else ""}<br>🕒 {p["hours"]}<br>💳 {p["check"]}{lk}</p></div></div>'
FI=D.get('food_intro')
intro=(f'<section id="taste"><h2 class="rv" style="font-size:30px">Что попробовать: кухня Рязанщины и Владимирской земли</h2><p class="rv" style="max-width:760px">{FI["history"]}</p><div class="tgrid">'+''.join(f'<div class="tc rv"><div class="ti">{i}</div><div><h3>{t}</h3><p>{w}</p><p class="where">📍 {wh}</p>{f"<p class=wk>⚠ {n}</p>" if n else ""}</div></div>' for i,t,w,wh,n in FI['cards'])+f'</div><p class="src rv">{FI["sources"]}</p></section>') if FI else ''
BS=D.get('book_spots')
books=(f'<section id="books"><h2 class="rv" style="font-size:30px">Для книжного блога: атмосферные места для фото</h2><p class="rv" style="max-width:760px">Места, где хорошо снимать книги. Рейтинги в открытых источниках не нашли — не выдумываем. Точки на карте приблизительные (📚).</p><div class="fgrid">'+''.join(fcard(dict(b,name=b['name']+' · '+b['city'],dish='')) for b in BS)+'</div></section>') if BS else ''
teaser='<section><a class="tc rv" href="cuisine.html" style="text-decoration:none;color:inherit;max-width:760px"><div class="ti">🥧</div><div><h3>Что попробовать: кухня Рязанщины и Владимирской земли →</h3><p>Курник, калинник, медовуха, суздальские огурцы, сбитень — история и где попробовать.</p></div></a></section>' if FI else ''
fs=teaser+books+''.join(f'<section><h2 class="rv" style="font-size:30px">{g}</h2><div class="fgrid">{"".join(fcard(p) for p in L)}</div></section>' for g,L in D['food'])
page('food.html','Где поесть',head('Где поесть','Недорого и по-местному. ✓ — часы проверены по сайту или справочнику; перед походом уточняйте. Средний чек на одного.')+f'<div class="wrap">{fs}<section><h2 class="rv" style="font-size:28px">На карте</h2><div class="mini rv" data-map="food" style="height:380px"></div></section></div>','food.html',True)
cl=''.join(f'<label><input type="checkbox"><span>{x}</span></label>' for x in D['checklist'])
rd=''.join(f'<label><input type="checkbox"><span>{x}</span></label>' for x in D.get('reading',[]))
lk=''.join(f'<a href="{l["url"]}">{l["title"]}</a>' for l in D['links'])
page('checklist.html','Чек-лист',head('Чек-лист','Что посмотреть и почитать до поездки. Отметки сохраняются в этом браузере.')+f'<div class="wrap"><section><h2 class="rv">Посмотреть и почитать перед поездкой</h2><div class="cl rv">{rd}</div></section><section><h2 class="rv">Полезные ссылки</h2><div class="links rv">{lk}</div></section></div>','checklist.html')
dl=''.join(f'<a class="rv" href="{dlink(d)}#was"><div class="th" style="background-image:url(img/{d["img"]}.jpg)"></div><div><b>{d["dt"]} · {d["title"]}</b><br>{stt(d)} <small>{"Есть заметки" if d.get("diary") else "Пока пусто"}{(" · 📷 "+str(len(gphotos(d["date"])))+" фото") if gphotos(d["date"]) else ""}</small></div></a>'+(f'<div class="dg"><h3 class="rv">{d["dt"]} · {d["title"]}</h3>{gal(d)}</div>' if gphotos(d["date"]) else '') for d in days)
page('diary.html','Дневник',head('Дневник','Заполняется во время и после поездки.')+f'<div class="wrap"><section>{PACARD}</section><section><div class="dl">{dl}</div></section></div>','diary.html')
page('cuisine.html','Кухня',head('Кухня','Что попробовать на Рязанщине и во Владимирской земле.')+f'<div class="wrap">{intro}<section><a class="rv" href="food.html">← Где поесть</a></section></div>','cuisine.html')
G=D.get('guide')
if G:
    ul=lambda L:'<ul>'+''.join(f'<li>{x}</li>' for x in L)+'</ul>'
    def chap(c):
        ph=('<h3>Для фото / книжного блога</h3>'+ul(c['photo'])) if c['photo'] else ''
        return (f'<section class="gch" id="{c["id"]}"><figure class="fig rv"><img src="img/{c["img"]}.jpg" alt="{c["title"]}" loading="lazy"></figure>'
          f'<h2 class="rv">{c["title"]} <small>· {c["days"]}</small></h2><p class="rv">{c["intro"]}</p>'
          f'<h3>Что посмотреть</h3>{ul(c["see"])}<h3>Как добраться</h3><p>{c["how"]}</p><h3>Где поесть</h3>{ul(c["eat"])}{ph}'+
          (f'<div class="box rv" id="{c["id"]}-day"><h3>{c["daytitle"]}</h3>'+ul(c['daytips'])+'</div>' if c.get('daytips') else '')+f'<h3>Наши советы</h3>{ul(c["tips"])}<div class="op"><b>Наше мнение после поездки</b><div class="stars">☆☆☆☆☆</div><p>Допишем в поездке.</p></div></section>')
    toc='<a href="#intro">Вступление</a>'+''.join(f'<a href="#{c["id"]}">{c["title"]}</a>' for c in G['chapters'])+'<a href="#extra">Ещё день</a><a href="#practical">Практическое</a>'
    P=G['practical']
    pr=f'<section class="gch" id="practical"><h2 class="rv">Практическое</h2><h3>Поезда</h3>{ul(P["trains"])}<h3>Бюджет на сейчас</h3>{ul(P["budget"])}<h3>Что взять в конце октября</h3>{ul(P["pack"])}<h3>Приложения</h3>{ul(P["apps"])}</section>'
    gi=f'<section class="gch" id="intro"><p class="draft">✎ {G["draft"]}</p><h2 class="rv">Путеводитель от нас</h2><p>{G["intro"]}</p><h3>Маршрут</h3><p>{G["route"]}</p><h3>Сколько дней</h3><p>{G["days"]}</p><h3>Когда ехать</h3><p>{G["season"]}</p><h3>Фото</h3><p>В каждой главе есть блок «Для фото / книжного блога» с атмосферными местами (подробно — на странице <a href="food.html#books">«Еда»</a>).</p>{PALINK}</section>'
    ex=f'<section class="gch" id="extra"><h2 class="rv">Если есть ещё день</h2><p>{G["extra"]}</p></section>'
    page('guide.html','Путеводитель',head('Путеводитель','Рязань, Мещёра, Суздаль и Владимир: наш маршрут для друзей.')+f'<div class="wrap"><div class="gl"><aside class="toc">{toc}</aside><div>{gi}{"".join(chap(c) for c in G["chapters"])}{ex}{pr}</div></div></div>','guide.html')
print('ok')

