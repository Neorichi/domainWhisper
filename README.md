# domainWhisper
> Get the lastest domains registred from whoisds database (Python3 based)


## Instalation

Install python3 and pip3

<pre> sudo apt install python3 </pre>
<pre> sudo apt install python3-pip</pre>

Install the dependencies via pip:

<pre> pip3 install -r requirements.txt </pre>

#### Telegram Implemetantion

To used of the telegram bot you need to get the chat id
<pre>
https://github.com/Neorichi/telegramWhisper
</pre>

#### Important

Change DB Config (mysql)
<pre>
host="xxxx.xxxx.us-east-1.rds.amazonaws.com"
port=3306
dbname="xxxxx"
user="xxxxx"
password="xxxxxx"
</pre>

Add "Example schema table" in your database
<pre>
CREATE TABLE `domains` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `link` varchar(250) COLLATE utf8_bin NOT NULL,
  `emails` blob,
  `created_at` timestamp NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
</pre>

Add Telegram API and Group ID (Optional)
<pre>
telegram_on = True
TOKEN = 'xxxxx:xxxx-xxx'
mi_canal = xxxxxx
</pre>


Change array tags
<pre>
tags = ['zonecama']
</pre>


## Usage
<pre>usage: python3 domainWhisper.py  </pre>

## Example
<pre>
python3 domainWhisper.py
python3 domainWhisper.py zonecama

 ____                        _    __        ___     _                     
|  _ \  ___  _ __ ___   __ _(_)_ _\ \      / / |__ (_)___ _ __   ___ _ __
| | | |/ _ \| '_ ` _ \ / _` | | '_ \ \ /\ / /| '_ \| / __| '_ \ / _ \ '__|
| |_| | (_) | | | | | | (_| | | | | \ V  V / | | | | \__ \ |_) |  __/ |   
|____/ \___/|_| |_| |_|\__,_|_|_| |_|\_/\_/  |_| |_|_|___/ .__/ \___|_|   
                                                         |_|              

11:43 13/05/19
-------
https://whoisds.com//whois-database/newly-registered-domains/MjAxOS0wNS0xMi56aXA=/nrd
['amzonex.com', 'dwizone.com', 'vizaone.com', 'zhjonescpa.com', 'zonephy.com', 'zonesn.com']
