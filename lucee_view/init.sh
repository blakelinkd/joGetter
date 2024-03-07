#!/bin/bash

# Start Lucee server
/usr/local/tomcat/bin/catalina.sh run &
cd /var/www/
npm i
npm run start-bs