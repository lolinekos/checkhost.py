import discord, asyncio
from subprocess import Popen, PIPE
from discord.ext import commands, tasks
import sys, os, socket, json
import requests
import subprocess

token = "ODI2OTIxNTcxNDE5MTYwNjg3.YGTgug.kk0FtWous1_ShWd0C0_vXqubIGs" #CHNAGE ME!!!

client = commands.Bot(command_prefix = '!n', case_insensitive=True)

client.remove_command("help")

#                    dP                   dP   dP         dP 
#                    88                   88   88         88 
#  88d888b. .d8888b. 88  .dP  .d8888b.    88 d8888P .d888b88 
#  88'  `88 88ooood8 88888"   88'  `88    88   88   88'  `88 
#  88    88 88.  ... 88  `8b. 88.  .88 dP 88   88   88.  .88 
#  dP    dP `88888P' dP   `YP `88888P' 88 dP   dP   `88888P8 
#  oooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
#                                                            
#  Discord.py script using the checkhost JSON api it's very 
#  Messy so bear with me. If you have any questions please
#  Message me @bleach | lolinekos#0001 on discord. This didn't take
#  more than 30 minutes to make so there most likely is some
#  issues but I've fixed all that I've seen.

nodes = "10" #number of checkhost requests

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send('This command is on cooldown.  Please wait %.2fs' % error.retry_after)
    elif isinstance(error, commands.errors.MissingPermissions):
        embed=discord.Embed(description="You do not have permissions to use this command", color=0x8000ff)
        await ctx.send(embed=embed)
    elif isinstance(error, commands.errors.MissingRequiredArgument):
        embed=discord.Embed(description="Missing an arg!", color=0x8000ff)
        await ctx.send(embed=embed)

@client.command()
async def help(ctx):
    embed=discord.Embed(title="__**Neko**__",description=f"""
{ctx.prefix}ping - IMCP request results
{ctx.prefix}tcping - TCP request results
{ctx.prefix}http - HTTP request results
{ctx.prefix}lookup - GEO ip information""", color=0x8000ff)
    await ctx.send(embed=embed)

@client.command()
async def lookup(ctx, ip):
	try:
		socket.gethostbyname(ip)
		geodat = ("http://ip-api.com/line/"+ip+"?fields=message,continent,continentCode,country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,offset,currency,isp,org,as,asname,reverse,query")
		resolve = requests.get(geodat)
		embed = discord.Embed(title="__**Neko**__",description=f"%s"%(resolve.text),color=0x8000ff)
		await ctx.send(embed=embed)

	except socket.gaierror:
		await ctx.send(f"{ip} is invaid please retry")

@commands.cooldown(rate=1, per=5, type=commands.BucketType.channel)
@client.command()
async def ping(ctx, ip):
	try:
		socket.gethostbyname(ip)
		await loading(ctx)
		jsonfood = requests.get('https://check-host.net/check-ping?host='+ip+'&max_nodes='+nodes,headers={'Accept': 'application/json'})
		jsonfood = jsonfood.text
		j = json.loads(jsonfood)
		req_id = j["request_id"]
		await asyncio.sleep(10)	
    
		jsonfood = requests.get('https://check-host.net/check-result/'+req_id,headers={'Accept': 'application/json'})
		jsonfood = jsonfood.text
		j = json.loads(jsonfood)
		embed=discord.Embed(title="__**Neko**__", description=f"ICMP response check-host result on {ip}", color=0x8000ff)
		embed.set_thumbnail(url="https://check-host.net/checkhost-favicon.png")
		#print(site_shit)
		for x in j :
			timeout = 0
			#print(x)
			try:
				for y in j[x][0]:
					if 'OK' in y:
						timeout = timeout + 1
			except TypeError:
				timeout = 0
			if timeout == 4:
				emoji = ":white_check_mark:"
			if timeout < 4:
				if timeout > 1:
					emoji = ":warning:"
			if timeout < 2 :
				emoji = ":x:"
			x = x.replace('.check-host.net', '')
			flagemoji = ":flag_"+x[0]+x[1]+":"
			embed.add_field(name=flagemoji+" "+x, value='RESULTS: '+emoji+' '+str(timeout)+'/4', inline=True)
			#print('RESULTS: '+str(timeout)+'/4')
		embed.set_footer(text=f"requested by {ctx.author.name} | https://check-host.net/check-result/"+req_id)
		await ctx.send(embed=embed)
	except socket.gaierror:
		await ctx.send(f"{ip} is invaid please retry")

async def loading(ctx):
	embed=discord.Embed(title="__**Neko**__", description=f"Please allow 10 seconds for the request", color=0x8000ff)
	embed.set_thumbnail(url="https://i.imgur.com/llF5iyg.gif")
	await ctx.send(embed=embed)

@commands.cooldown(rate=1, per=5, type=commands.BucketType.channel)
@client.command()
async def tcping(ctx, ip, port="80"):
	try:
		lmao = int(port)
		socket.gethostbyname(ip)
		await loading(ctx)
   
		jsonfood = requests.get('https://check-host.net/check-tcp?host='+ip+":"+port+'&max_nodes='+nodes,headers={'Accept': 'application/json'}).text	
		j = json.loads(jsonfood)

		req_id = j["request_id"]
		await asyncio.sleep(10)	
    
		jsonfood = requests.get('https://check-host.net/check-result/'+req_id,headers={'Accept': 'application/json'})
		jsonfood = jsonfood.text
		j = json.loads(jsonfood)
		embed=discord.Embed(title="__**Neko**__", description=f"TCP response check-host result on {ip}:{port}", color=0x8000ff)
		embed.set_thumbnail(url="https://check-host.net/checkhost-favicon.png")
		ptimeout = "Error "
		for x in j :
			timeout = 0
			#print(x)
			try:
				for y in j[x][0]:
					if 'time' in y:
						timeout = timeout + 1
						ptimeout = j[x][0]["time"]
						ptimeout = str(int(ptimeout*1000))
			except TypeError:
				timeout = 0
			if timeout == 1:
				emoji = ":white_check_mark:"
			if timeout == 0 :
				emoji = ":x:"
			x = x.replace('.check-host.net', '')
			flagemoji = ":flag_"+x[0]+x[1]+":"
			embed.add_field(name=flagemoji+" "+x, value=emoji+' '+str(ptimeout)+'ms', inline=True)
			#print('RESULTS: '+str(timeout)+'/4')
		embed.set_footer(text=f"requested by {ctx.author.name} | https://check-host.net/check-result/"+req_id)
		await ctx.send(embed=embed)
	except socket.gaierror:
		await ctx.send(f"{ip} is invaid please retry")

@commands.cooldown(rate=1, per=5, type=commands.BucketType.channel)
@client.command()
async def http(ctx, ip):
	try:
		socket.gethostbyname(ip)
		await loading(ctx)
		jsonfood = requests.get('https://check-host.net/check-http?host='+ip+'&max_nodes='+nodes,headers={'Accept': 'application/json'})
		jsonfood = jsonfood.text
		j = json.loads(jsonfood)

		req_id = j["request_id"]
		await asyncio.sleep(10)	
    
		jsonfood = requests.get('https://check-host.net/check-result/'+req_id,headers={'Accept': 'application/json'})
		jsonfood = jsonfood.text
		j = json.loads(jsonfood)
		embed=discord.Embed(title="__**Neko**__", description=f"HTTP response check-host result on {ip}", color=0x8000ff)
		embed.set_thumbnail(url="https://check-host.net/checkhost-favicon.png")
		for x in j :
			timeout = 0
			#print(x)
			try:
				for y in j[x][0]:
					emoji = ":x:"
					if 100 <= int(j[x][0][3]) <= 199:
						emoji = ":globe_with_meridians: "
					if 200 <= int(j[x][0][3]) <= 299:
						emoji = ":white_check_mark:"
					if 300 <= int(j[x][0][3]) <= 399:
						emoji = ":warning:"
					if 400 <= int(j[x][0][3]) <= 599:
						emoji = ":x:"
					ptimeout = j[x][0][2]
			except TypeError:
				emoji = ":x:"
				ptimeout = "Failed to get info"
			x = x.replace('.check-host.net', '')
			flagemoji = ":flag_"+x[0]+x[1]+":"
			embed.add_field(name=flagemoji+" "+x, value=emoji+' '+str(ptimeout), inline=True)
		embed.set_footer(text=f"requested by {ctx.author.name} | https://check-host.net/check-result/"+req_id)
		await ctx.send(embed=embed)
	except socket.gaierror:
		await ctx.send(f"{ip} is invaid please retry")

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f'my master | !nhelp'))
    print('''
          \x1b[38;5;197m╔╗╔┌─┐┬┌─┌─┐  ╦ ╔╦╗╔╦╗
          \x1b[38;5;198m║║║├┤ ├┴┐│ │  ║  ║  ║║
          \x1b[38;5;199m╝╚╝└─┘┴ ┴└─┘\x1b[0mo \x1b[38;5;199m╩═╝╩ ═╩╝  
  \x1b[0mDiscord bot for the Check host JSON API
    ''')
    print("        disc.py Version: "+discord.__version__)

client.run(token, bot=True)
