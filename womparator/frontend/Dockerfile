FROM node:18-slim

WORKDIR /usr/src/app

COPY ./package.json .
COPY ./yarn.lock .

# install application dependencies
RUN yarn install

# copy app files
COPY . .

EXPOSE 3000

CMD [ "yarn", "run", "start-watch" ]
