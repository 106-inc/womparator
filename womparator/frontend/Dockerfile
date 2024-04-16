FROM node:18-slim

WORKDIR /usr/src/app

COPY ./package.json .
COPY ./package-lock.json .

# install application dependencies
RUN npm install --legacy-peer-deps

# copy app files
COPY . .

EXPOSE 3000

CMD [ "npm", "run", "start-watch" ]
