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

"""
this is file is for initializing. called first when main.py imported it.
for loading env file, connect and load data from mongo_db cloud.
there are 2 collection loaded.
by default use collection from rum_data1.

1. bot setting collection loaded into list in_sett['job_coll']
2. jobs collection loaded into list in_sett['job_coll']

import in_sett['job_coll'] as your need to manipulate collection thats rendered on website

"""
modb = MongoClient("mongodb+srv://rum:12345@cluster0.xtg4o.mongodb.net/rum_data1?retryWrites=true&w=majority", server_api=ServerApi('1'))
mydb = modb["rum_data1"]

botdb=mydb["bot_settings"]
q_set={"bot_name":"dataCollector"}
col_sett=botdb.find_one(q_set)
print(col_sett)

TOKEN = None

is_prod = os.environ.get('IS_HEROKU', None)

if is_prod:
	TOKEN = os.getenv('DISCORD_TOKEN')
else
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
	"""called everytime need something from cloud.
	because sometimes the connection shut down. the bot need to check
	whether the connection to cloud exist?"""
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
