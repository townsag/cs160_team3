FROM python:3.10.1

WORKDIR /ogo

COPY . . 

RUN pip3 install -r requirements.txt


CMD ["flask",  "--app",  "app.py",  "run", "-p", "3000"]