# MongoDB
---
### Install
### Amazon Linux 2023
```shell
echo "[mongodb-org-7.0]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/amazon/2023/mongodb-org/7.0/x86_64/
gpgcheck=1
enabled=1
gpgkey=https://www.mongodb.org/static/pgp/server-7.0.asc
" | sudo tee /etc/yum.repos.d/mongodb-org-7.0.repo
```
```shell
sudo yum install -y mongodb-mongosh-shared-openssl3
sudo yum install -y mongodb-org-7.0.2 mongodb-org-database-7.0.2 mongodb-org-server-7.0.2 mongodb-org-mongos-7.0.2 mongodb-org-tools-7.0.2
sudo systemctl enable --now mongod
```

<br>

```shell
# Export
ENDPOINT_URL="<DB_ENDPOINT>"
PORT="<PORT>" # Default Port Number : 27017
USER_NAME="<USER_NAME>"
USER_PASSWORD="<USER_PASSWORD>"

# Connect
# Instance Cluster
mongosh "mongodb://$USER_NAME:$USER_PASSWORD@$ENDPOINT_URL:$PORT/?tls=true&tlsCAFile=global-bundle.pem&retryWrites=false"

# Elastic Cluster
mongosh mongodb://$USER_NAME:$USER_PASSWORD@$ENDPOINT_URL:$PORT -tls --retryWrites=false
```

<br>

---
## DataBase Example
**Create DataBase**
``` bash
use demo
db.dropDatabase()
```

## Collection
``` bash
db.createCollection("user")

# maximum size 10MB, no more than 100 documents
db.createCollection("user", {capped: true, size: 10000000, max: 100})
```

<br>

**Add Data in Table**
``` bash
db.user.insertOne({
    user_name: "js", 
    password: 20
})

db.user.insertMany([
    {name: "js", age: 20}, 
    {name: "sm", age: 19},
    {name: "ys", age: 18}
])
```

<br>

**Select Table**
```bash
db.user.find({age: 20}, {name: true})  # (Query, Projection)
db.user.find({name: {$ne: "js"}})    # Not Equal

db.user.find({age: {$lt: 20}})  # less than
db.user.find({age: {$lte: 20}}) # less than or equal
db.user.find({age: {$gt: 20}})  # greater than
db.user.find({age: {$gte: 20}}) # greater than or equal

db.user.find({name: {$in: ["js", "sm"]}})  # in
db.user.find({name: {$nin: ["js", "sm", "ys"]}}) # not in

db.user.find({$and: [{name: true}, {age: {$lt: 20}}]})  # True & True -> True
db.user.find({$or: [{name: true}, {age: {$lte: 20}}]})  # True & False -> True
db.user.find({$nor: [{name: true}, {age: {$lte: 20}}]}) # False & False -> True
db.user.find({age: {$not: {$gte: 20}}}) # not

db.user.find().sort({age: 20})  # 1 -> ASC, -1 -> DESC
db.user.find().limit(5)
```

<br>

**Update Data in Table**
``` bash
# (Filter, Update)
db.usera.updateOne({name: "js"}, {$set: {name: true}})
db.user.updateMany({name: {$exists: false}}, {$set: {name: true}})
```

<br>

**Delete Data in Table**
``` bash
db.user.deleteOne({name: 'js'})
db.user.deleteMany({age: {$exists: false}})
```

<br>

**Select Index**
``` bash
db.user.createIndex({name: 1})
db.user.getIndexes()
db.user.dropIndex("name_1")
```

<br>

**Remove Data in Table**
```bash
db.user.remove({ });
```