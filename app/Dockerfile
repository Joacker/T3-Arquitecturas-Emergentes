FROM python:3.8.5-alpine
COPY . /app
WORKDIR /app
RUN apk add gcc musl-dev python3-dev libffi-dev openssl-dev
RUN apk add --no-cache sqlite~=3.32.1-r1
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install -U flask-cors
ENTRYPOINT ["python"]
EXPOSE 5000
CMD ["-u","rest.py"]