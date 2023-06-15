FROM python:3.10-slim-buster

WORKDIR /app

RUN pip3 install starfyre

COPY . .

CMD ["./build.sh"]
