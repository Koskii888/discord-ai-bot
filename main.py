import discord
import requests
import os

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
HF_TOKEN = os.getenv("HF_TOKEN")
MODEL = "mistralai/Mistral-7B-v0.1"

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

def query(prompt):
    r = requests.post(
        f"https://api-inference.huggingface.co/models/{MODEL}",
        headers={"Authorization": f"Bearer {HF_TOKEN}"},
        json={"inputs": prompt}
    )
    return r.json()[0]["generated_text"]

@client.event
async def on_ready():
    print(f"Bot online jako {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith("!ai"):
        prompt = message.content.replace("!ai", "")
        await message.channel.send("🤖 Myślę...")
        reply = query(prompt)
        await message.channel.send(reply)

client.run(DISCORD_TOKEN)
