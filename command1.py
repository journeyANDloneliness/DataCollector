from initialize import in_sett, reconnect, q_set, botdb, col_sett, bot, mydb
from helper import bl_q, bt_q
import discord
import auto_message as am
"""command1. named it '1' because if u wants to add aditional command
please use other file. and import it to main.py  """
@bot.command(name='activate', help="activate [amount].activate the message before i login")
async def activate(ctx, cmd, *args):
    """cache data for the bot to listen to"""
    am.clear_cache_data()

    await am.cache_data(cmd)
    response = f"messages amount {cmd} succesfully activated "
    await ctx.send(bt_q(response))

@bot.command(name='clear', help="clear cache data manually")
async def clear(ctx, cmd="", *args):
    """clear the cached data exist in the pools! maybe something wrong?
    or the jobs channel changed? change server? or too many data and bot become slow?
    run this command!"""
    am.clear_cache_data()
    response = f"cache cleared!"
    await ctx.send(bt_q(response))

@bot.command(name='mongodb_coll', help="""mongodb_coll [collection name you want to strore]
  change mongo db collection""")
async def x(ctx, cmd, *args):
  """change which collection should this bot store?"""
  col_sett['store_coll']=cmd
  in_sett['job_coll'] = mydb[col_sett['store_coll']]
  reconnect(lambda : in_sett['bot_coll'].update_one(q_set,  {"$set":col_sett}, upsert=True))
  await ctx.send(bt_q(f"success change collection. from now i will store data to collection{cmd}"))
    
@bot.command(name='channel', help="""
             channel [channel name] [opt]
             """)
async def set_channel(ctx, cmd, *args):
  """set channel for bot to listen to"""
  response = "something  wrong..."

  if not any(ch.name == cmd for ch in bot.get_all_channels()):
    response = "no such channel found"
  else:     
    #o = json.loads(col_sett["channel"])
    
    if not cmd in col_sett['channel']:
      col_sett['channel'].append(cmd)

      response = "messages from channel '#"+cmd\
      +"' will be collected"
      print(col_sett['channel'])
      reconnect(lambda : in_sett['bot_coll'].update_one(q_set,  {"$set":col_sett}, upsert=True))
      ch = bot.is_channel_exist(cmd)
      embedVar = discord.Embed(title="JOBS POST RULES",   description="", color=0x1f45ee)
      embedVar.add_field(name="Job format example:", value="""

  [Hiring][Remote]
  Job Code: 10

  Job needs: Full-stack (React, Angular, Node) devs.
  Proven work record history: Minimum 3+ years
  English level needed: Minimum B2 level (reading, writing, speaking)
  Devs from locations: Ukraine, Moldova, Kazakhstan, Georgia only.
  Job location: Remote job
  Job type: Full-time job
  Salary: €3000-€5500 monthly net

  Apply: Send your CV to @Zero1 (please mention the Job Code in your message)
  """, inline=False)
      embedVar.add_field(name="Rules:", value="""
  ->[Hiring] or [Hire] tag is required!
  ->must have more than 4 descriptions""", inline=False)
      embedVar.add_field(name="Available Tag", value="""
  these tags are optional. u can add tag of your own too.
  here are some common tags:
  -level jobs:[Hobbyist][Amateur][Semi-Profesional][Profesional]
  -schedule:[part-time][full-time]
  -avilability:[2h/day][24h/week]
  -sallary:[$100+/week][unpaid]
  -job-role:[discord-admin][programmer]
  -job-tech:[react][vue][laravel]
                         """, inline=False)

      embedVar.add_field(name="Common Job Description", value="""
  here are some help for you about what too add in description to help your client to understand more about your job:
  English level needed: Minimum B2 level (reading, writing, speaking)
  Devs from locations: Ukraine, Moldova, Kazakhstan, Georgia only.
  Job location: Remote job
  Job type: Full-time job
  Salary: €3000-€5500 monthly net
  etc...
  """, inline=False)
      msg=await ch.send(embed=embedVar)
      await msg.pin()
  await ctx.send(bl_q(response))

@bot.command(name='review', help="""
             review [channel name] [opt]""")
async def set_review(ctx, cmd, *args):
  """command for set the review channel. if no review channel specified the bot will ask
  for new!"""
  print('u')
  if not bot.is_channel_exist(cmd):
    response = "no such channel found"
  else:     
    ch=bot.is_channel_exist(cmd)
    embedVar = discord.Embed(title="REVIEW",   description="", color=0x1f45ee)
    embedVar.add_field(name="How To?", value="""
    when there is jobs channel added with ```!channel``` command,
    i automatically collected anything posted on it.
    here the step:
    - I will check it, if it's match format i will send it to review channel.
    - In review channel, u can either give reaction 👍=OK or 👎=BAD to review.
    - I will only collect to database if staff user from `data-manager` role
      give OK review. a reaction '☁' is indicator the job posted already in the cloud.


  """, inline=False)
     
    msg=await ch.send(embed=embedVar)
    col_sett['review_ch'] = cmd
    response = f"channel {cmd} will used for reviewing jobs"
    reconnect(lambda : in_sett['bot_coll'].update_one(q_set,  {"$set":col_sett}, upsert=True))
    await msg.pin()
    
  await ctx.send(bl_q(response))

@bot.command(name='pre', help="""
             pre [any}""")
async def set_pre(ctx, cmd, *args):
  """change bot prefix. default '!'"""

  print('u')

  col_sett['pre']=cmd
  reconnect(lambda : in_sett['bot_coll'].update_one(q_set,  {"$set":col_sett}, upsert=True))
 
  await ctx.send(bt_q('prefix command succesfylly changed!'))

@bot.command(name='show_info', help="""
             show_info [0=false | 1=true]""")
async def set(ctx, cmd, *args):
  """a command to set wheter the bot should give verbose information to user when
  they post new job? use !show_info 0 will disable the bot for sending verbose message to user. """
  print('u')

  if int(cmd):
    col_sett['show_info']=True
  else:
    col_sett['show_info']=False
    print("print false please!")

  reconnect(lambda : in_sett['bot_coll'].update_one(q_set,  {"$set":col_sett}, upsert=True))
 
  await ctx.send(bt_q('info succesfylly changed!'))


