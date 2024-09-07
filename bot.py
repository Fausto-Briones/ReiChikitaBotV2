import discord
import openai
import os

openai.api_key = os.getenv("OPEN_AI_KEY")
DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
client = discord.Client(intents=intents)

async def generateTask(task_description):
    prompt = f"Split the following task into detailed steps: {task_description}"
    
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

@client.event
async def on_message(message):
    print(f'Logged in as {client.user}!')

@client.event
async def on_message(message):
    # Prevent the bot from replying to itself
    if message.author == client.user:
        return

    # If the message starts with "!task", the bot splits the task into steps
    if message.content.startswith("!task"):
        task_description = message.content[len("!task "):].strip()
        if task_description:
            # Generate steps for the task
            steps = await generateTask(task_description)
            await message.channel.send(f"Here are the steps to accomplish your task:\n{steps}")
        else:
            await message.channel.send("Please provide a task description after the command.")

# Run the bot
client.run(DISCORD_TOKEN)
