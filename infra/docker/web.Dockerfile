FROM node:20-alpine

WORKDIR /workspace

COPY package.json /workspace/package.json
COPY apps/web /workspace/apps/web
COPY packages /workspace/packages

RUN npm install && npm run build:web

WORKDIR /workspace/apps/web

EXPOSE 3000

CMD ["npm", "run", "start"]

