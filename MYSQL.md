# Show MySQL process list
```bash
SELECT user, time, state, info 
  FROM 
information_schema.processlist 
  WHERE command != 'Sleep' 
    AND 
    time >= 2 
    ORDER BY time DESC, id \G
```
# Slave fail to atch up with error 1032
```bash
mysql> stop slave;
Query OK, 0 rows affected (0.00 sec)

mysql> SET GLOBAL SQL_SLAVE_SKIP_COUNTER=1;
Query OK, 0 rows affected (0.02 sec)

mysql> start slave;
Query OK, 0 rows affected (0.00 sec)

mysql> show slave status \G;

```
