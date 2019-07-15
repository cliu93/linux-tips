# linux-tips
Linux Tips

## Doveco POP Log entries
/etc/dovecot/conf.d/20-pop3.conf
|  # POP3 logout format string:
|  #  %i - total number of bytes read from client
|  #  %o - total number of bytes sent to client
|  #  %t - number of TOP commands
|  #  %p - number of bytes sent to client as a result of TOP command
|  #  %r - number of RETR commands
|  #  %b - number of bytes sent to client as a result of RETR command
|  #  %d - number of deleted messages
|  #  %m - number of messages (before deletion)
|  #  %s - mailbox size in bytes (before deletion)
|  #  %u - old/new UIDL hash. may help finding out if UIDLs changed unexpectedly
|  #pop3_logout_format = top=%t/%p, retr=%r/%b, del=%d/%m, size=%s
