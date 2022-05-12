from initialize import in_sett, reconnect, q_set, botdb, col_sett, bot
from helper import bl_q, bt_q, get_time, get_time_s
import re
import json
import pprint as pp
from pymaybe import maybe
import format_filter as ff

class MessageReview:
  def __init__(self):
    self.listeners=[]
    #must available upon creation
    self.channel=None
    self.message=None
    
    self.log_data={"update_count":0,"delete":"-"}
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
    self.text_ls='-'*40
    
  def add_listener(self,l):
    self.listeners.append(l)

  async def on_create(self, message, eo=None):           
    self.content= f"#{'='*29}\n```user:{message.author} usr:{message.author.id} id:{col_sett['last_id']}```\n{'='*29}#\n {message.content}"
    self.usrstr=str(message.author)
    self.usrid=message.author.id
    self.job_id = col_sett['last_id']

    self.job_text=message.content
    #a message which this review listen to the their change
    self.msg_refer_to=message
    print(bl_q(self.content))      
    self.message=await self.channel.send(bl_q(self.content))

  async def on_message_edit(self, payload, eo, **kwargs):
    print("founf")
    #self.log_data['update_count']=int(maybe(re.search(r"(?<=update_count:)\d+", message2.content)).group(0) or 0)
    self.log_data['update_count']+=1
    self.log_data['update'+str(self.log_data['update_count'])]=["date="+get_time()]
    
    # a =  message2.content.replace("> ","")
    # b=a.split("=#")
    # c=b[0]+"=#"
    #if update_count < 1:
    # c=re.sub(r"(?<=update_count:)\d+",str(update_count), c)
    # d=re.search(r"(?<=id:)\d+", b[0]).group(0)
    self.arrange_log()    
    self.job_text=eo.message.content
    await self.post_message()
    await self.message.reply(bt_q(f"{self.usrstr} updated their jobs. check it now @manager"))
    await self.message.add_reaction("🔄")
    
    
  async def post_message(self):
    jobs_cb_msg= f"{self.log_text}{self.job_text}"
    self.content=jobs_cb_msg
    await self.message.edit(content=bl_q(jobs_cb_msg))
    print(bl_q(jobs_cb_msg))
    
  def analyze_info(self, content):
    self.usrstr= str(maybe(re.search(r"(?<=user:)\S+",content)).group(0))
    self.usrid= str(maybe(re.search(r"(?<=usr:)\d+",content)).group(0))
    self.job_id= str(maybe(re.search(r"(?<=id:)\d+",content)).group(0))

    mc=content.split("=#")
    if len(mc)<2 or self.usrstr == None or self.usrid == None or self.job_id == None:
      return False
    self.log_text = mc[0].replace("> ","")
    self.job_text = mc[1].replace("> ","")

    self.log_data['update_count']=int(maybe(re.search(r"(?<=update_count:)\d+",self.log_text)).group(0) or 0)
    rpat=re.findall(r"(review\d+(?=:)): (.+)\n",self.log_text)
    rls=rpat or []
    for v in rls:
      #group 1 definitly exist
      self.log_data[v[0]]=v[1].split("|")
    upat=re.findall(r"(update\d+(?=:)): (.+)\n",self.log_text)
    uls=upat or []
    for v in uls:
      #group 1 definitly exist
      self.log_data[v[0]]=v[1].split("|")
    dpat=re.findall(r"(\d\d-\d\d-\d\d\;.+(?=:)): (.+)\n",self.log_text)
    dls=dpat or []
    for v in dls:
      #group 1 definitly exist
      self.log_data[v[0]]=v[1]
      
    self.log_data['delete']=str(maybe(re.search(r"(?<=delete:).+\n",self.log_text)).group(0) or "-")
  
    
    
  def arrange_log(self):
    out=""
    
    out+=f"user:{self.usrstr} usr:{self.usrid} id:{self.job_id}\n"
    
    out+=self.text_ls+"\n"
    if self.log_data['update_count']:
      out+=f'update_count: {self.log_data["update_count"]}\n'
    for x in [(k,v) for k,v in self.log_data.items() if "review" in k]:
      out+=f"{x[0]}: {'|'.join(x[1])}\n"
  
    for x in [(k,v) for k,v in self.log_data.items() if re.search(r"update\d+",k)]:
      out+=f"{x[0]}: {'|'.join(x[1])}\n"
      
    if 'delete' in self.log_data.keys():
      if self.log_data['delete'] != "" and self.log_data['delete'] != "-" :
        out+='delete: '+self.log_data['delete']+"\n"
      
    out+=self.text_ls+"\n"
    for x in [(k,v) for k,v in self.log_data.items() if "-" in k]:
      out+=f"{x[0]}: {x[1]}\n"

    self.log_text=f"{self.text_lf_top}\n```{out}```\n{self.text_lf_bottom}\n"
    
  async def on_reaction_add(self,payload, eo):

    
    #print(int(self.usrid))
    #discord.utils.get(bot.get_guild(int(reaction.message.guild.id)).members,\
    # name="frog", discriminator="5827")
    #usr= await bot.fetch_user(int(usrid))
    print(payload.emoji.name)
    print("here goes...")
    if payload.emoji.name == "👍":
      self.message = await self.channel.fetch_message(self.message.id)
      
      for r in self.message.reactions:
        if r.emoji == "👎":
          await self.message.clear_reaction("👎")
      
      self.log_data[get_time_s()]=" review done. jobs added in to the database!"
      rl=len(re.findall(r"(?<=review)\d+:(.+\n)",self.log_text) or [])

      self.log_data[f'review{rl+1}']=[f"staff=<@!{payload.user_id}>",f"date={get_time()}","value=OK"]
      breako=False

      print("here goes...")

      print('reviewd...')
      for ls in self.listeners:
        await ls.on_reaction_add(payload, self)
      #raw=reaction.message.content.split("=#")
      data=ff.make_data(self.job_text)
      #raw[0]
      data["job_id"]=self.job_id 
      data["dicord_id"]=self.usrstr
      data["user"]=self.usrid
      data["manage"]=self.log_data
      if '_id' in data: 
        del data['_id'] 
      ppx = pp.PrettyPrinter(indent=4)
      ppx.pprint(data)
      reconnect(lambda: in_sett['job_coll'].update_one({"job_id":self.job_id}, {"$set":data},upsert=True))


      await self.message.add_reaction("☁")

            
          
    elif payload.emoji.name == "👎":
      self.message = await self.channel.fetch_message(self.message.id)
      for r in self.message.reactions:
        if r.emoji == "👍":
          await self.message.clear_reaction("👍")
      for ls in self.listeners:
        await ls.on_reaction_add(payload, self,value=0)
      rl=len(re.findall(r"(?<=review)\d+:(.+\n)",self.log_text) or [])

      self.log_data[f'review{rl+1}']=[f"staff=<@!{payload.user_id}>",f"date={get_time()}","value=BAD"]
              
              

      self.log_data[get_time_s()]=" i will tell user to edit their jobs message"
    else: return
      
    self.arrange_log()
    await self.post_message()
     
    