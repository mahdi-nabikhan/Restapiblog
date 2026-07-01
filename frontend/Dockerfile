FROM node:22

WORKDIR /app

COPY package*.json ./
RUN npm config list
RUN npm config set registry https://package-mirror.liara.ir/repository/npm/
RUN npm config get registry
RUN cat /root/.npmrc || true


RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "start"]