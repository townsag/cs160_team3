FROM node:16

WORKDIR /usr/src/app

RUN yarn global add nodemon

COPY ../package-lock.json .

COPY ../package.json .

COPY ./frontend/ . 

RUN npm install

RUN npm run build

CMD ["npm", "run", "dev"]