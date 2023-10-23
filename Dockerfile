FROM python:3.11-alpine

WORKDIR /app

RUN apk update && apk add nodejs npm

COPY . /app

WORKDIR /app/ogo

RUN npm install

RUN npm run build

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]