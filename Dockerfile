FROM python:3.10.1

WORKDIR /base

COPY requirements.txt .

RUN pip3 install -r requirements.txt

RUN apt-get update --fix-missing && \
    apt-get install -y nodejs npm && \
    rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash -
RUN apt-get install -y nodejs

COPY . .

EXPOSE 3000
# EXPOSE 8000

WORKDIR /base/ogo 
RUN npm install
RUN npm run build
WORKDIR /base

CMD ["flask",  "--app",  "app.py", "run", "--host=0.0.0.0", "-p", "3000"]