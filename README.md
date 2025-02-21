TP-link PoE switch port control, for TL-SG1016PE

Smart switches are great because they're significantly cheaper (and often smaller) than fully managed, and yet allow you to configure basic vlans, not
to mention for PoE they actually give you some power info, so you can figure out if you're near the limit.

The problem is that remote management may be completely non-standard.  I can't understand this, SNMP or a basic API would be very low overhead
but TPLink just have the web interface for the above switch and then some Windows-only software in case the web IF doesn't work which I couldn't make
work under Wine.

I only need to disable and re-enable ports at certain times of day but the protocol is pretty simple and the script could be easily extended to do other stuff.

TO use, run this script without parameters to see the port status:

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

