# checkhost.py
Checkhost json api usage for all to use.

>Setup steps

# Debian/Raspi
1. `apt install python3-pip -y`
2. `pip3 install discord`
> `(optional) apt install screen -y`
4. `Change token.`
```python
import discord
from subprocess import Popen, PIPE
from discord.ext import commands, tasks
import sys, os, socket, json
import time
import requests
import subprocess

token = "NEKO NEKO" #CHNAGE ME!!!

client = commands.Bot(command_prefix = '!n', case_insensitive=True)

client.remove_command("help")
```
5. `python3 checkhost.py or screen -dmS bot python3 checkhost.py`
