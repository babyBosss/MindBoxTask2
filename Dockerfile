FROM alpine:3.10

RUN apk add --no-cache python3 py3-pip

COPY requirements.txt /usr/src/app/
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r /usr/src/app/requirements.txt

COPY main.py /usr/src/app/
COPY create_db.sql /usr/src/app/
COPY fill_db.sql /usr/src/app/
COPY database.sqlite /usr/src/app/
WORKDIR /usr/src/app/

EXPOSE 80

CMD ["python3", "/usr/src/app/main.py"]