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
# Slave fails to catch up with error 1032
```bash
mysql> stop slave;
Query OK, 0 rows affected (0.00 sec)

mysql> SET GLOBAL SQL_SLAVE_SKIP_COUNTER=1;
Query OK, 0 rows affected (0.02 sec)

mysql> start slave;
Query OK, 0 rows affected (0.00 sec)

mysql> show slave status \G;

stop slave;
SET GLOBAL SQL_SLAVE_SKIP_COUNTER=1;
start slave;
show slave status \G;
```
#  Slave fails to catch up with error 1236
THis is means slave is trying to read a position which is out of the original binlog file

At slave end, I can see the error is:
```
the last event was read from './AUMELL131P-bin.009273' at 521805668, the last byte read was read from './AUMELL131P-bin.009273' at 521805824.
```

At Master end, I can see the last position of the binlog is 521805593:
```
[root@AUMELL131P /home/mysql]# mysqlbinlog ./AUMELL131P-bin.009273 |tail -15
ERROR: Error in Log_event::read_log_event(): 'read error', data_len: 199, event_type: 2
SET TIMESTAMP=1563044909/*!*/;
UPDATE phoenix_service_configs.Schedule SET LastRunDateTime = '2019-07-14 05:08:29', NextRunDateTime = '2019-07-14 05:09:00' WHERE ServiceConfigID = 1262
/*!*/;
# at 521805566
#190714  5:08:29 server id 10  end_log_pos 521805593    Xid = 95629009014
COMMIT/*!*/;
# at 521805593
#190714  5:08:29 server id 10  end_log_pos 521805668    Query   thread_id=1452128984    exec_time=0     error_code=0
SET TIMESTAMP=1563044909/*!*/;
BEGIN
/*!*/;
DELIMITER ;
# End of log file
ROLLBACK /* added by mysqlbinlog */;
/*!50003 SET COMPLETION_TYPE=@OLD_COMPLETION_TYPE*/;

```

So we can see that the slave is trying to read a non-exist position. To fix the issue, we just need to change the master to the next valid binlog

```bash
mysql> stop slave;
Query OK, 0 rows affected (0.00 sec)

mysql> change master to master_log_file='AUMELL131P-bin.009274' master_log_pos=1;
Query OK, 0 rows affected (0.02 sec)

mysql> start slave;
Query OK, 0 rows affected (0.00 sec)

mysql> show slave status \G;
```
