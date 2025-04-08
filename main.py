import discord
import os

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.dm_messages = True

client = discord.Client(intents=intents)

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
TARGET_CHANNEL_ID = int(os.getenv("TARGET_CHANNEL_ID"))  # replace with your channel ID if not using Railway env vars

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.guild is not None:
        return  # Ignore messages not in DMs

    if message.author == client.user:
        return

    if not message.content.lower().startswith("!submit"):
        await message.channel.send("To submit, use `!submit RiotID#TAG` and attach your clip.")
        return

    if not message.attachments:
        await message.channel.send("Please attach an image or video with your submission.")
        return

    riot_id = message.content[7:].strip()

    if not riot_id or "#" not in riot_id:
        await message.channel.send("Please include your Riot ID in the format `RiotID#1234`.")
        return

    try:
        channel = client.get_channel(TARGET_CHANNEL_ID)

        files = [await a.to_file() for a in message.attachments]

        await channel.send(
            content=f"🎁 **Anonymous Night Market Submission** 🎁\n🧑 Riot ID: `{riot_id}`\n📎 Clip below:",
            files=files
        )

        await message.channel.send("✅ Submission sent anonymously. Good luck!")
    except Exception as e:
        print(f"Error sending message: {e}")
        await message.channel.send("Something went wrong while sending your submission. Try again later.")

client.run(TOKEN)
