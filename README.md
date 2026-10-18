# Рязань и Владимир · 23–31 октября 2026

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

## Путеводитель (guide.html)
Данные — поле `guide` в data.json: `draft`, `intro`, `route`, `days`, `season`, `chapters[]` (id, title, img, days, intro, see[], how, eat[], photo[], tips[]), `extra`, `practical` (trains, budget, pack, apps). Ссылки на карточки: `food.html#<id>` (поле `id` у мест в `food` и `book_spots`). Блок «Наше мнение после поездки» пока заглушка — чтобы заполнить, добавьте в главу поля и выведите их в build.py. Затем `python3 build.py`.

## Погода
`./update_and_publish.sh` — одна команда раз в день: `update_weather.py` берёт прогноз Open-Meteo (без ключа) по точкам каждого дня → `weather.json` (fetched_at МСК, source), затем `build.py` и commit/push только при изменениях (`weather: <дата>`). Нужен `$GITHUB_TOKEN` в окружении (не печатается).
- Ошибка или дата за горизонтом прогноза → остаются прежние данные или надпись «прогноз появится ближе к дате».
- Прошедшие дни не перезаписываются; после 31.10.2026 файл заморожен целиком.
- Отображение: карточка на странице дня, чипы на главной и в плане. Коды WMO и подсказки по одежде — в build.py.
