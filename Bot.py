#importing libraries (ensure you have these installed using pip, dontenv pip library name is python-dotenv)
from getpass import getuser
import json
import discord
import os
from happytransformer import HappyGeneration
from happytransformer import GENSettings

from dotenv import load_dotenv
#load in the token keys from the .env file
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
#load in AI parameters
DEFAULT_PERSONALITY_TYPE = os.getenv("DEFAULT_PERSONALITY_TYPE")
MODEL_TYPE = os.getenv("MODEL_TYPE")
MODEL_NAME = os.getenv("MODEL_NAME")
MAX_TOKENS = int(os.getenv("MAX_TOKENS"))
#load in HappyGeneration model
happy_gen = HappyGeneration(model_name=MODEL_NAME,model_type=MODEL_TYPE)
beam_settings = GENSettings(num_beams=5,  max_length=10)

client = discord.Client()

prompt_arr = []
    
def getResponce(prompt, userID):
    output_beam_search = happy_gen.generate_text(prompt)
    prompt_arr.append(output_beam_search.text)
    return output_beam_search.text

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    #formating the message into the GPT input
    prompt = '\n[Human]: ' + message.content + "\n[AI]: "
    prompt_arr.append(prompt)

    if len(prompt_arr) > 3:
        prompt_arr.pop(0)
    input = ' '.join(prompt_arr)

    

    messageOutput = getResponce(DEFAULT_PERSONALITY_TYPE + input,message.author.id)
    print(DEFAULT_PERSONALITY_TYPE + input)
    await message.channel.send(messageOutput)

client.run(DISCORD_TOKEN)

 