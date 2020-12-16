import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()



sad_words = ['angry','sad','depressed','unhappy','miserable']



encouragements = [
  "Cheer Up ",
  "Hang in there ",
  "You are an amazing person "
]



if 'responding' not in db.keys():
  db['responding'] = True



def update_quotes(newquote):
  if 'quotes' in db.keys():
    quotes = db['quotes']
    quotes.append(newquote)
    db['quotes'] = quotes
  else:
    db["quotes"] = [newquote]



def delete_quote(index):
  quotes = db['quotes']
  if len(quotes) > index:
    del quotes[index]
    db['quotes'] = quotes



def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " - " + json_data[0]['a']
  return quote 



@client.event
async def on_ready():
  print(f"Logged in as {client.user}")



@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if msg.startswith("$hello"):
    await message.channel.send("Hello!")
  
  if msg.startswith("$inspire"):
    quote = get_quote()
    await message.channel.send(quote)
  
  
  
  if db['responding']:

    options = encouragements
    if 'quotes' in db.keys():
      options  +=  db['quotes'] 
    else:
      options = encouragements

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options)+' ' +  str(message.author.name))



  if msg.startswith("$new"):
    newquote = msg.split("$new ",1)[1]
    update_quotes(newquote)
    await message.channel.send("New encouragement message added...")



  if msg.startswith("$del"):
    quotes = []
    if 'quotes' in db.keys():
      index  = int(msg.split("$del",1)[1])
      delete_quote(index) 
      quotes = db['quotes']
    await message.channel.send(quotes)



  if msg.startswith("$list"):
    quotes = []
    if 'quotes' in db.keys():
      quotes = db['quotes']
    await message.channel.send(quotes)

  

  if msg.startswith("$responding"):
    value = msg.split("$responding ",1)[1]

    if value.lower() == "true":
      db['responding'] = True
      await message.channel.send("Responding is on...")
    else:
      db['responding'] = False
      await message.channel.send("Bot gonna take a nap..")


keep_alive()
client.run(os.getenv('TOKEN'))
