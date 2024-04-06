# PostgreSQL
---
## Install
### Amazon Linux 2023
```shell
sudo dnf install -y postgresql15
```
### Amazon Linux 2
``` shell
sudo amazon-linux-extras install -y postgresql14
```

<br>

---
## connect
```shell
# Export
ENDPOINT_URL="<DB_ENDPOINT>"
PORT="<PORT>" # Default Port Number : 5432
USER_NAME="<USER_NAME>"
DB_NAME="<DB_NAME>"

# Connect
psql --host=$ENDPOINT_URL --port=$PORT --username=$USER_NAME --password --dbname=$DB_NAME
```

<br>

---
## DataBase Example
**Create DataBase**
```sql
CREATE DATABASE demo with owner postgres;
\l+
\c demo;
```

<br>

**Create Schema**
```sql
CREATE SCHEMA wsi authorization postgres;
set search_path to wsi;
\dn+
```

<br>

**Create Table**
```sql
CREATE TABLE public.user_table (
    user_id INT NOT NULL AUTO_INCREMENT,
    user_name VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    PRIMARY KEY(user_id)
);
\dt
```

<br>

**Add Data in Table**
```sql
INSERT INTO public.user_table(user_name, password) VALUES ('admin', 'Skil39!@#');
```

<br>

**Select Table**
```sql
SELECT * FROM public.user_table;
```

<br>

**Update Data in Table**
```sql
UPDATE public.user_table SET password = 'Skill53##' WEHETE user_name = 'admin';
```

<br>

**Delete Data in Table**
```sql
DELETE FROM public.user_table WHERE user_name = 'admin';
```