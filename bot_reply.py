from initialize import jobsdb, q_set, botdb, col_sett, bot
from helper import bl_q, bt_q
import format_filter as ff
import re

class BotReply:
  def __init__(self):
    self.listeners=[]
    self.message=None
    self.channel=None
    
    self.full_messages=""
    self.job_id=-1
    self.replied_to=-1
    self.status=-1
    self.usrid=-1
    self.usrstr=""
    
  def add_listener(self,l):
    self.listeners.append(l)
    
  def analyze_info(self, content):
    self.usrstr= re.search(r"(?<=user:)\S+",content).group(0)
    self.usrid= re.search(r"(?<=usr:)\d+",content).group(0)
    self.job_id= re.search(r"(?<=id:)\d+",content).group(0)
    
  def on_create(self,message,oe):
    data=ff.make_data(oe.message.content)
    a=ff.check_format(data)
  
    self.message=await oe.message.reply("")
    self.on_message_edit(None,oe, value=1 if a else 0,filter=a)
    self.usrstr= oe.message.author
    self.usrid= oe.message.author.id
    self.job_id=col_sett['last_id']
    
  def on_reaction_add(self, payload, oe, value=1):
    if value:
      await self.message.edit(content =bt_q(f"✅  <@!{self.usrid}>\
          your jobs with id:{self.jobid} succesfully reviewed"))
    else:
      print('didnt pass...')
      
      await self.message.edit(content =bt_q(f"❌  hi <@!{self.usrid}>\
          your jobs with id:{self.jobid}didn't pass reviewing phase. please check again how to post job correctly or ask @manager"))

  def on_message_edit(self,payload,oe,**kwargs):
    response=""
    if kwargs['value']:
      response= f" <@!{self.usrid}>\
          your jobs with id:{self.jobid}\n"+kwargs['filter']
    else:
      response=f" <@!{self.usrid}>\
          your jobs with id:{self.jobid} waiting for review... please wait..."
    await self.message.edit(bt_q(response))