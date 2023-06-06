FROM python:3.8-alpine

ENV PYTHONUNBUFFERED 1
ENV DEBUG=True
ENV ALLOWED_HOSTS=*
ENV SECRET_KEY=sample_scret_key
ENV PAPER_TRAIL_ADDRESS=sample.com
ENV PAPER_TRAIL_PORT=1234
ENV DB_HOST=emote_api_db
ENV DB_NAME=app
ENV DB_USER=postgres
ENV DB_PASS=supersecretpassword
ENV DB_PORT=5432
ENV IMAGE_PATH=uploads/images/
ENV REDIS_NETWORK=emote_api_redis
ENV REDIS_PORT=6379

WORKDIR /emote_api

COPY requirements.txt /emote_api

COPY ./scripts/ /scripts/

RUN chmod +x /scripts/*

RUN apk update

RUN pip install --upgrade pip

RUN apk add --update --no-cache postgresql-client jpeg-dev

RUN apk add --update --no-cache --virtual .tmp-build-deps \
      gcc libc-dev libffi-dev linux-headers postgresql-dev musl-dev \
      zlib zlib-dev openssl-dev rust 

RUN apk add --update \
  build-base \
  cairo \
  cairo-dev \
  cargo \
  freetype-dev \
  gcc \
  gdk-pixbuf-dev \
  gettext \
  jpeg-dev \
  lcms2-dev \
  libffi-dev \
  musl-dev \
  openjpeg-dev \
  openssl-dev \
  pango-dev \
  poppler-utils \
  postgresql-client \
  postgresql-dev \
  py-cffi \
  python3-dev \
  rust \
  tcl-dev \
  tiff-dev \
  tk-dev \
  zlib-dev \
  linux-headers

RUN pip install cryptography

RUN pip install -r requirements.txt

RUN apk del .tmp-build-deps

COPY ./app /emote_api

RUN adduser --disabled-password --no-create-home emote_api && \
    mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \
    chown -R emote_api:emote_api /vol && \
    chmod -R 755 /vol

RUN chmod -R 777 /vol/web


ENV PATH="/scripts:/py/bin:$PATH"

RUN python manage.py collectstatic --noinput

CMD ["run.sh"]

EXPOSE 8000

CMD python manage.py runserver 0.0.0.0:$PORT
