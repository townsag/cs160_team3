FROM python:3.10.1

WORKDIR /ogo

RUN pip3 install flask flask_login

COPY . . 

CMD ["flask",  "--app",  "app.py",  "run", "-p", "3000"]