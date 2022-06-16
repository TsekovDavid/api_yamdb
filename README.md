# Проект YaMDb - сервис отзывов на произведения

### Авторы:
- [Цеков Давид](https://github.com/TsekovDavid "Github page")
- [Позднышева Наталья](https://github.com/pozdnysheva "Github page")

### Технологии:
- Python
- Django
- DRF

### С помощью этого проекта можно:
* Читать отзывы на произведения различных категорий и жанров
* Добавлять, изменять и удалять собственные отзывы
* Оставлять комментарии к отзывам

#### Документация доступна после запуска сервера по адресу:
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

Создать миграции:

```
python manage.py makemigrations reviews
```

Выполнить миграции:

```
python3 manage.py migrate
```

Заполнить базу данных тестовой информацией:

```
python manage.py load_to_database
```

Запустить проект:

```
python3 manage.py runserver
```
