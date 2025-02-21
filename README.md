Run this script without parameters to see the port status:

```
$ ./tplink_port.py 
Port 1: enabled
Port 2: enabled
Port 3: enabled
Port 4: enabled
Port 5: enabled
Port 6: enabled
Port 7: enabled
Port 8: enabled
Port 9: enabled
Port 10: enabled
Port 11: enabled
Port 12: enabled
Port 13: enabled
Port 14: enabled
Port 15: enabled
Port 16: enabled
```

Or just show a single port value, maybe for use in scripts or something

```
$ ./tplink_port.py 1
enabled
```

Or of course you can disable/enable:

```
$ ./tplink_port.py 1 disable
Status Code: 200
$ ./tplink_port.py 1
disabled
```

