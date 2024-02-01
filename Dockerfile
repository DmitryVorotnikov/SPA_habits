FROM python:3

WORKDIR /spa_habits

COPY requirements.txt .

RUN pip install -r requirements.txt
RUN sudo usermod -aG docker gitlab-runner
RUN sudo chown -R gitlab-runner:gitlab-runner /home/gitlab-runner/
RUN sudo chmod -R a+rwx /home/gitlab-runner/
RUN sudo chmod -R 755 /home/gitlab-runner/

COPY . .
