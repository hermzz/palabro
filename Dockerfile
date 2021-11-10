FROM python:3.9

RUN apt-get update && apt-get install -y locales && sed -i '/es_ES.UTF-8/s/^# //g' /etc/locale.gen && locale-gen

COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app

WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["8080"]