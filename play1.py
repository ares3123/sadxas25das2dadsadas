import discord
from time import sleep
from sms import SendSms

TOKEN = "x"

gif = "https://media.tenor.com/SWiGXYOM8eMAAAAC/russia-soviet.gif"
saniye = 0
stop_bot = False  # Global variable to track whether the bot should stop

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('{} Çalışmaya Başladı!'.format(client.user))
    activity = discord.Activity(type=discord.ActivityType.playing, name="https://gitlab.com/tingirifistik/enough/")
    await client.change_presence(activity=activity)
    
@client.event
async def on_message(message):
    global stop_bot  # Declare the global variable
    
    if message.author == client.user:
        return

    if len(message.content.split(" ")) == 3 and message.content.split(" ")[0] == "!sms":
        telno = message.content.split(" ")[1]
        adet = int(message.content.split(" ")[2])  # Convert adet to an integer
        if len(telno) == 10:
            embed=discord.Embed(title="SMS Bomber (+90)", description=(f"{adet} adet SMS Gönderiliyor --> {telno}\n{message.author.mention}"), color=0x001eff)
            embed.set_thumbnail(url=gif)
            await message.channel.send(embed=embed)
            sms = SendSms(telno, "")
            while sms.adet < adet and not stop_bot:  # Check if the stop_bot flag is False
                for attribute in dir(SendSms):
                    attribute_value = getattr(SendSms, attribute)
                    if callable(attribute_value):
                        if attribute.startswith('__') == False:
                            if sms.adet == adet or stop_bot:  # Check if the stop_bot flag is True
                                break
                            exec("sms."+attribute+"()")
                            sleep(saniye)
            await message.channel.send(telno+" --> "+str(sms.adet)+f" adet SMS gönderildi.\n{message.author.mention}")                        
        else:
            await message.channel.send(f"Geçerli komut yazınız!\nYardım için '!help' yazınız.\n{message.author.mention}")
    elif "!help" == message.content:
        await message.channel.send(f"Sms göndermek için komutu aşağıdaki gibi yazınız.\n```!sms 5051234567 10```\n!sms (telefon numarası) (adet)\n{message.author.mention}")
    elif "!stop" == message.content:
        await message.channel.send("Bot durduruldu.")
        stop_bot = True  # Set the stop_bot flag to True to stop the bot
    else:
        pass
  
client.run(TOKEN)
