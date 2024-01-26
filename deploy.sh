# Останавливаем и перезагружаем сервисы
sudo systemctl stop postgresql
sudo systemctl stop spa_habits
sudo systemctl restart nginx

# Добавляем права
sudo usermod -aG docker gitlab-runner
sudo chown -R gitlab-runner /home/gitlab-runner/
sudo chmod -R a+rwx /home/gitlab-runner/

# Останавливаем и перезагружаем сервисы
sudo systemctl restart nginx

# Перезапускаем Docker-Compose
docker-compose down
docker-compose build
docker-compose up -d

# Добавляем права заново
sudo usermod -aG docker gitlab-runner
sudo chown -R gitlab-runner /home/gitlab-runner/
sudo chmod -R a+rwx /home/gitlab-runner/

# Перезагружаем nginx
sudo systemctl restart nginx

#Собираем статику


# Добавляем права заново
sudo usermod -aG docker gitlab-runner
sudo chown -R gitlab-runner /home/gitlab-runner/
sudo chmod -R a+rwx /home/gitlab-runner/

# Перезагружаем nginx
sudo systemctl restart nginx