# Table of Contents
- [Purge binlog](MYSQL.md#purge-binlog)
- [Show MySQL process list](MYSQL.md#show-mysql-process-list)
- [Show mysql processlist](MYSQL.md#show-mysql-process-list)
- [Slave fails to catch up with error 1032](MYSQL.md#slave-fails-to-catch-up-with-error-1032)
- [Slave fails to catch up with error 1236](MYSQL.md#slave-fails-to-catch-up-with-error-1236)
- [Slave fails to catch up with error ha_err_key_not_found](MYSQL.md#slave-fails-to-catch-up-with-error-1032-handler-error-ha_err_key_not_found)
- [Mysql export selected data to txt file](MYSQL.md#mysql-export-selected-data-to-txt-file)
- [Mysql load rows from txt file into table](MYSQL.md#mysql-load-rows-from-txt-file-into-table)
- [Copy Mysql Slave LXD snapshot and make it as a new Mysql Slave](MYSQL.md#copy-mysql-slave-lxd-snapshot-and-make-it-as-a-new-mysql-slave)

# Purge binlog
```
mysql> PURGE BINARY LOGS TO 'mysql-bin.000010';
mysql> PURGE BINARY LOGS BEFORE '2008-04-02 22:46:26';
mysql> set global expire_logs_days=3;
```

Add to my.cnf
expire-logs-days = 3

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
# Slave fails to catch up with error 1032 handler error HA_ERR_KEY_NOT_FOUND
Slave failed to sync because of HA_ERR_KEY_NOT_FOUND
This error message is telling us that a row that was modified on the master can not be found on the slave:HA_ERR_KEY_NOT_FOUND. 

Let's dig into it.

Check slave status in slave db:
```bash
mysql>  show slave status \G;
*************************** 1. row ***************************
               Slave_IO_State: Waiting for master to send event
                  Master_Host: 10.10.0.72
                  Master_User: mconphoenixdbs04
                  Master_Port: 3306
                Connect_Retry: 60
              Master_Log_File: AUMELL131P-bin.009322
          Read_Master_Log_Pos: 1072540253
               Relay_Log_File: phoenix_DB-relay-bin.000249
                Relay_Log_Pos: 936273164
        Relay_Master_Log_File: AUMELL131P-bin.009288
             Slave_IO_Running: Yes
            Slave_SQL_Running: No
              Replicate_Do_DB:
          Replicate_Ignore_DB:
           Replicate_Do_Table:
       Replicate_Ignore_Table:
      Replicate_Wild_Do_Table:
  Replicate_Wild_Ignore_Table:
                   Last_Errno: 1032
                   Last_Error: Could not execute Update_rows event on table unified_message_interface.Message; Can't find record in 'Message', Error_code: 1032; handler error HA_ERR_KEY_NOT_FOUND; the event's master log AUMELL131P-bin.009288, end_log_pos 936273393
                 Skip_Counter: 0
          Exec_Master_Log_Pos: 936273013
              Relay_Log_Space: 37579824419
              Until_Condition: None
               Until_Log_File:
                Until_Log_Pos: 0
           Master_SSL_Allowed: No
           Master_SSL_CA_File:
           Master_SSL_CA_Path:
              Master_SSL_Cert:
            Master_SSL_Cipher:
               Master_SSL_Key:
        Seconds_Behind_Master: NULL
Master_SSL_Verify_Server_Cert: No
                Last_IO_Errno: 0
                Last_IO_Error:
               Last_SQL_Errno: 1032
               Last_SQL_Error: Could not execute Update_rows event on table unified_message_interface.Message; Can't find record in 'Message', Error_code: 1032; handler error HA_ERR_KEY_NOT_FOUND; the event's master log AUMELL131P-bin.009288, end_log_pos 936273393
  Replicate_Ignore_Server_Ids:
             Master_Server_Id: 10
1 row in set (0.00 sec)

[root@mcon-phoenixdbslave-04 mysql]# mysqlbinlog phoenix_DB-relay-bin.000249  –base64-output=decode-rows -v |grep -C 50 936273164
...
### UPDATE unified_message_interface.Message
### WHERE
###   @1=463715337
###   @2=1
###   @3=10234
###   @4=4778708098
###   @5='3773937'
###   @6=2019-07-14 00:12:59
###   @7=2026-07-17 00:12:59
###   @8=1
### SET
###   @1=463715337
###   @2=1
###   @3=10234
###   @4=4778708098
###   @5='3773937'
###   @6=2019-07-14 00:12:59
###   @7=2026-07-17 00:12:59
###   @8=3
# at 936273544
...
```

So we know that the unified_message_interface.Message table lost the ID=463715337 record.

Further check on the master node, I can see find out the all missing records and recover back to slave manually.

# Mysql export selected data to txt file
```sql
SELECT * INTO OUTFILE '/tmp/message.sql'
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n'
from  unified_message_interface.Message where ID >=463713873 and ID <=463719734
```

# Mysql load rows from txt file into table
```sql
LOAD DATA INFILE '/tmp/message.sql' INTO TABLE Message 
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';
```

# Copy Mysql Slave LXD snapshot and make it as a new Mysql Slave
## Background and requirement
- Mysql is running above ZFS system
- Current slave is running inside of LXD container and it has daily snapshot backup
- Need to use a snaphsot of the Mysql Slave to create a new slave, it might be promoted to master node in the future.

## Procedure
1. create an empty container on targer VM server
On the target VM server, create an empty container, destroy the zfs
```bash
root@mconvm-devall-01:~# lxc copy mcon-proxy-01 mcon-phoenixdb-01
root@mconvm-devall-01:~# zfs destroy -f lxd/containers/mcon-phoenixdb-01
```

2. Send ZFS snapshot from source VM server to targer VM server
```zsh
root@mysqlslaves:~# zfs send mysql/containers/AUMELL132D-SLAVE@snapshot-snap277 | pv -L 20m | ssh root@10.11.0.20 zfs receive -F lxd/containers/mcon-phoenixdb-01
```

3. Modify the new Mysql slave container IP address setting, hostname
```bash
root@mconvm-devall-01:~# zfs set mountpoint=/var/lib/lxd/containers/mcon-phoenixdb-01 lxd/containers/mcon-phoenixdb-01
root@mconvm-devall-01:~# cat /var/lib/lxd/containers/mcon-phoenixdb-01/rootfs/etc/sysconfig/network
NETWORKING=yes
NETWORKING_IPV6=no
HOSTNAME=mcon-phoenixdb-01.exmaple.com
GATEWAY=10.11.0.254
root@mconvm-devall-01:~# cat /var/lib/lxd/containers/mcon-phoenixdb-01/rootfs/etc/sysconfig/network-scripts/ifcfg-eth0
DEVICE=eth0
BOOTPROTO=static
ONBOOT=yes
IPADDR=10.11.0.22
NETMASK=255.255.255.0
NETWORK=10.11.0.0
root@mconvm-devall-01:~# cat /var/lib/lxd/containers/mcon-phoenixdb-01/rootfs/etc/hosts
127.0.0.1   localhost mcon-phoenixdb-01.exmaple.com AUMELL132D.exmaple.com
127.0.1.1   mcon-phoenixdb-01

# The following lines are desirable for IPv6 capable hosts
::1     ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
root@mconvm-devall-01:~#
```

4. Start new Mysql slave container and adjust the MYSQL settings, like server-id
```bash
root@mconvm-devall-01:~# lxc start mcon-phoenixdb-01
root@mconvm-devall-01:~# lxc exec mcon-phoenixdb-01 bash
[root@mcon-phoenixdb-01 ~]# vi /etc/my.cnf
[root@mcon-phoenixdb-01 ~]# /etc/init.d/mysql restart
```
5. Reset Master Slave replica

Grant slave permission on Master Mysql DB
```bash
mysql> GRANT REPLICATION SLAVE ON *.* TO 'aumell132d-slave'@'10.11.0.22' IDENTIFIED BY 'xxxxxx';
mysql> flush privileges;

```

```bash
mysql> show slave status\G;
*************************** 1. row ***************************
               Slave_IO_State:
                  Master_Host: 10.11.0.75
                  Master_User: aumell132d-slave
                  Master_Port: 3306
                Connect_Retry: 60
              Master_Log_File: AUMELL132D-bin.000883
          Read_Master_Log_Pos: 771908359
               Relay_Log_File: AUMELL132D-SLAVE-relay-bin.000509
                Relay_Log_Pos: 4
        Relay_Master_Log_File: AUMELL132D-bin.000883
             Slave_IO_Running: No
            Slave_SQL_Running: No
              Replicate_Do_DB:
          Replicate_Ignore_DB:
           Replicate_Do_Table:
       Replicate_Ignore_Table:
      Replicate_Wild_Do_Table:
  Replicate_Wild_Ignore_Table:
                   Last_Errno: 0
                   Last_Error:
                 Skip_Counter: 0
          Exec_Master_Log_Pos: 771908359
              Relay_Log_Space: 214
              Until_Condition: None
               Until_Log_File:
                Until_Log_Pos: 0
           Master_SSL_Allowed: No
           Master_SSL_CA_File:
           Master_SSL_CA_Path:
              Master_SSL_Cert:
            Master_SSL_Cipher:
               Master_SSL_Key:
        Seconds_Behind_Master: NULL
Master_SSL_Verify_Server_Cert: No
                Last_IO_Errno: 1045
                Last_IO_Error: error connecting to master 'aumell132d-slave@10.11.0.75:3306' - retry-time: 60  retries: 86400
               Last_SQL_Errno: 0
               Last_SQL_Error:
  Replicate_Ignore_Server_Ids:
             Master_Server_Id: 0
 
mysql> stop slave;
mysql> reset slave;
mysql> CHANGE MASTER TO MASTER_HOST='10.11.0.75',MASTER_USER='aumell132d-slave', MASTER_PASSWORD='xxxxxx',MASTER_LOG_FILE='AUMELL132D-bin.000883',MASTER_LOG_POS=771908359;
mysql> start slave;
mysql> show slave status\G;
*************************** 1. row ***************************
               Slave_IO_State: Waiting for master to send event
                  Master_Host: 10.11.0.75
                  Master_User: aumell132d-slave
                  Master_Port: 3306
                Connect_Retry: 60
              Master_Log_File: AUMELL132D-bin.000884
          Read_Master_Log_Pos: 99401646
               Relay_Log_File: mcon-phoenixdb-01-relay-bin.000004
                Relay_Log_Pos: 99401797
        Relay_Master_Log_File: AUMELL132D-bin.000884
             Slave_IO_Running: Yes
            Slave_SQL_Running: Yes
              Replicate_Do_DB:
          Replicate_Ignore_DB:
           Replicate_Do_Table:
       Replicate_Ignore_Table:
      Replicate_Wild_Do_Table:
  Replicate_Wild_Ignore_Table:
                   Last_Errno: 0
                   Last_Error:
                 Skip_Counter: 0
          Exec_Master_Log_Pos: 99401646
              Relay_Log_Space: 99402013
              Until_Condition: None
               Until_Log_File:
                Until_Log_Pos: 0
           Master_SSL_Allowed: No
           Master_SSL_CA_File:
           Master_SSL_CA_Path:
              Master_SSL_Cert:
            Master_SSL_Cipher:
               Master_SSL_Key:
        Seconds_Behind_Master: 0
Master_SSL_Verify_Server_Cert: No
                Last_IO_Errno: 0
                Last_IO_Error:
               Last_SQL_Errno: 0
               Last_SQL_Error:
  Replicate_Ignore_Server_Ids:
             Master_Server_Id: 1
1 row in set (0.00 sec)

ERROR:
No query specified

mysql>

           
```
