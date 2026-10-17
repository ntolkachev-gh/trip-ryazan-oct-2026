#!/usr/bin/env python3
"""Генерирует все страницы сайта из data.json. Запуск: python3 build.py"""
import json,os
D=json.load(open('data.json',encoding='utf8'))
NAV=[('index.html','Главная'),('tickets.html','Билеты'),('plan.html','План'),('map.html','Карта'),('checklist.html','Чек-лист'),('diary.html','Дневник')]
WD={'2026-10-24':'Сб','2026-10-25':'Вс','2026-10-26':'Пн','2026-10-27':'Вт','2026-10-28':'Ср','2026-10-29':'Чт','2026-10-30':'Пт'}
def chips(c): return ''.join(f'<span class="chip{" t" if x.startswith("!") else ""}">{x.lstrip("!")}</span>' for x in c)
def page(path,title,body,active,needmap=False):
    r='../'*path.count('/')
    nav=''.join(f'<a href="{r}{h}"{" class=on" if h==active else ""}>{t}</a>' for h,t in NAV)
    mp='<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"><script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>' if needmap else ''
    data=f'<script>window.TRIP={json.dumps(dict(points=D["points"],colors=D["colors"]),ensure_ascii=False)}</script>' if needmap else ''
    html=f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} · Рязань, октябрь 2026</title><link rel="icon" href="{r}favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,800;1,600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
{mp}<link rel="stylesheet" href="{r}assets/style.css"></head><body>
<nav><b>Рязань ’26</b><button class="burger" aria-label="Меню">☰</button><div class="lnk">{nav}</div></nav>
{body.replace('img/',r+'img/').replace('href="day/','href="'+r+'day/')}
<footer><div class="wrap">Черновик собран 17.10.2026. Время везде московское.<br><br>Фото: Wikimedia Commons — {D["credits_html"]}</div></footer>
{data}<script src="{r}assets/app.js"></script></body></html>'''
    os.makedirs(os.path.dirname(path) or '.',exist_ok=True);open(path,'w',encoding='utf8').write(html)
def head(t,sub): return f'<header class="ptitle"><h1>{t}</h1><p>{sub}</p></header>'
days=D['days']
def stt(d): return '<span class="st ok">✓ подтверждено</span>' if d.get('status')=='confirmed' else '<span class="st">черновик</span>'
def dlink(d): return f'day/{d["date"][-2:]}.html'
strip=''.join(f'<a class="sd rv" href="{dlink(d)}" style="background-image:url(img/{d["img"]}.jpg)"><span><b>{d["dt"]}</b>{d["title"]}<br>{stt(d)}</span></a>' for d in days)
tiles=[('tickets.html','🎫','Билеты','Оба поезда куплены'),('plan.html','🗓️','План','7 дней по Рязани и окрестностям'),('map.html','🗺️','Карта','Все точки, фильтр по дням'),('checklist.html','✅','Чек-лист','Сборы и полезные ссылки'),('diary.html','📔','Дневник','Заметки и фото из поездки')]
page('index.html','Главная',f'''<header class="hero"><div class="in"><div class="kick">Осеннее путешествие · черновик</div><h1>Рязань <i>и окрестности</i></h1><p>{D["dates"]}</p></div></header>
<div class="wrap"><div class="note rv">{D["note"]}</div>
<section><h2 class="rv">Коротко</h2><p class="sub rv">Ночным поездом в Рязань, неделя по городу и области: кремль, Есенинское Константиново, Мещёра, Касимов, Окский заповедник с зубрами. В последний день Владимир, оттуда ночным поездом 30→31 октября в Петербург.</p>
<div class="grid">{''.join(f'<a class="tile rv" href="{h}"><div class="ic">{i}</div><h3>{t}</h3><p>{p}</p></a>' for h,i,t,p in tiles)}</div></section>
<section><h2 class="rv">7 дней</h2><p class="sub rv">Нажмите на день, чтобы открыть подробный план.</p><div class="strip">{strip}</div></section></div>''','index.html')
page('tickets.html','Билеты',head('Билеты','Оба билета куплены.')+f'''<div class="wrap"><section>{D["ticket_html"].replace('href="#return"','href="#return"')}</section></div>''','tickets.html')
tl=''.join(f'<div class="day rv"><div class="dot">{d["n"]}</div><div class="ph" style="background-image:url(img/{d["img"]}.jpg)"></div><div class="bd"><div class="dt">{d["dt"]} {stt(d)}</div><h3>{d["title"]}</h3><div class="chips">{chips(d["chips"])}</div><p style="margin:6px 0 0;font-size:15px">{d["items"][0] if d["n"]!=1 else d["items"][1]}</p><a class="more" href="{dlink(d)}">Подробнее о дне →</a></div></div>' for d in days)
page('plan.html','План',head('План по дням (черновик)','7 дней, база в Рязани рядом с центром или Рязанью-2, одна ночь в Касимове, ночь 29→30 в поезде до Владимира. Учтены выходные музеев.')+f'<div class="wrap"><section><div class="tl">{tl}</div></section></div>','plan.html')
for i,d in enumerate(days):
    pv=f'<a href="{days[i-1]["date"][-2:]}.html">← {days[i-1]["dt"]}<br><b>{days[i-1]["title"]}</b></a>' if i else '<a href="../plan.html">← Весь план</a>'
    nx=f'<a class="nx" href="{days[i+1]["date"][-2:]}.html">{days[i+1]["dt"]} →<br><b>{days[i+1]["title"]}</b></a>' if i<len(days)-1 else '<a class="nx" href="../tickets.html">Билеты →</a>'
    diary=d.get('diary') or '<div class="diary">Здесь появятся заметки и фото из поездки</div>'
    page(f'day/{d["date"][-2:]}.html',d['dt']+' · '+d['title'],f'''<header class="phead" style="background-image:url(img/{d["img"]}.jpg)"><div class="in"><div class="kick">День {d["n"]} · {d["dt"]} · {"✓ подтверждено" if d.get("status")=="confirmed" else "черновик"}</div><h1>{d["title"]}</h1></div></header>
<div class="wrap"><section><div class="chips rv">{chips(d["chips"])}</div><div class="box rv"><h2 style="font-size:26px">План</h2><ul>{''.join(f"<li>{x}</li>" for x in d["items"])}</ul></div></section>
<section><h2 class="rv" style="font-size:28px">Точки дня</h2><div class="mini rv" data-map="{d["n"]}"></div></section>
<section id="was"><h2 class="rv" style="font-size:28px">Как было</h2>{diary}</section>
<div class="pn">{pv}{nx}</div></div>''','plan.html',True)
flt=''.join(f'<button class="on" data-d="{k}" style="--c:{D["colors"][k]}">{k} · {v}</button>' for k,v in D['legend'].items())
page('map.html','Карта',head('Карта','Цвет и номер метки — день поездки. Нажмите на день, чтобы скрыть или показать его точки.')+f'<div class="wrap"><section><div class="flt">{flt}</div><div id="bigmap" data-map="all"></div></section></div>','map.html',True)
cl=''.join(f'<label><input type="checkbox"><span>{x}</span></label>' for x in D['checklist'])
rd=''.join(f'<label><input type="checkbox"><span>{x}</span></label>' for x in D.get('reading',[]))
lk=''.join(f'<a href="{l["url"]}">{l["title"]}</a>' for l in D['links'])
page('checklist.html','Чек-лист',head('Чек-лист','Отметки сохраняются в этом браузере.')+f'<div class="wrap"><section><div class="cl rv">{cl}</div></section><section><h2 class="rv">Посмотреть и почитать перед поездкой</h2><div class="cl rv">{rd}</div></section><section><h2 class="rv">Полезные ссылки</h2><div class="links rv">{lk}</div></section></div>','checklist.html')
dl=''.join(f'<a class="rv" href="{dlink(d)}#was"><div class="th" style="background-image:url(img/{d["img"]}.jpg)"></div><div><b>{d["dt"]} · {d["title"]}</b><br>{stt(d)} <small>{"Есть заметки" if d.get("diary") else "Пока пусто"}</small></div></a>' for d in days)
page('diary.html','Дневник',head('Дневник','Заполняется во время и после поездки.')+f'<div class="wrap"><section><div class="dl">{dl}</div></section></div>','diary.html')
print('ok')
