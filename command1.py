from initialize import jobsdb, q_set, botdb, col_sett, bot
from helper import bl_q, bt_q
import discord

@bot.command(name='manual', help="manual data collection")
async def collect_manual(ctx):
    
    response = "data collected"
    await ctx.send(bt_q(response))
    
@bot.command(name='setup', help="""
             1.channel [channel name] [opt]
             2.review_ch [channel name]""")
async def test(ctx, cmd, *args):
    response = "x"
    if cmd == "channel":
      if len(args) > 0:
        if not any(ch.name == args[0] for ch in bot.get_all_channels()):
          response = "no such channel found"
        else:     
          #o = json.loads(col_sett["channel"])
          
          if not args[0] in col_sett['channel']:
            col_sett['channel'].append(args[0])
    
          response = "messages from channel '#"+args[0]\
          +"' will be collected"
          print(col_sett['channel'])
          botdb.update_one(q_set,  {"$set":col_sett}, upsert=True)
          ch = bot.is_channel_exist(args[0])
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
    elif cmd == "review_ch":
      print('u')
      if not bot.is_channel_exist(args[0]):
        response = "no such channel found"
      else:     
        col_sett['review_ch'] = args[0]
        response = f"channel {args[0]} will used for reviewing jobs"
        botdb.update_one(q_set,  {"$set":col_sett}, upsert=True)
      await ctx.send(bl_q(response))