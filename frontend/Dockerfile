FROM node:16

WORKDIR /ogoFrontEnd

COPY ../package-lock.json .

COPY ../package.json .

COPY . .

RUN npm install

RUN npm run build

CMD ["npm", "run", "dev"]