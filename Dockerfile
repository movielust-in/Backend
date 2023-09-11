FROM node:18

RUN apt-get update || : && apt-get install python3 python3-pip -y

WORKDIR /usr/src/app

COPY flask/requirements.txt ./

RUN pip install --break-system-packages -r requirements.txt

COPY node/package*.json ./

RUN npm ci --omit=dev

COPY . .

RUN chmod +x wrapper.sh

CMD ./wrapper.sh
