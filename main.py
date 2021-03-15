from discord.ext import commands
import discord
import string
import configparser
import random
import string


default_intents = discord.Intents.default()
default_intents.members = True
bot = discord.Client(intents=default_intents)


@bot.event
async def on_ready():
	print(f'Bot connected as {bot.user}')

@bot.event
async def on_member_join(member):
    config = configparser.ConfigParser()
    mot = ""
    for w in range(7):
        mot = mot + random.choice(string.hexdigits)
     
    config[member.name] = {}
    config[member.name]["CODE"] = mot
    with open('confg.ini','a') as confile:
        config.write(confile)
        confile.write("\n")

    await member.send(f"Bienvenue sur le serveur {member.display_name} ! Pour être vérifié et utiliser le serveur, tu dois utiliser la commande '$VALID {mot}' sur ce salon: https://discord.com/channels/820735041411088454/820754157082378281.")

@bot.event
async def on_message(message):
    auth = message.author
    print(message)
    if message.content.startswith("$sneak"):
        await message.author.send("Alors, tu veux des chaussures ?\nEnvoie '*start' pour commencer.")
    
    if message.content.startswith("*"):
        if message.channel.__class__.__name__ == "DMChannel":
            if message.content.startswith("*start"):
                conf = configparser.ConfigParser()
                conf[str(auth.name)]["START"] = True
                embed = discord.Embed(title="Processus de commande.",colour=discord.Colour(0x3e039c))
                embed.add_field(name=f"Étape 1:",value="Envoyez '*pre', suivi de votre prénom pour l'enregistrer.",inline=False)
                embed.add_field(name=f"Étape 2:",value="Envoyez '*nom', suivi de votre nom pour l'enregistrer.",inline=False)
                embed.add_field(name=f"Étape 3:",value="Envoyez '*adr1', suivi de votre adresse de livraison 1 pour l'enregistrer.",inline=False)
                embed.add_field(name=f"Étape 4:",value="Envoyez '*adr2', suivi de votre adresse de livraison 2 pour l'enregistrer.",inline=False)
                embed.add_field(name=f"Étape 5:",value="Envoyez '*land', suivi de votre pays pour l'enregistrer.",inline=False)
                embed.add_field(name=f"Étape 6:",value="Envoyez '*zip', suivi de votre code postal pour l'enregistrer.",inline=False)
                embed.add_field(name=f"Déroulement:",value="Vous serrez prier d'envoyer vos informations une fois que je vous l'aurrai demandé.",inline=False)
                with open("confg.ini","a") as confile:
                    conf.write(confile)
                await message.channel.send(embed=embed)

        else:
            await message.channel.send("Seulement disponible en DM")
    
    if message.content.startswith("$VALID"):
        conf = configparser.ConfigParser()
        conf.read("confg.ini")
        param = message.content.split()[1]
        if str(auth.name) in conf.sections():
            if str(conf[auth.name]["CODE"]) == param:
                var = discord.utils.get(message.guild.roles, name = "Verif")
                await auth.add_roles(var)
                await message.channel.send("C'est bon, amuse toi bien.")
            else:
                await message.channel.send("Mauvais code.")
        else:
            await message.channel.send("Tu ne dois pas utiliser cette commande.")
    
    if message.content.startswith("$infos"):
        await message.channel.send("En cours...")

    if message.content.startswith("$help"):
        try:
            param = message.content.split()[1]
        except:
            embed = discord.Embed(title="Aide général (commandes):", colour=discord.Colour(0x3e038c))

            embed.add_field(name=f"$sneak:", value=f"Vous permet d'engager la conversation avec {bot.user} pour lui demander de fonctionner. Le procéssus est détaillé en DM.", inline=False)
            embed.add_field(name=f"$help:", value="Active cette command d'aide.", inline=False)
            embed.add_field(name=f"Voir plus:", value="Faites '$help' plus la commande sur laquelle vous souhaitez des renseignements.", inline=False)
            await message.channel.send(embed=embed)
    
    else:
        if message.channel.id == 820754647873617938:
            await message.delete()
    


bot.run("ODIwNzMzODgyNzY3OTAwNjkz.YE5d_g.qSGdfM5mFnUnbPRSak4DF8t3LcU")