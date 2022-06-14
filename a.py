class AutoMessage:
  async def on_ready(self, payload):pass
  async def on_message_edit(self, payload):pass
  async def on_reaction_add(self, payload):pass
  async def on_message_delete(self,payload):pass
  async def on_create(self, payload):pass

"""
a collection of object.
mr = message_review
mj = message_job
ch = channel
br = bot_reply

mr is a message send by bot when user post new job in review channel.
mj is a message send by user in channel job.
br is a message send by bot to reply job message from user in channel job.
for detail please see to the corespond py file
"""
mr_pools={}
mj_pools={}
br_pools={}
ch_pools={}