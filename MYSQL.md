# Show MySQL process list
```
SELECT user, time, state, info 
  FROM 
information_schema.processlist 
  WHERE command != 'Sleep' 
    AND 
    time >= 2 
    ORDER BY time DESC, id \G
```
