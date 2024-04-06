# MySQL
---
## Install
### Amazon Linux 2023
```shell
sudo dnf install -y mariadb105
```
### Amazon Linux 2
``` shell
sudo yum install -y mariadb
```

<br>

---
## connect
```shell
# Export
ENDPOINT_URL="<DB_ENDPOINT>"
PORT="<PORT>" # Default Port Number : 3306
USER_NAME="<USER_NAME>"

# Connect
mysql -h $ENDPOINT_URL -P $PORT -u $USER_NAME -p
```

<br>

---
## DataBase Example
**Create DataBase**
```sql
CREATE DATBASE demo;
USE demo;
```

<br>

**Create Table**
```sql
CREATE TABLE user_table (
    user_id INT NOT NULL AUTO_INCREMENT,
    user_name VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    PRIMARY KEY(user_id)
);
```

<br>

**Add Data in Table**
```sql
INSERT INTO user_table(user_name, password) VALUES ('admin', 'Skil39!@#');
```

<br>

**Select Table**
```sql
SELECT * FROM user_table;
```

<br>

**Update Data in Table**
```sql
UPDATE user_table SET password = 'Skill53##' WEHETE user_name = 'admin';
```

<br>

**Delete Data in Table**
```sql
DELETE FROM user_table WHERE user_name = 'admin';
```