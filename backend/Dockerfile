FROM python:3.10.1

WORKDIR /usr/src/app

COPY . . 

RUN pip3 install -r requirements.txt

CMD ["flask",  "--app",  "app.py", "--debug", "run", "-p", "3000"]