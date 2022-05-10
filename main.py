# bot.py
from initialize import jobsdb, q_set, botdb, col_sett, bot, TOKEN
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

@bot.event
async def on_message(message):
    
    if message.author == bot.user:
      return
    await bot.process_commands(message)
    if bot.get_command(message.content[1:]):
      return
    if type(message.channel) is discord.TextChannel:
      if message.channel.name in col_sett["channel"]:
        response=""
        ch = bot.is_channel_exist(col_sett["review_ch"])
        if not ch:
          response = f"review channel doesnt exist! please set one type {col_sett['pre']}help for help"
        else: 
          col_sett['last_id']+=1
          mj = MessageJob()
          mj.message = message
          await mj.on_create(message,None)

          
        await message.reply(bt_q(response))
        botdb.update_one(q_set,  {"$set":col_sett}, upsert=True)
        

          
@bot.event
async def on_raw_reaction_add(payload):
  if ch_pools[payload.channel_id].name == col_sett["review_ch"]:
    if payload.message_id in mr_pools.keys():
      await mr_pools[payload.message_id].on_reaction_add(payload,None)
@bot.event
async def on_raw_message_edit(payload):
  if ch_pools[payload.channel_id].name in col_sett["channel"]:
    if payload.message_id in mr_pools.keys():
      await mj_pools[payload.message_id].on_message_edit(payload,None)

     

print(col_sett['channel'])
bot.run(TOKEN)



