#!/bin/bash

# Start Lucee server
/usr/local/tomcat/bin/catalina.sh run &&
cd /var/www/jobs
useradd -m -d /home/appuser -s /bin/bash appuser

npm i
npm run start-bs