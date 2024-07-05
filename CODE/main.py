import discord
from discord.ext import commands
import os
import requests

intents = discord.Intents.all()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix='+', intents=intents)

def sanitize_filename_for_naz_api(filename):
    invalid_chars = set('\\/:*?"<>|')
    return ''.join('_' if char in invalid_chars else char for char in filename)

@bot.command()
async def search(ctx, *, request_id):

    if ctx.channel.id != 1257811657254764566:
        await ctx.send("❌ → https://discord.com/channels/1216428655744389271/1216429441593511988/1216436164416765983")
        return
    
    if not request_id:
        await ctx.reply("## > 🌐 `+search` - Pour rechercher votre Query.\n## > Usage: `+search demande`")
        return
    
    blacklist = ["lukas siadyan", "xekoo", "mot3"]
    if any(word in request_id.lower() for word in blacklist):
        await ctx.reply("## > ❌ Blackliste.")
        return
    
    print(f"Received command: +search {request_id}")
                
    naz_search = request_id
    sanitized_filename_for_naz_api = sanitize_filename_for_naz_api(naz_search)

    download_path = "./resultat/"
    filename = f"{sanitized_filename_for_naz_api}.txt"
    file_path = download_path + filename

    if not os.path.exists(download_path):
        os.makedirs(download_path)
    
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            await ctx.reply(f"⭐ {request_id}:", file=discord.File(file))

    else:
        data = {"token": "1501479747:EOHy2kbG", "request": f"{naz_search}", "limit": 75, "lang": "fr"}
        url = 'https://server.leakosint.com/'
        response = requests.post(url, json=data)

        response_json = response.json()
        if "List" not in response_json:
            await ctx.reply("❌ Aucun résultat trouvé !")
            return

        list_data = response_json["List"]

        logo_texte = requests.get("https://gist.githubusercontent.com/septxrdp/c38dcdaa7c3f4ccaa3d8d5560b896908/raw/gistfile1.txt").text

        with open(os.path.join(download_path, filename), "wb") as file:
            file.write(logo_texte.encode('utf-8') + b"\n\n")

            for category, category_data in list_data.items():
                file.write(f"✩———————✭ Category / categorie : {category} ✭———————✩\n".encode('utf-8'))

                if "Data" not in category_data or not category_data["Data"]:
                    await ctx.reply("❌ Aucun résultat trouvé !")
                    return

                for data_item in category_data["Data"]:
                    if isinstance(data_item, dict):
                        for key, value in data_item.items():
                            file.write(f"{key}: {value}\n".encode('utf-8'))
                    else:
                        await ctx.reply("❌ Aucun résultat trouvé !")
                        break

                file.write(b"\n")

        with open(file_path, 'rb') as file:
            await ctx.reply(f"⭐ {request_id}:", file=discord.File(file))

bot.run('TOKEN')
