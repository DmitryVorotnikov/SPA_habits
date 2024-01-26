# Останавливаем и перезагружаем сервисы
sudo systemctl stop postgresql
sudo systemctl stop spa_habits
sudo systemctl restart nginx

# Добавляем права
sudo usermod -aG docker gitlab-runner
sudo chown -R gitlab-runner /home/gitlab-runner/
sudo chmod -R a+rwx /home/gitlab-runner/

# Перезапускаем Docker-Compose
docker-compose down
docker-compose build
docker-compose up -d

# Добавляем права заново
sudo usermod -aG docker gitlab-runner
sudo chown -R gitlab-runner /home/gitlab-runner/
sudo chmod -R a+rwx /home/gitlab-runner/

#Собираем статику
docker-compose exec web_api python manage.py collectstatic --noinput

# Добавляем права заново
sudo usermod -aG docker gitlab-runner
sudo chown -R gitlab-runner /home/gitlab-runner/
sudo chmod -R a+rwx /home/gitlab-runner/