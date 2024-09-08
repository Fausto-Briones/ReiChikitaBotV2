import discord
import openai
import os
import asyncio
from discord.ext import commands

openai.api_key = os.getenv("OPEN_AI_KEY")
DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
#client = discord.Client(intents=intents)
intents.message_content = True 
bot = commands.Bot(command_prefix='!',intents=intents)

async def generateTask(task_description):
    prompt = f"Split the following task into detailed steps: {task_description}"
    
    try:
        response = openai.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=200,
            n=1,
            stop=None,
            temperature=0.7
        )
        steps=response.choices[0].text.strip()
        return steps
    except Exception as e:
        print(f"Error in OpenAI API call: {e}")
        return "Sorry, I couldn't generate the task steps."    
    

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

@bot.command(name="task")
async def task(ctx, *, task_description: str = None):
    if task_description is None:
        await ctx.send("Please provide a task description after the `!task` command.")
    else:
        # Generate task steps and send the response
        steps = await generateTask(task_description)
        await ctx.send(f"Here are the steps to accomplish your task:\n{steps}")
        
        # Add a small delay to prevent rapid API calls
        await asyncio.sleep(1)  # Helps prevent rate limiting
# Run the bot
bot.run(DISCORD_TOKEN)
