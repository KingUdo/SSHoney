This is a little SSH Honeypot which allows SSH bruteforce-bots to connect to it and loggs the username, password, timestamp and the IP into a SQLite Database.
Additional to that SQLite database is processed and printed out to a webpage. 

To get this running you need to move the SSH Port from 26 to 22:
```
sudo nano /etc/ssh/sshd_config
```
chnage port 22 to something like 26
```
Port 26
```

Then you will have to start the pshit file!
