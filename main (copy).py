# bot.py
from initialize import jobsdb, q_set, botdb, col_sett, bot
import os
import random
#import threading
import discord
from discord.ext import commands
#from dotenv import load_dotenv
import json
import datetime
#from replit import db
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import format_filter as ff
from helper import bl_q, bt_q
import re
from pymaybe import maybe
import auto_message
import command1
from auto_message import mr_pools, mj_pools, br_pools, ch_pools


@bot.event
async def on_message(message):
    
    if message.author == bot.user:
      return
    await bot.process_commands(message)
    if bot.get_command(message.content[1:]):
      return
    if type(message.channel) is discord.TextChannel:
      if message.channel.name in col_sett["channel"]:
        
        ch = bot.is_channel_exist(col_sett["review_ch"])
        if not ch:
          response = f"review channel doesnt exist! please set one type {col_sett['pre']}help for help"
        else: 
          col_sett['last_id']+=1
          
          data=ff.make_data(message.content)
          a=ff.check_format(data)
          if a:
            response= f"your jobs with id:{col_sett['last_id']}\n"+a
          else:
            response= f"jobs id:{col_sett['last_id']} waiting for review... please wait..."
           
            
            jobs_cb_msg= f"#{'='*29}\n```usr:{message.author.id} user:{message.author} id:{col_sett['last_id']}```\n{'='*29}#\n {message.content}"
            print(bl_q(jobs_cb_msg))
            
            await ch.send(bl_q(jobs_cb_msg))
          
        await message.reply(bt_q(response))
        botdb.update_one(q_set,  {"$set":col_sett}, upsert=True)
        
@bot.event
async def on_message_edit(before, after):
  print("didnt clled")
  if before.channel.name in col_sett["channel"]:

    async for message in before.channel.history(limit=30):
      if message.author == bot.user:
        if maybe(message.reference).message_id == before.id:
          data=ff.make_data(after.content)
          a=ff.check_format(data)
          idn=int(re.search(r"(?<=id:)\d+", message.content).group(0))
          if a:
            response= f"your jobs with id:{idn}\n"+a
          else:
            response= f"your jobs updated. id:{idn} waiting for review... please wait..."
           
            
            ch = bot.is_channel_exist(col_sett["review_ch"])
            if not ch:
              pass
            else:
              message_review_found=None
              async for message2 in ch.history(limit=30):
                if message2.author == bot.user:
                  if int(maybe(re.search(r"(?<=id:)\d+", message2.content)).group(0) or -1) == idn:
                    print("founf")
                    update_count=int(maybe(re.search(r"(?<=update_count:)\d+", message2.content)).group(0) or 0)
                    update_count+=1
                    a =  message2.content.replace("> ","")
                    b=a.split("=#")
                    c=b[0]+"=#"
                    #if update_count < 1:
                      
                    c=re.sub(r"(?<=update_count:)\d+",str(update_count), c)
                    
                    d=re.search(r"(?<=id:)\d+", b[0]).group(0)
                    jobs_cb_msg= f"{c}{after.content}"
                    await message2.edit(content=bl_q(jobs_cb_msg))
                    print(bl_q(jobs_cb_msg))
                    await message2.reply(bt_q(f"{d} updated their jobs. check it now @manager"))
                    message_review_found=message2
                    break
              if not message_review_found:
                jobs_cb_msg= f"#{'='*29}\n```update_count:1\nusr:{after.author.id} user:{after.author} id:{col_sett['last_id']}```\n{'='*29}#\n {after.content}"
                print(bl_q(jobs_cb_msg))   
                await ch.send(bl_q(jobs_cb_msg))

              await before.add_reaction("🔄")
            
          await message.edit(content=bt_q(response))
          
@bot.event
async def on_raw_reaction_add(payload):
  if ch_pools[payload.channel_id].name == col_sett["review_ch"]:
    mr_pools[payload.message_id].on_reaction(payload)
    
@bot.event
async def on_reaction_add(reaction,user):
  if reaction.message.channel.name == col_sett["review_ch"]:
    print("reaction please!\n")
    response=""
    idn=re.search(r"(?<=id:)\d+", reaction.message.content)
    
   # print(idn)
    if idn == None:
      print("no id")
      return
    if bot.user != reaction.message.author:
      print(reaction.message.author)
      print(bot.user)
      return
    if reaction.count > 1:
      print("already")
      return
    idn= int(idn.group(0))
    usrstr= re.search(r"(?<=user:)\S+",reaction.message.content).group(0)
    usrid= re.search(r"(?<=usr:)\d+",reaction.message.content).group(0)
    
    print(int(usrid))
    #discord.utils.get(bot.get_guild(int(reaction.message.guild.id)).members,\
    # name="frog", discriminator="5827")
    usr= await bot.fetch_user(int(usrid))
    print(reaction.emoji)
    if reaction.emoji == "👍":
      
      for r in reaction.message.reactions:
        if r.emoji == "👎":
          await reaction.message.clear_reaction("👎")
      
      response="review done. jobs will be added in database"
      breako=False
      for ch in col_sett["channel"]:
        ch = bot.is_channel_exist(ch)
        async for message in ch.history(limit=30):
          if bot.user == message.author:
            print("here goes...")
            if int(maybe(re.search(r"(?<=id:)\d+", message.content)).group(0) or -1)== idn :
              print('reviewd...')
              await message.edit(content =bt_q(f"✅  <@!{usr.id}>\
                  your jobs with id:{idn} succesfully reviewed"))
              raw=reaction.message.content.split("=#")
              data=ff.make_data(raw[1])
              #raw[0]
              data["idx"]=idn
              data["dicord_id"]=usrstr
              data["user"]=usr.id
              data["manage"]["reviews"].append({"reaction":"👍", "staff":user.name+"#"+user.discriminator, \
                "date":datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
              if '_id' in data: 
                del data['_id'] 
              jobsdb.update_one({"idx":idn}, {"$set":data},upsert=True)
              await message.add_reaction("☁")
              
              breako=True 
              break
        if breako: break
            
          
    elif reaction.emoji == "👎":
      for r in reaction.message.reactions:
        if r.emoji == "👍":
          await reaction.message.clear_reaction("👍")
      breako=False
      for ch in col_sett["channel"]:
        ch = bot.is_channel_exist(ch)
        async for message in ch.history(limit=30):
          if bot.get_user(bot.user.id) == message.author:
            if int(re.search(r"(?<=id:)\d+", message.content).group(0))==idn :
              print('didnt pass...')
              
              await message.edit(content =bt_q(f"❌  hi <@!{usrid}>your jobs with id:{idn} didn't pass reviewing phase. please check again how to post job correctly or ask @manager"))
              
              breako=True 
        if breako: break
      response="i will tell user to edit their jobs message"
    else: return
        
    await reaction.message.reply(bt_q(response))


          

print(col_sett['channel'])
bot.run("OTcxOTQ1NjI4MTY5MDExMjQw.YnR45w.fXTn_RxzOByKuHnDH-5__qZhz78")



