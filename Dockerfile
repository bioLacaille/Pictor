FROM fualan/pictor_base

MAINTAINER Alan "fualan1990@gmail.com"

# Docker环境
ENV DOCKER_ENV 1

# web app
RUN mkdir -p /deploy_web

WORKDIR /deploy_web

COPY pictor_backend /deploy_web/pictor_backend
COPY pictor_frontend/dist /deploy_web/pictor_frontend
COPY PictorData/avatar /deploy_web/PictorData/avatar
RUN rm -rf /deploy_web/pictor_backend/migrations

RUN python3 -m venv pictor_env && source pictor_env/bin/activate && pip3 install -r /deploy_web/pictor_backend/requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com

#RUN source pictor_env/bin/activate && cd /deploy_web/pictor_backend && python manage.py makemigrations pictor && python manage.py migrate && python manage.py create_default_user

COPY docker/conf/pictor.conf /etc/supervisor/conf.d/pictor.conf

COPY docker/conf/pictor_beat.conf /etc/supervisor/conf.d/pictor_beat.conf

COPY docker/conf/pictor_worker.conf /etc/supervisor/conf.d/pictor_worker.conf

COPY docker/conf/pictor_nginx.conf /etc/nginx/conf.d/pictor_nginx.conf






