FROM node:16

WORKDIR /usr/src/app

RUN yarn global add nodemon

COPY ./frontend .

RUN npm install

RUN npm run build

CMD ["npm", "run", "dev"]