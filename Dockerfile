FROM node:18

RUN apt-get update || : && apt-get install python3 python3-pip -y

WORKDIR /usr/src/app

COPY flask/requirements.txt ./

RUN pip install --break-system-packages -r requirements.txt

COPY node/package*.json ./

RUN npm ci --omit=dev

COPY . .

ENV PORT 8000
ENV DATABASE_URL mongodb://127.0.0.1:27017/moviebase
ENV FLASK_DEBUG production
ENV SECRET 3f0ca94aeb057399b9193787790b5bf0
ENV TMDB_KEY 2a7d4498c790ee971ae3369d0327d57c
ENV MAIL_SERVER smtp.zoho.in
ENV MAIL_EMAIL anuragparmar@zohomail.in
ENV MAIL_PASSWORD y8adJjbtWNUT
ENV MAIL_PORT 465
ENV MAIL_USE_SSL True
ENV MAIL_USE_TLS False
ENV ADMIN_SECRET 3f0ca94bea052711b9193787790b5bf0

RUN chmod +x wrapper.sh

CMD ./wrapper.sh
