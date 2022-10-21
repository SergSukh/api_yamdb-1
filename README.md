### Проект API социальной сети YaTube
- создание пользователей с подтверждением из электронной почты
- создание произведений, ревью, комментариев, оценка произведений(рейтинг)
- модели (Пользователь(абстрактный), произведение, ревью, комментарии, жанры, категории)

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/SergSukh/api_final_yatube.git
```

```
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```
python -m venv env
```

```
source venv/scripts/activate
```

```
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```
