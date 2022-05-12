from initialize import in_sett, reconnect,  q_set, botdb, col_sett, bot
from a import AutoMessage
from message_review import MessageReview
from bot_reply import BotReply
import format_filter as ff
from a import mr_pools, mj_pools, br_pools, ch_pools

class MessageJob(AutoMessage):
  def __init__(self):
    self.listeners=[]
    self.message=None
    self.channel=None
    
    self.before=None
    self.after=None
    self.job_id=-1
    
  def add_listener(self,l):
    self.listeners.append(l)

  async def on_create(self, message, oe):
    self.message = message
    self.job_id = col_sett['last_id']
    ch = bot.is_channel_exist(col_sett["review_ch"])
    mr=await self.make_message_review(None,ch)
    br=await self.make_bot_reply(None,ch)
    mr.add_listener(br)
    
  async def on_message_edit(self, payload,oe):
    print("didnt clled")
    self.before = self.message
    self.message=await self.channel.fetch_message(self.message.id)
    self.after=self.message
    data=ff.make_data(self.message.content)
    a=ff.check_format(data)

    if a:
      for l in self.listeners:
        await l.on_message_edit(payload,self,value=1, filter=a)
    else:
      for l in self.listeners:
        await l.on_message_edit(payload,self,value=0, filter=a)
     
      
      ch = bot.is_channel_exist(col_sett["review_ch"])
      if not ch:
        pass
      else:
        message_review_found=any([type(l) is MessageReview for l in self.listeners])
        if not message_review_found:
          self.make_message_review(payload,ch).\
          on_message_edit(payload, self)
        reply_found=any([type(l) is BotReply for l in self.listeners])
        if not reply_found:
          self.make_bot_reply(payload,ch).\
          on_message_edit(payload, self)
          
      await self.message.add_reaction("🔄")
      
  async def make_message_review(self,payload,ch):
    mr=MessageReview()
    mr.channel=ch
    await mr.on_create(self.message,self)

    self.add_listener(mr)
    mr_pools[mr.message.id]=mr
    return mr
  
  async def make_bot_reply(self,payload,ch):
    br=BotReply()
    br.channel=ch
    await br.on_create(self.message,self)
    
    self.add_listener(br)
    if br.message:
      br_pools[br.message.id]=br
    return br