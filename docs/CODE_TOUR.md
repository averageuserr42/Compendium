# CODE_TOUR — разбор кода Compendium

Этот файл — не документация для проверяющего, а шпаргалка для тебя.
Здесь объяснено, что делает каждая часть кода и какими простыми немецкими фразами это сказать.

---

## 1. Как всё связано

```
data/trees.json  →  seed.py  →  data/compendium.db (SQLite)  →  app.py  →  /api/trees  →  index.html
```

И третий путь, отдельный от сайта (запускается вручную, когда добавились произведения):

```
data/trees.json  →  generate_covers.py  →  data/covers/*.svg  +  поля cover/wiki в data/trees.json
```

И второй путь, без сервера:

```
data/trees.json  →  index.html (fetch)
```

Первый путь работает локально, когда запущен `python app.py`.
Второй путь работает всегда — так живёт сайт на GitHub Pages, где Python запустить нельзя.

**Фраза:** „Die Daten liegen in einer JSON-Datei. Ein Skript schreibt sie in eine SQLite-Tabelle. Flask liest die Tabelle und liefert die Bäume als JSON an das Frontend."

---

## 2. seed.py (121 строка) — JSON в базу

Делает одну вещь: превращает `data/trees.json` в таблицу `nodes`.

| Что | Где в файле | Зачем |
|---|---|---|
| `SCHEMA` | сверху | SQL-запрос `CREATE TABLE nodes (...)`. Описывает колонки. |
| `insert_node()` | функция | Вставляет один узел и **вызывает себя** для детей. Это рекурсия. |
| `build_database()` | функция | Читает JSON, удаляет старую базу, создаёт новую, вставляет всё. |
| `if __name__ == "__main__"` | внизу | Запускается, когда ты пишешь `python seed.py`. |

Три места, которые стоит понимать:

1. `node.get("children", [])` — у книги нет `children`, поэтому берём пустой список. Цикл просто не выполнится.
2. `1 if node.get("isBook") else 0` — в SQLite нет логического типа, поэтому `true` превращается в `1`.
3. `db_path.unlink()` — база **каждый раз создаётся заново**. Это осознанно: источник правды — JSON. Из базы читает `app.py`, а новые записи приходят из формы (см. §3 ниже).

**Фразы:**
- „Das Seed-Skript wandelt die JSON-Datei in eine SQL-Tabelle um."
- „Die Funktion `insert_node` ruft sich selbst auf. So wird der ganze Baum eingefügt."

---

## 3. app.py (263 строки) — Flask

| Часть | Что делает |
|---|---|
| `get_connection()` | Открывает базу. `row_factory = sqlite3.Row` позволяет писать `row["title"]` вместо `row[3]`. |
| `build_node()` | Главная функция. Из строки таблицы делает узел для фронтенда — и детей через рекурсию. |
| `@app.route("/")` | Отдаёт `index.html`. |
| `@app.route("/api/trees")` | Отдаёт оба дерева как JSON. Это и есть API. |
| `@app.route("/api/works", methods=["POST"])` | Новое произведение: пишет в базу **и** в JSON. |
| `@app.route("/api/covers", methods=["POST"])` | Принимает картинку из формы, кладёт её в `data/covers/`. |
| `@app.route("/data/covers/<datei>")` | Отдаёт картинку браузеру (на Pages это делает сам хостинг). |
| `seed.missing_columns()` | При старте: если в базе не хватает колонок — база пересобирается сама. |
| `app.run(...)` | Запускает локальный сервер на `127.0.0.1:5000`. |

Логика `build_node` в двух шагах:

1. Если строка — книга (`is_book = 1`), то это лист: добавляем автора, ★, cross-media и возвращаем узел без детей.
2. Если это категория, то делаем SQL-запрос `WHERE parent_id = ?` — это дети — и вызываем `build_node` для каждого ребёнка.

Почему `ORDER BY rowid`: строки вставились в том же порядке, что и в JSON. `rowid` сохраняет этот порядок, поэтому карточки на сайте идут как раньше.

`finally: connection.close()` — соединение закрывается всегда, даже если была ошибка.

**Фразы:**
- „Die Tabelle hat sich selbst als Referenz: `parent_id` zeigt auf die übergeordnete Kategorie."
- „`parent_id = NULL` bedeutet: das ist eine Wurzel."
- „Der Baum entsteht nicht durch einen einzigen SQL-Befehl, sondern durch eine rekursive Funktion."

### Запись: `POST /api/works`

Это единственный путь, которым приложение меняет данные. Три шага:

1. Проверка входа: обязательны `parent_id`, `title`, `author`. Категория должна существовать и не быть книгой; ID не должна повторяться.
2. `INSERT` в таблицу `nodes`.
3. Тот же узел дописывается в `data/trees.json` (функции `find_node()` и `save_tree_data()`).

Зачем третий шаг, если база уже обновлена: база **создаётся заново** из `data/trees.json` командой `python seed.py`. Если писать только в базу, добавленное произведение исчезнет при следующей пересборке. Поэтому JSON — источник, а база — текущая копия. Если запись в JSON не удалась, сервер удаляет строку из базы и отвечает ошибкой 500: обе стороны остаются одинаковыми.

Коды ответов: **201** создано, **400** не хватает поля / неверный формат / родитель — книга, **404** категории нет, **409** такой ID уже есть, **413** картинка больше 3 МБ, **500** JSON недоступен для записи.

### Загрузка картинки: `POST /api/covers`

Форма отправляет файл как `multipart/form-data` (поле `file`, плюс `id` для имени файла). Разрешены `.jpg`, `.jpeg`, `.png`, `.webp`, лимит 3 МБ задаётся строкой `app.config["MAX_CONTENT_LENGTH"]`. Имя файла получается через `slugify()`: `Prüfwerk Eins` → `pruefwerk-eins.png`. Сервер возвращает путь вида `data/covers/pruefwerk-eins.png` — именно он уходит в поле `cover`.

**Фразы:**
- „Der Endpunkt `POST /api/works` schreibt an zwei Stellen: in die Tabelle und in die JSON-Datei."
- „Die JSON-Datei ist die Quelle, die Tabelle wird daraus erzeugt. Deshalb wird beides aktualisiert."
- „Wenn das Schreiben in die Datei fehlschlägt, wird die Datenbank zurückgerollt."
- „Bilder werden nach `data/covers/` gespeichert; die Karte bekommt nur den Pfad."

---

## 4. index.html — что изменилось

Раньше данные лежали в середине файла (около 200 строк). Теперь там две функции:

```javascript
async function loadTrees() { ... }   // пробует /api/trees, потом data/trees.json
async function start() { ... }       // грузит данные и рисует первый экран
```

`start()` вызывается один раз, в самом конце. Сначала данные, потом отрисовка — без данных рисовать нечего.

Порядок источников важен: сначала **API** (Flask), потом **файл**. Так один и тот же файл работает и локально с бэкендом, и на GitHub Pages без него.

В консоли браузера будет видно `404` на `/api/trees` — это ожидаемо на GitHub Pages, но выглядит как ошибка. Что сказать, если спросят:

> „Auf GitHub Pages gibt es kein Backend. Der 404 im Log ist der erste Versuch; die App fällt automatisch auf die JSON-Datei zurück."

Если оба источника недоступны, страница показывает текст `.status` вместо карточек — это не пустой белый экран.

Остальной код (`findPath`, `navigateTo`, `switchTree`, `countWorks`, `updateBreadcrumb`) не менялся.

### Карточка-постер (версия 0.9)

В `renderNode` появилась одна важная строка перед отрисовкой:

```javascript
const onlyBooks = node.children.length > 0 && node.children.every(child => child.isBook);
grid.classList.toggle('grid-books', onlyBooks);
```

Логика: если в текущей категории **только произведения**, сетка переключается на узкие колонки (`.grid-books`, ~185 px) — получается полка постеров. Категории остаются в широких колонках (300 px). Так одна и та же сетка служит обоим типам карточек.

Разметка карточки книги тоже изменилась:

| Блок | Что делает |
|---|---|
| `.cover-wrap` | Обёртка картинки с `position: relative` — на ней лежат бейдж и подпись. |
| `.cover-badge` | ★ как уголок картинки. Ставится **только** если обложка не SVG: в самом SVG звезда уже нарисована, иначе она была бы дважды. |
| `.cover-caption` | Подпись на картинке (титул + автор) для загруженных фото — у них нет собственной надписи. |
| `.cover-fallback` | Если произведения нет картинки — тёмная плоскость с названием и автором. |
| `.book-overlay` | Тёмная полоса снизу: описание (2 строки, `line-clamp`) + кнопки. |

Признак, по которому код отличает сгенерированную обложку от загруженной: `cover.endsWith('.svg')`. Это работает, потому что только генератор создаёт `.svg`-файлы, а форма принимает `.jpg/.png/.webp`.

---

## 5. Таблица `nodes`

| Колонка | Тип | Bedeutung |
|---|---|---|
| `id` | TEXT, PRIMARY KEY | ID des Knotens, weltweit eindeutig |
| `parent_id` | TEXT | ID der übergeordneten Kategorie, `NULL` = Wurzel |
| `tree` | TEXT | `literature` oder `novels` |
| `title` | TEXT | Titel oder Kategoriename |
| `description` | TEXT | Kurzbeschreibung |
| `is_book` | INTEGER | `1` = Buch (Blatt), `0` = Kategorie |
| `author` | TEXT | nur bei Büchern |
| `recommended` | INTEGER | `1` = ★ |
| `cover` | TEXT | Pfad zum Titelbild, z. B. `data/covers/1984.jpg` |
| `wiki` | TEXT | Link zum Wikipedia-Artikel |
| `related_id` | TEXT | Ziel des Cross-Media-Links |
| `related_title` | TEXT | Name des verknüpften Werks |

`cover` zeigt auf eine selbst erzeugte SVG-Datei, z. B. `data/covers/1984.svg` (siehe §7).

Проверить таблицу можно так: `python -c "import sqlite3; print(sqlite3.connect('data/compendium.db').execute('SELECT COUNT(*) FROM nodes').fetchone())"` — должно быть `(62,)`.

---

## 6. Запуск (три команды)

```bash
python -m pip install flask     # только один раз
python seed.py                  # JSON -> SQLite
python app.py                   # сервер на http://127.0.0.1:5000
python generate_covers.py       # только если добавились произведения: обложки и ссылки
```

`python seed.py` не обязателен: если базы нет, `app.py` создаёт её сам при старте.

**Сайт на GitHub Pages** после этого продолжает работать как раньше — ему база и Flask не нужны.

---

## 7. Обложки и ссылки: generate_covers.py (361 строка)

Этот скрипт не участвует в работе сайта. Он запускается вручную и делает две вещи: рисует обложки и проставляет ссылки на Википедию.

| Часть | Что делает |
|---|---|
| `WIKI_LINKS` | Словарь «id произведения → адрес статьи». Ссылка **хранится полем**, а не вычисляется из названия. |
| `walk_books()` | Рекурсивно обходит оба дерева и собирает произведения с их категорией. |
| `cover_svg()` | Собирает текст SVG-файла: фон, рамка, категория, название, автор, звёздочка, ветви. |
| `title_layout()` | Подбирает размер шрифта и переносит длинное название на строки, чтобы оно влезло в блок. |
| `branch()` | Рисует ветку и вызывает себя для ветвления — та же рекурсия, что и в `seed.py`. |
| `digest_of()` | `hashlib.sha256(...)` — отсюда берётся «разнообразие». Поэтому результат повторяем. |
| `main()` | Пишет 43 файла, заполняет `cover` и `wiki`, переписывает `data/trees.json`, пересобирает базу. |

Три вещи, которые стоит понимать:

1. **SVG — это текст.** Внутри обычные теги, как в HTML. Поэтому файл весит около 3 КБ и читается глазами.
2. **Детерминированность.** Никакого `random`: узор выбирается по хешу от id. Повторный запуск даёт те же файлы — проверено сравнением хешей.
3. **Мотив определяет категория, а не произведение.** `branch()` получает хеш категории, поэтому все книги одной категории выглядят как одна серия, а фон у каждой свой.

Отдельно и важно: ссылка на Википедию **не собирается из названия**. Проверка показала, почему: у книги «1984» статья `1984` в немецкой Википедии — про год, а не про роман Орвелла (а в одном запросе пришла фотография Индиры Ганди). Поэтому сорок ссылок хранятся в данных и были проверены поштучно.

**Фразы:**
- „Die Titelbilder sind selbst erzeugt: ein Skript schreibt SVG-Dateien. So gibt es keine Rechteprobleme und alle Karten sehen einheitlich aus."
- „Das Skript ist deterministisch — derselbe Titel ergibt immer dasselbe Bild."
- „Ein SVG ist eine Textdatei, deshalb ist jedes Bild nur etwa 3 KB groß."
- „Die Wikipedia-Links stehen als Feld in den Daten. Sie werden nicht aus dem Titel berechnet — sonst würde «1984» auf den Artikel über das Jahr 1984 zeigen."

---

## 8. Вероятные вопросы преподавателя

| Вопрос | Короткий ответ |
|---|---|
| Warum überhaupt eine Datenbank? | Damit die Daten getrennt vom Code liegen. Neue Werke brauchen keine Code-Änderung. |
| Warum SQLite und nicht MySQL? | SQLite ist in Python enthalten und braucht keinen Server. Für einen Prototyp reicht das. |
| Was ist `parent_id`? | Der Verweis auf die übergeordnete Kategorie. So liegt ein Baum in einer Tabelle. |
| Wie entsteht der Baum? | Die Funktion `build_node` liest die Kinder rekursiv aus der Tabelle. |
| Was passiert ohne Backend? | Das Frontend lädt `data/trees.json`. Die Demo funktioniert weiter. |
| Warum läuft Flask nicht auf GitHub Pages? | Pages ist nur statisches Hosting. Python braucht einen Server. |
| Was ist ein Endpunkt? | Eine URL, die Daten als JSON liefert. Hier: `/api/trees`. |
| Warum sind die Buchkarten schmal, die Kategorien aber breit? | Werke zeigen das Poster — dafür reicht schmale Spalte. Kategorien zeigen Text, dafür ist eine breite Karte lesbarer. |
| Warum steht der Titel nicht doppelt auf der Karte? | Er steht auf dem Titelbild. Die Karte wiederholt ihn nur, wenn das Bild keine Schrift trägt (Foto aus dem Formular). |
| Wo liegt die Datenbank im Repository? | Die `.db` ist in `.gitignore`. `seed.py` erzeugt sie aus `data/trees.json`. |
| Ist das schon produktionsreif? | Nein. `app.run()` ist der Entwicklungsserver. Für Produktion nimmt man z. B. Gunicorn. |
| Kann die App Daten schreiben? | Ja: `POST /api/works` legt ein Werk an — in der Datenbank und in `data/trees.json`. |
| Warum zwei Stellen? | Die JSON-Datei ist die Quelle, die Tabelle wird daraus erzeugt. Sonst wäre die Ergänzung nach dem nächsten `seed.py` weg. |
| Können Bilder hochgeladen werden? | Ja, `POST /api/covers` speichert sie in `data/covers/`. Erlaubt sind JPG, PNG und WEBP bis 3 MB. |
| Warum sieht der Lehrer das Formular nicht? | Die Live-Demo liegt auf GitHub Pages, dort läuft kein Python. Das Formular erscheint nur lokal, wenn `app.py` läuft. |
| Wie unterscheidet der Code generierte und hochgeladene Bilder? | Am Pfad: nur der Generator schreibt `.svg`-Dateien, das Formular nimmt JPG/PNG/WEBP. |
| Woher kommen die Titelbilder? | Aus einem eigenen Skript (`generate_covers.py`). Es schreibt typografische SVG-Dateien — rechtlich sauber und einheitlich. |
| Warum keine echten Buchcover? | Die deutsche Wikipedia zeigt keine Buchcover (dort sind nicht-freie Dateien nicht erlaubt), die englische nur unter „fair use". Für dieses Repository wäre das rechtlich nicht sauber. |
| Wie viele Werke haben einen Wikipedia-Link? | 40 von 43. Drei haben keinen Artikel in der deutschen oder englischen Wikipedia. |

---

## 9. Чего не говорить

- Формулировка про «база только читается» больше неверна: `POST /api/works` вставляет новые строки. Но правки и удаления из интерфейса нет — это честно сказать, если спросят.
- Про обложки больше не говори «их пока нет» — они есть, самодельные, в формате SVG. Если спросят про картинки из интернета, причина отказа — в документации, раздел 2.6, а не «не успел».
- Не говорить, что в проекте нет автоматических тестов, если спросят про качество — это честно и записано в разделе 8 документации.
- Про использование ИИ у тебя есть готовые формулировки в твоих заметках. Держись их.

---

*Stand: Version 0.8 (Titelbilder und Wikipedia-Links).*
