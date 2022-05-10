from initialize import jobsdb, q_set, botdb, col_sett, bot
from helper import bl_q, bt_q, get_time
import re

from pymaybe import maybe
import format_filter as ff

class MessageReview:
  def __init__(self):
    self.listeners=[]
    #must available upon creation
    self.channel=None
    self.message=None
    
    self.log_data={"update_count":0}
    self.log_text=""
    self.usrid=""
    self.usrstr=""
    self.job_id=-1
    self.msg_refer_to=None
    self.text_ok_rev=""
    self.content=""
    self.job_text=""
    self.text_lf_top='#'+'='*29
    self.text_lf_bottom='='*29+'#'
    self.text_ls='-'*30
    
  def add_listener(self,l):
    self.listeners.append(l)

  def on_create(self, message, eo=None):           
    self.content= f"#{'='*29}\n```usr:{message.author.id} user:{message.author} id:{col_sett['last_id']}```\n{'='*29}#\n {message.content}"
    self.job_text=message.content
    #a message which this review listen to the their change
    self.msg_refer_to=message
    print(bl_q(self.content))      
    self.message=await self.channel.send(bl_q(self.content))

  def on_message_edit(self, payload, eo):
    print("founf")
    #self.log_data['update_count']=int(maybe(re.search(r"(?<=update_count:)\d+", message2.content)).group(0) or 0)
    self.log_data['update_count']+=1
    self.log_data['update'+self.log_data['update_count']]=["date="+get_time()]
    
    # a =  message2.content.replace("> ","")
    # b=a.split("=#")
    # c=b[0]+"=#"
    #if update_count < 1:
    # c=re.sub(r"(?<=update_count:)\d+",str(update_count), c)
    # d=re.search(r"(?<=id:)\d+", b[0]).group(0)
    self.arrange_log()    
    self.job_text=eo.message.content
    self.post_message()
    await self.message.reply(bt_q(f"{self.usrstr} updated their jobs. check it now @manager"))
    await self.message.add_reaction("🔄")
    
    
  def post_message(self):
    jobs_cb_msg= f"{self.text_log}{self.job_text}"
    self.content=jobs_cb_msg
    await self.message.edit(content=bl_q(jobs_cb_msg))
    print(bl_q(jobs_cb_msg))
    
  def analyze_info(self, content):
    self.usrstr= re.search(r"(?<=user:)\S+",content).group(0)
    self.usrid= re.search(r"(?<=usr:)\d+",content).group(0)
    self.job_id= re.search(r"(?<=id:)\d+",content).group(0)

    mc=content.split("=#")
    self.log_text = mc[0].replace("> ","")
    self.job_text = mc[1].replace("> ","")

    self.log_data['update_count']=int(maybe(re.search(r"(?<=update_count:)\d+",self.log_text)).group(0) or 0)
    rpat=re.search(r"review\d+(?=:)(:.+\n)",self.log_text)
    rls=maybe(rpat).group(0) or []
    for v,k in enumerate(rls):
      #group 1 definitly exist
      self.log_data[v]=rpat.group(1)[k].split("|")
    upat=re.search(r"update\d+(?=:)(:.+\n)",self.log_text)
    uls=maybe(upat).group(0) or []
    for v,k in enumerate(uls):
      #group 1 definitly exist
      self.log_data[v]=upat.group(1)[k].split("|")
    dpat=re.search(r"\d\d-\d\d-\d\d\;.+(?=:)(.+\n)",self.log_text)
    dls=maybe(dpat).group(0) or []
    for v,k in enumerate(dls):
      #group 1 definitly exist
      self.log_data[v]=dpat.group(1)[k]
      
    self.log_data['delete']=maybe(re.search(r"(?<=delete:).+\n",self.log_text)).group(0) or ""
  
    
    
  def arrange_log(self):
    out=""
    out+= self.text_lf_top+"\n"
    out+=f"{self.usrstr} {self.usrid} {self.job_id}\n"
    
    out+=self.text_ls+"\n"
    if self.log_data['update_count']:
      out+='update_count: '+self.log_data['update_count']+"\n"
    for x in [(k,v) for k,v in self.log_data.items() if "review" in k]:
      out+=f"{x[0]}: {'|'.join(x[1])}\n"
  
    for x in [(k,v) for k,v in self.log_data.items() if "update" in k]:
      out+=f"{x[0]}: {'|'.join(x[1])}\n"
      
    if self.log_data['delete']:
      out+='delete: '+self.log_data['delete']+"\n"
      
    out+=self.text_ls+"\n"
    for x in [(k,v) for k,v in self.log_data.items() if "\\" in k]:
      out+=f"{x[0]}: {x[1]}\n"
    out+=self.text_lf_bottom+"\n"
    self.log_text=out
    
  def on_reaction_add(self,payload):

    
    #print(int(self.usrid))
    #discord.utils.get(bot.get_guild(int(reaction.message.guild.id)).members,\
    # name="frog", discriminator="5827")
    #usr= await bot.fetch_user(int(usrid))
    print(payload.emoji)
    if payload.emoji == "👍":
      
      for r in self.message.reactions:
        if r.emoji == "👎":
          await self.message.clear_reaction("👎")
      
      self.log_data[get_time]=" review done. jobs will be added in database!"
      breako=False

      print("here goes...")

      print('reviewd...')
      for ls in self.listeners:
        ls.on_reaction_add(payload, self)
      #raw=reaction.message.content.split("=#")
      data=ff.make_data(self.job_text)
      #raw[0]
      data["job_id"]=self.job_id
      data["dicord_id"]=self.usrstr
      data["user"]=self.usrid
      data["manage"]=self.log_data
      if '_id' in data: 
        del data['_id'] 
      jobsdb.update_one({"idx":self.job_id}, {"$set":data},upsert=True)
      await self.message.add_reaction("☁")

            
          
    elif payload.emoji == "👎":
      for r in self.message.reactions:
        if r.emoji == "👍":
          await self.message.clear_reaction("👍")
      for ls in self.listeners:
        ls.on_reaction_add(payload, self,value=0)

              
              

      self.log_data[get_time]==" i will tell user to edit their jobs message"
    else: return
      
    self.arrange_log()
    self.post_message()
    
    