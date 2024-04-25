FROM node:18-slim

WORKDIR /frontend

COPY ./package.json .
COPY ./yarn.lock .

# install application dependencies
RUN yarn install

# copy app files
COPY . .

CMD [ "yarn", "run", "start-watch" ]
