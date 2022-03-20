 import os
 import json
 import traceback
 import hmac
 import hashlib
 import requests
 from discord.ext import commands
 from discord.player import FFmpegPCMAudio
 from io import BytesIO
 
 bot = commands.Bot(command_prefix='!')
 TOKEN = os.environ['DISCORD_BOT_TOKEN']
 CF_KEY = os.environ['COEFONT_KEY']
 CF_SECRET = os.environ['COEFONT_SECRET']
 
 @bot.event
 async def on_command_error(ctx, error):
     orig_error = getattr(error, "original", error)
     error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
     await ctx.send(error_msg)
 
 
 @bot.command()
 async def ping(ctx):
     await ctx.send('pong')
 
 
 @bot.command(name='join')
 async def cmd_join(ctx):
     if ctx.message.guild:
         if ctx.author.voice is None:
             pass
         elif ctx.guild.voice_client:
             await ctx.guild.voice_client.move_to(ctx.author.voice.channel)
             await ctx.send('move vc')
         else:
             await ctx.author.voice.channel.connect()
             await ctx.send('join vc')
 
 
 @bot.command(name='dc')
 async def cmd_dc(ctx):
     if ctx.message.guild:
         if ctx.voice_client is None:
             pass
         else:
             await ctx.voice_client.disconnect()
 
 
 @bot.command(name='cf')
 async def cmd_coefont(ctx, *args):
 
     if len(args) <= 0:
         await ctx.send('入力文字数が不正です（1~100)')
         return
 
     arguments = ', '.join(args)
     if len(arguments) < 100:
         if ctx.message.guild.voice_client:
             coefontTTS(ctx, arguments)
     else:
         await ctx.send('入力文字数が不正です（1~100)')
 
 
 def coefontTTS(ctx, text):
     signature = hmac.new(bytes(CF_SECRET, 'utf-8'), text.encode('utf-8'), hashlib.sha256).hexdigest()
     url = 'https://api.coefont.cloud/text2speech'
     response = requests.post(url, data=json.dumps({
         'coefont': 'Averuni',
         'text': text,
         'accesskey': CF_KEY,
         'signature': signature
     }), headers={'Content-Type': 'application/json'})
 
     if response.status_code == 200:
         with open('tts.wav', 'wb') as f:
             f.write(response.content)
             ctx.guild.voice_client.play(FFmpegPCMAudio('tts.wav'))
 
 
 bot.run(TOKEN)
