#!/bin/bash

gunicorn -b ":5000" --chdir /usr/src/app/flask app:app &

node /usr/src/app/node/src/server.js &

wait -n

# Exit with status of process that exited first
exit $?