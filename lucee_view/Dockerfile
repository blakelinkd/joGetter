FROM lucee/lucee:latest
# Install Maven
RUN apt-get update && apt-get install -y maven npm

# copy database over, this is a hard link to ../job_data.db
COPY job_data.db /opt/lucee/web

# Copy lucee password file
COPY password.txt /opt/lucee/server/lucee-server/context
# copy the datasource over
# COPY datasource.xml /opt/lucee/web/lucee-server/context

COPY init.sh /usr/local/bin/init.sh
# Set the script as executable
RUN chmod +x /usr/local/bin/init.sh
# Set the entry point to the initialization script

# Create a directory for the SQLite JDBC driver
WORKDIR /opt/lucee/server/lucee-server/bundles

# Download the SQLite JDBC driver using Maven
RUN mvn dependency:get -Dartifact=org.xerial:sqlite-jdbc:3.34.0:jar -Ddest=sqlite-jdbc-3.34.0.jar

# Copy the SQLite JDBC driver to /usr/local/tomcat/lib
RUN cp sqlite-jdbc-3.34.0.jar /usr/local/tomcat/lib/

# Download slf4j-api using Maven
RUN mvn dependency:get -Dartifact=org.slf4j:slf4j-api:1.7.36:jar -Ddest=slf4j-api-1.7.36.jar

# Copy slf4j-api to /usr/local/tomcat/lib
RUN cp slf4j-api-1.7.36.jar /usr/local/tomcat/lib/



COPY lucee-web.xml.cfm /opt/lucee/web/lucee-web.xml.cfm
ENTRYPOINT ["/usr/local/bin/init.sh"]

