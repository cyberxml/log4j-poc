
# FROM tomcat:8.5.20-jre8
# docker run -d --name tomcat8 -p 4403:4403 -p 8000:8000 -p 8080:8080 -p 9876:9876 codenvy/ubuntu_jdk8
FROM codenvy/jdk8_maven3_tomcat8

# copy in the build targets
COPY --chown=user:user files /

USER user

WORKDIR /home/user

# build app
RUN cd /home/user/log4j-shell-poc/vulnerable-application && touch file.test
RUN cd /home/user/log4j-shell-poc/vulnerable-application && /home/user/maven3/bin/mvn compile
RUN cd /home/user/log4j-shell-poc/vulnerable-application && /home/user/maven3/bin/mvn package
RUN cp /home/user/log4j-shell-poc/vulnerable-application/target/log4shell-1.0-SNAPSHOT.war /home/user/tomcat8/webapps/log4shell.war 

# update tomcat from 8.0.20 to 8.5.3 for log4j2 
RUN cd /opt && \
    wget https://archive.apache.org/dist/tomcat/tomcat-8/v8.5.3/bin/apache-tomcat-8.5.3.tar.gz && \
    tar xvzf apache-tomcat-8.5.3.tar.gz && \
    cd apache-tomcat-8.5.3 && \
    cp -rp * /home/user/tomcat8 && \
    cd /home/user && \
    rm /opt/apache-tomcat-8.5.3.tar.gz && \
    rm -rf /opt/apache-tomcat-8.5.3 

RUN rm /home/user/tomcat8/conf/logging.properties

# replace customized tomcat
COPY --chown=user:user files /
     
EXPOSE 8080/tcp

CMD ["/entrypoint.sh"]
