FROM node:16

WORKDIR /ogoFrontEnd

COPY . .

RUN npm install

RUN npm run build

CMD ["npm", "run", "dev"]