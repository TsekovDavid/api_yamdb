# Проект YaMDb - сервис отзывов на произведения

### Авторы:
- Цеков Давид - https://github.com/TsekovDavid
- Позднышева Наталья - https://github.com/pozdnysheva/

### Технологии:
- Python
- Django
- DRF

### С помощью этого проекта можно:
* Читать отзывы на произведения различных категорий и жанров
* Добавлять, изменять и удалять собственные отзывы
* Оставлять комментарии к отзывам

#### Документация по адресу:
```
http://localhost:8000/redoc/
```
### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/yandex-praktikum/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```
