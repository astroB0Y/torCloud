from git import Repo
import utils as u
import re
from elBarcoTorScraper import *
import asyncio
import os
#from telethon.sync import TelegramClient
#from telethon import TelegramClient
#from telethon.tl.types import PeerChannel


'''
try:
    SOME_SECRET = os.environ["SOME_SECRET"]
except KeyError:
    SOME_SECRET = "Token not available!"
    #logger.info("Token not available!")
    #raise
'''


def main():
    asyncio.run(export_messages())
    
    
#api_id = 18062170
#api_hash = '9a97fd9dc96e745d5b8869966e21ace7'
#peer_channel_id = -1727304456

async def export_messages(export_file = "tags.txt"):

    #async with TelegramClient('jgutierrezperez', api_id, api_hash) as client:
        #channel_name = await client.get_entity(PeerChannel(peer_channel_id))

        channel_dict = dict()  # {channel_id: channel_name}

        try:
            contenido_elBarco = scraper()
            cleansed_content = cleanse_message(contenido_elBarco)
            # comment out bottom 2 lines and uncomment line below to block elBarco
            # cleansed_content = ""
            #async for message in client.iter_messages(channel_name, limit=4):
                # limit=x sets how many msgs in telegram are retreived
                #message_content = message.message
                #if message_content is not None:
                    #cleansed_content += cleanse_message(message_content)
                    #if cleansed_content:
            channel_dict = update_channel_dict(cleansed_content, channel_dict)
        except Exception as e:
            print("elBarcoTorMain : ERROR :", e)
            sys.exit(1)

        #print("elBarcoTorMain : INFO : messages retrieved from Telegram")

        export_channels(channel_dict, export_file)

        print("elBarcoTorMain : INFO : list exported to local file")
    
  
def cleanse_message(message_content):
    cleansed_content = ""
    rows = [row for row in message_content.split("\n") if len(row.strip()) > 0]
    channel_id_regex = r'[a-zA-Z0-9]{40}'
    if re.search(channel_id_regex, message_content):
        for i, row in enumerate(rows):
            if re.search(channel_id_regex, row):
                if i > 0:
                  cleansed_content += rows[i-1] + "\n" + row + "\n"
                else:
                  cleansed_content += "UNTITLED CHANNEL" + "\n" + row + "\n"
    return cleansed_content


def update_channel_dict(message_content, channel_dict):
    rows = message_content.split("\n")
    for i, row in enumerate(rows):
        if i % 2 == 1:
            channel_id = row
            channel_name = rows[i-1]
            if "DAZN F1 1080" in channel_name:
                channel_name = "DAZN F1 1080"
            elif "DAZN F1 720" in channel_name:
                channel_name = "DAZN F1 720"
            elif "SmartBanck" in channel_name:
                channel_name = channel_name.replace("SmartBanck", "Smartbank")
            elif "La1" in channel_name:
                channel_name = channel_name.replace("La1", "La 1")
            elif "LA 1" in channel_name:
                channel_name = channel_name.replace("LA 1", "La 1")
            elif "Tv" in channel_name:
                channel_name = channel_name.replace("Tv", "TV")
            elif "#0 de Movistar" in channel_name:
                channel_name = channel_name.replace("#0 de Movistar", "#0 M+ HD")
            #elif "BarÃ§a" in channel_name:
                #channel_name = channel_name.replace("BarÃ§a", "Barça")

            channel_dict[channel_id] = channel_name
    return channel_dict


def export_channels(channel_dict, export_file):

    channel_list = []

    for channel_id, channel_name in channel_dict.items():
        group_title = u.extract_group_title(channel_name)
        tvg_id = u.extract_tvg_id(channel_name)
        logo = u.get_logo(tvg_id)
        identif = (channel_id[0:4])
        channel_info = {"group_title": group_title,
                        "tvg_id": tvg_id,
                        "logo": logo,
                        "channel_id": channel_id,
                        "channel_name": channel_name + "  " + identif}
        channel_list.append(channel_info)

    all_channels = ""
    # all_channels += '#EXTM3U url-tvg="https://raw.githubusercontent.com/dracohe/CARLOS/master/guide_IPTV.xml"\n'
    all_channels += '#EXTM3U url-tvg="https://raw.githubusercontent.com/davidmuma/EPG_dobleM/master/guia.xml, https://raw.githubusercontent.com/acidjesuz/EPG/master/guide.xml"\n'

    channel_pattern = '#EXTINF:-1 group-title="GROUPTITLE" tvg-id="TVGID" tvg-logo="LOGO" ,CHANNELTITLE\nacestream://CHANNELID\n'
    #channel_pattern = '#EXTINF:-1 group-title="GROUPTITLE" tvg-id="TVGID" tvg-logo="LOGO" ,CHANNELTITLE\nhttp://127.0.0.1:6878/ace/getstream?id=CHANNELID\n'

    for group_title in u.group_title_order:
        for channel_info in channel_list:
            if channel_info["group_title"] == group_title:
                all_channels += channel_pattern.replace("GROUPTITLE", channel_info["group_title"]) \
                                               .replace("TVGID", channel_info["tvg_id"]) \
                                               .replace("LOGO", channel_info["logo"]) \
                                               .replace("CHANNELID", channel_info["channel_id"]) \
                                               .replace("CHANNELTITLE", channel_info["channel_name"])


    #with open(export_file, "wb") as f:
        #f.write(all_channels.encode("latin1"))
    with open(export_file, "wb") as f:
        f.write(all_channels.encode("utf-8")
    
 
# ÉSTA PARTE PERTENECE AL SCRIPT ORIGINAL. AQUÍ COMMIT Y PUSH SE HACEN DESDE actions.yml
'''
def gitUpdate():
    gitRepo = r'/Users/Jorge/Documents/AcestreamScraper/AceTorScraper/github'
    commitMessage = 'tags updated'

    try:
        repo = Repo(gitRepo)
        repo.git.add(update=True)
        repo.index.commit(commitMessage)
        origin = repo.remote(name='origin')
        origin.push()

        print("updating_github : INFO : list updated to github")
    except:
        print("updating_github : ERROR : some error occured while pushing the code")
'''


if __name__ == "__main__":
    main()
    #gitUpdate()
