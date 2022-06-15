# bot.py
from initialize import in_sett, reconnect,  q_set, botdb, col_sett, bot, TOKEN
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
from a import mr_pools, mj_pools, br_pools, ch_pools
from message_job import MessageJob
import logging
"""
after the code inside initialize.py and auto_message.py executed by import
here is the start of the program where the bot read the changes in discord server.
we use on_raw_(event_name) instead of on_(event_name) 
because this bot has ability to fetch any message before it's turned on,
thats whats auto_message.py do. while initialize.py is conecting to database/load env/read bot settings etc...
"""

@bot.event
async def on_message(message):
    """since message sent will always new. we doesn't use on_raw..
    it's listen for any  incoming message in job's channel.(setup by !channel (channel_name)) """
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
          await message.reply(bt_q(response))
        else: 
          col_sett['last_id']+=1
          mj = MessageJob()
          mj.message = message
          mj.channel = message.channel
          await mj.on_create(message,None)
          mj_pools[mj.message.id] = mj

          
        
        reconnect(lambda : in_sett['bot_coll'].update_one(q_set,  {"$set":col_sett}, upsert=True))
        

          
@bot.event
async def on_raw_reaction_add(payload):
  """is reaction added ? whter the message is already exist before the bot was on?
  it's listen to any reaction changes"""
  print("goooooo")
  if ch_pools[payload.channel_id].name == col_sett["review_ch"]:
    if payload.message_id in mr_pools.keys():
      print("goooooo")
      await mr_pools[payload.message_id].on_reaction_add(payload,None)
@bot.event
async def on_raw_message_edit(payload):
  """is message edited? whter the message is already exist before the bot was on?
  it's listen to any edited message"""

  if ch_pools[payload.channel_id].name in col_sett["channel"]:
    print("goooooo uuuu")
    if payload.message_id in mj_pools.keys():
      print("goooooo uuuu")
      """mj == mesage_job. an object pools 
      """
      await mj_pools[payload.message_id].on_message_edit(payload,None)

@bot.event
async def on_guild_channel_create(channel):
  """because we also need new created channel to exist in the pools, otherwise
  the bot don't know if new channel exist"""
  ch_pools[channel.id]=channel

print(col_sett['channel'])
"""run the bot with token from env"""
bot.run(TOKEN)



