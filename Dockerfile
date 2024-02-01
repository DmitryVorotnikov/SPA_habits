FROM python:3

USER gitlab-runner

WORKDIR /spa_habits

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .
