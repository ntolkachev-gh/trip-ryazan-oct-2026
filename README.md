# Рязань и окрестности · 23–31 октября 2026

Статический сайт для GitHub Pages: https://ntolkachev-gh.github.io/trip-ryazan-oct-2026/

## Как устроено
- `data.json` хранит все данные: дни (`days`), точки карты (`points`), цвета и легенду, HTML блоков билетов и обратных поездов, чек-лист, ссылки и подписи к фото.
- `build.py` генерирует из `data.json` все страницы: `index.html`, `tickets.html`, `plan.html`, `day/24.html … day/30.html`, `map.html`, `checklist.html`, `diary.html`.
- `assets/style.css`, `assets/app.js` — общие стили, меню, карты Leaflet, чек-лист в localStorage, анимации.
- `img/` — фото с Wikimedia Commons (авторы в подвале).

## Как обновить
1. Отредактировать `data.json`. Для дневника заполнить поле `diary` нужного дня (HTML, можно `<p>` и `<img src="img/...">`).
2. `python3 build.py`
3. `git commit -am "..." && git push`
