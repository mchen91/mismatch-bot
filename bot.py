import discord
import os


client = discord.Client()

@client.event
async def on_ready():
    print("Bot is ready")


@client.event
async def on_message(msg):
    if msg.author.bot:
        return
    await msg.channel.send(f"hello {msg.author.id}: ur msg: {msg.content}")


client.run(os.environ["DISCORD_TOKEN"])
