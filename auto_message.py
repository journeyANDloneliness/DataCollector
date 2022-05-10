import discord
import re
from initialize import bot, col_sett
from message_job import MessageJob
from message_review import MessageReview
from bot_reply import BotReply
from pymaybe import maybe
from a import mr_pools, mj_pools, br_pools, ch_pools


  

@bot.event
async def on_ready():
  
  print("fetch started...")
  async for guild in bot.fetch_guilds():
    for channel in await  guild.fetch_channels():
      ch_pools[channel.id]=channel

      if channel.name == col_sett['review_ch']:
        async for message in channel.history(limit=200):
          d=maybe(re.search(r"(?<=id:)\d+", message.content)).group(0)
          if d and message.author == bot.user:
            mr=MessageReview()
            mr.message = message
            #put to chace only if its info somehow really are message review

            if not mr.analyze_info(message.content):

              mr_pools[message.id]=mr
              mr_pools[str(d)]=mr
    for channel in ch_pools.values():
      if channel.name in col_sett['channel']:
        async for message in channel.history(limit=200):
          if message.author != bot.user:
            continue
          d=maybe(re.search(r"(?<=id:)\d+",message.content)).group(0)
          if d:    
            #put to chace only if its has reference/ reply to jobs post
            ms = await channel.fetch_message(message.reference.message_id) 
            if ms:
              br=BotReply()
              br.message = message
              br.analyze_info(message.content)
              mj=MessageJob()
              mj.before = ms
              if str(d) in mr_pools.keys():
                mj.add_listener(mr_pools[str(d)])
                mr_pools[str(d)].add_listener(br)
              mj.add_listener(br)  
              
              mj_pools[ms.id] = mj
              mj_pools[str(d)]=mj
              br_pools[message.id] = br
              br_pools[str(d)]=br
  
  print("fetch done")
  
@bot.event
async def on_guild_join(guild):
  embedVar = discord.Embed(title="DataController v1.0",   description="""
Hi! welcome me. Im your server assistant to manage your data and collect it to the database""", color=0x00ff00)
  embedVar.add_field(name="Get Started!", value="""
To get started, first u should set which channel i will use to collect.
e.g. we want to collect post that posted in jobs channel.
use this command:```!channel jobs```.
with that command i will automatically starting to collect data from that channel.
however i will not collect data that posted before i joined.
to do so u need to call command:
```!collect -1```.
i will automatically setup every necesary things to make my system works.
i will make `review` channel under `Data Controll` category. within this channel you can reviewing jobs that user posted. i will only collect job to the database if it's reviewed.

there also some more!
u can also change my prefix command by ```!setup pre @```.""", inline=False)
  embedVar.add_field(name="Reviewing And Post Job", value="""
i will also create data-manager role, which is the role that can review and see review channel.
i pinned a message in review channel. check it to see  how to review. there also pinned messages in job channel when u run command: ```!channel jobs```.
check""", inline=False)
  embedVar.add_field(name="Command List", value="hi2", inline=False)
  channel = guild.system_channel 
  if channel.permissions_for(guild.me).send_messages:
    await channel.send(embed=embedVar)
  dc=await guild.create_category("Data Control")
  dm=await guild.create_role(name ="data-manager")
  await guild.me.add_roles(dm)
  await guild.create_text_channel(name="review", category=dc, overwrite=  {
    guild.default_role: discord.PermissionOverwrite(read_messages=False),
    dm: discord.PermissionOverwrite(read_messages=True)
})
  await guild.create_text_channel("featured-jobs", category=dc)
  await guild.create_text_channel("jobs board", category=dc)

