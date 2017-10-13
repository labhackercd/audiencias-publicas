FROM labhackercd/alpine-python3-nodejs

ENV BUILD_PACKAGES postgresql-dev postgresql-client gettext

RUN apk add --update --no-cache $BUILD_PACKAGES
RUN mkdir -p /var/labhacker/audiencias

ADD . /var/labhacker/audiencias
WORKDIR /var/labhacker/audiencias

RUN pip3 install -r requirements.txt psycopg2 gunicorn && \
    rm -r /root/.cache

RUN npm install

RUN python3 manage.py bower_install --allow-root && \
    python3 manage.py collectstatic --no-input && \
    python3 manage.py compilemessages

RUN npm rebuild node-sass --force

EXPOSE 8000