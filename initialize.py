# bot.py
import os
import random
#import threading
import discord
from discord.ext import commands
from dotenv import load_dotenv
import json
import datetime
#from replit import db
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import format_filter as ff
import helper as h
import re
from pymaybe import maybe

modb = MongoClient("mongodb+srv://rum:12345@cluster0.xtg4o.mongodb.net/rum_data1?retryWrites=true&w=majority", server_api=ServerApi('1'))
mydb = modb["rum_data1"]

botdb=mydb["bot_settings"]
q_set={"bot_name":"dataCollector"}
col_sett=botdb.find_one(q_set)
print(col_sett)



load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
if 'pre' not in col_sett:
	col_sett['pre'] ='!'

clientintents  = discord.Intents.all()
bot = commands.Bot(command_prefix=lambda guild,message:col_sett['pre'])
#bot.login("akystpobv939uGegax44hb_C5qKcX91C")



in_sett={}
in_sett['job_coll']=mydb[col_sett['store_coll']]
in_sett['bot_coll']=mydb['bot_settings']

def reconnect(q):
	res = q()
	if not res:
		modb = MongoClient("mongodb+srv://rum:12345@cluster0.xtg4o.mongodb.net/rum_data1?retryWrites=true&w=majority", server_api=ServerApi('1'))
		mydb = modb["rum_data1"]
		botdb=mydb["bot_settings"]
		in_sett['bot_coll']=mydb['bot_settings']
		#col_sett=in_sett['bot_coll'].find_one(q_set)
		#recheck_settings(col_sett)
		in_sett['job_coll']=mydb[col_sett['store_coll']]
		

		q()
		print("reconnect")
	else:
		return res


if not col_sett:
	col_sett = q_set


def recheck_settings(col_sett):


	if 'channel' not in col_sett:
		col_sett['channel'] = []
	if 'review_ch' not in col_sett:
		col_sett['review_ch'] ='review'
	if 'last_id' not in col_sett:
		col_sett['last_id'] = 0
	if 'store_coll' not in col_sett:
		col_sett['store_coll'] = 'coll1'
	if 'show_info' not in col_sett:
		col_sett['show_info'] = False

recheck_settings(col_sett)
print("initialize...")
