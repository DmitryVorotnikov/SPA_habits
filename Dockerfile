FROM python:3

WORKDIR /spa_habits

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN python manage.py collectstatic --noinput

COPY . .
