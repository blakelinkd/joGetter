FROM lucee/lucee:5.3.9.133-tomcat9.0-jdk11-openjdk

RUN sed -i 's/htt[p|ps]:\/\/archive.ubuntu.com\/ubuntu\//mirror:\/\/mirrors.ubuntu.com\/mirrors.txt/g' /etc/apt/sources.list


# Install Maven
RUN apt-get update && apt-get install -y maven npm

# copy database over, this is a hard link to ../job_data.db
COPY job_data.db /opt/lucee/web

# Copy lucee password file
COPY password.txt /opt/lucee/server/lucee-server/context
# copy the datasource over
# COPY datasource.xml /opt/lucee/web/lucee-server/context

COPY init.sh /usr/local/bin/
# Set the script as executable
RUN chmod +x /usr/local/bin/init.sh
# Set the entry point to the initialization script

# Create a directory for the SQLite JDBC driver
WORKDIR /opt/lucee/server/lucee-server/bundles

# Copy the SQLite JDBC driver to /usr/local/tomcat/lib
COPY sqlite-jdbc-3.34.0.jar /usr/local/tomcat/lib/

# Copy slf4j-api to /usr/local/tomcat/lib
COPY slf4j-api-1.7.36.jar /usr/local/tomcat/lib/

COPY Application.cfc /var/www
ENTRYPOINT ["/usr/local/bin/init.sh"]

