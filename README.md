# api_yamdb
Как развернуть проект: 
1. Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

```
source venv/Scripts/activate
```

2. Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

3. Выполнить миграции:

```
cd api_yamdb
```

```
python manage.py migrate
```

4. Запустить проект:

```
python manage.py runserver
```
