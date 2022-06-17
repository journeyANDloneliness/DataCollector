from discord.ext import commands
import re
import datetime
"""
helper functions
"""
def is_channel_exist(self, name=''):     
  for ch in self.get_all_channels():
    if ch.name == name:
      return ch
  return False

async def check_channel(self,channel, name):
  res = self.is_channel_exist(name)
  if res:
    return res
  else:
    await channel.send(f"channel with name {name} doesn't exist")
commands.Bot.is_channel_exist = is_channel_exist
commands.Bot.check_channel = check_channel


def findnth(string, substring, n):
   if (n == 1):
       return string.find(substring)
   else:
       return string.find(substring, findnth(string, substring, n - 1) + 1)


def bt_q(q):
  return f'```{q}```'
def bl_q(q):
  return re.sub("\n","\n> ",q)
  
def get_time():
  return datetime.datetime.now().strftime("%d-%m-%y;%H-%M")
  
def get_time_s():
  return datetime.datetime.now().strftime("%d-%m-%y;%H-%M-%S")
