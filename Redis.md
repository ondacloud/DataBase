# Redis
---
## Install
```shell
sudo yum -y install openssl-devel gcc
wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
cd redis-stable
make distclean
make redis-cli BUILD_TLS=yes
sudo install -m 755 src/redis-cli /usr/local/bin/
```
<br>

---
## Connect
```shell
# Export
ENDPOINT_URL="<DB_ENDPOINT>"
PORT="<PORT>" # Default Port Number : 6397

# Connect
redis-cli -h $ENDPOINT_URL -c -p $PORT
```