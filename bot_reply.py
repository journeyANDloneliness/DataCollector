from initialize import in_sett, reconnect,  q_set, botdb, col_sett, bot
from helper import bl_q, bt_q
import format_filter as ff
import re
from pymaybe import maybe
from a import br_pools

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
    self.usrstr= maybe(re.search(r"(?<=user:)\S+",content)).group(0)
    self.usrid= maybe(re.search(r"(?<=usr:)\d+",content)).group(0)
    self.job_id= maybe(re.search(r"(?<=id:)\d+",content)).group(0)

    #if len(mc)<2 or self.usrstr == None or self.usrid == None or self.job_id == None:
    # return False
    
  async def on_create(self,message,oe):
    data=ff.make_data(oe.message.content)
    a=ff.check_format(data)

    self.usrstr= oe.message.author
    self.usrid= oe.message.author.id
    self.job_id=col_sett['last_id']
    self.replied_to = oe.message
    if not col_sett['show_info']:
      return
    print("why u always calling me????")

    print(col_sett['show_info'])
    print("why u always calling me????")
    self.message=await oe.message.reply(".........")
    await self.on_message_edit(None,oe, value=1 if a else 0,filter=a)
 
    
  async def on_reaction_add(self, payload, oe, value=1):
    if not col_sett['show_info']:
      return
    if not self.message:
      self.message=await replied_to.message.reply(".........")
      br_pools[self.message.id]=self
    if value:
      await self.message.edit(content =bt_q(f"✅  <@!{self.usrid}>\
          your jobs with id:{self.job_id} succesfully reviewed"))
    else:
      print('didnt pass...')
      
      await self.message.edit(content =bt_q(f"❌  hi <@!{self.usrid}>\
          your jobs with id:{self.job_id}didn't pass reviewing phase. please check again how to post job correctly or ask @manager"))

  async def on_message_edit(self,payload,oe,**kwargs):
    if not col_sett['show_info']:
      return
    if not self.message:
      self.message=await replied_to.message.reply(".........")
      br_pools[self.message.id]=self
    response=""
    if kwargs['value']:
      response= f" <@!{self.usrid}>\
          your jobs with id:{self.job_id}\n"+kwargs['filter']
    else:
      response=f" <@!{self.usrid}>\
          your jobs with id:{self.job_id} waiting for review... please wait..."
    await self.message.edit(content=bt_q(response))
    print("why>???????? inever called")