from discord.ext import commands, tasks
import discord 
from initialize import bot, in_sett
from helper import bl_q

class JobBoards(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		
	@commands.Cog.listener()
	async def on_guild_join(self, member):
		 pass

	@commands.command()
	async def show(self, ctx):
	   """shows jobs board manually"""
	   in_sett['job_coll']
	   
	@commands.command()
	async def pin(self, ctx, channel="job boards", interval=24,start_at=1, ):
		"""pin message on specified channel and create task to make it show info in specified
		interval"""
		if not self.bot.check_channel(ctx.channel, channel):return True
	
		in_sett.update_setting('JobBoard',{'channel':channel})
		await ctx.channel.send(content=b_q(f"""just created from bot in channel{channel}
			is pinned. and will be updated regularly each {interval}"""))
		self.start_jobs_board_loop.change_interval(start_at)
		self.update_jobs_board.change_interval(hours=interval)
		self.start_jobs_board_loop.start()

	@tasks.loop(seconds=1)
	async def start_jobs_board_loop(self):
		self.update_jobs_board.start()
		self.start_jobs_board_loop.stop()

	@tasks.loop(hours=24)
	async def update_jobs_board(self):

		print(self.index)
		self.index += 1

@bot.event
async def on_ready():
	await bot.add_cog(JobBoards(bot))