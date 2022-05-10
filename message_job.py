from initialize import jobsdb, q_set, botdb, col_sett, bot
from auto_message import AutoMessage
from message_review import MessageReview
from bot_reply import BotReply
import format_filter as ff
from auto_message import mr_pools, mj_pools, br_pools, ch_pools

class MessageJob(AutoMessage):
  def __init__(self):
    self.listeners=[]
    self.message=None
    self.channel=None
    
    self.before=None
    self.after=None
    self.job_id
    
  def add_listener(self,l):
    self.listeners.append(l)

  def on_create(self, message, oe):
    self.message = message
    self.job_id = col_sett['last_id']
    mr=self.make_message_review(None)
    br=self.make_bot_reply(None)
    mr.add_listener(br)
    
  def on_message_edit(self, payload,oe):
    print("didnt clled")
    self.before = self.message
    self.message=await self.channel.fetch_message(self.message.id)
    self.after=self.message
    data=ff.make_data(self.message.content)
    a=ff.check_format(data)

    if a:
      for l in self.listeners:
        l.on_message_edit(payload,self,value=1, filter=a)
    else:
      for l in self.listeners:
        l.on_message_edit(payload,self,value=0, filter=a)
     
      
      ch = bot.is_channel_exist(col_sett["review_ch"])
      if not ch:
        pass
      else:
        message_review_found=any([l is MessageReview for l in self.listeners])
        if not message_review_found:
          self.make_message_review(payload,ch).\
          on_message_edit(payload, self)
        reply_found=any([l is BotReply for l in self.listeners])
        if not reply_found:
          self.make_bot_reply(payload,ch).\
          on_message_edit(payload, self)
          
      await self.message.add_reaction("🔄")
      
  def make_message_review(self,payload,ch):
    mr=MessageReview()
    mr.channel=ch
    mr.on_create(self.message,self)

    self.add_listener(mr)
    mr_pools.append(mr)
    return mr
  
  def make_bot_reply(self,payload,ch):
    br=BotReply()
    br.channel=ch
    br.on_create(self.message,self)
    
    self.add_listener(br)
    br_pools.append(br)
    return br