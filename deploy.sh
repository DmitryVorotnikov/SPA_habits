# Перезапускаем Docker-Compose
docker-compose down
docker-compose build
docker-compose up -d

#Собираем статику
#sudo docker-compose exec web_api python manage.py collectstatic --noinput
