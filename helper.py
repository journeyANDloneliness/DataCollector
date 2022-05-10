from discord.ext import commands
import re
import datetime

def is_channel_exist(self, name=''):     
  for ch in self.get_all_channels():
    if ch.name == name:
      return ch
  return False
commands.Bot.is_channel_exist = is_channel_exist

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
