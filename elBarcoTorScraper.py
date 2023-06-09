#import asyncio
import sys
#import io
from bs4 import BeautifulSoup
from torpy.http.requests import TorRequests


#sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='latin1')


def scraper():
    grab = None
    lista = ""
    #global contenido
    print('elBarcoTorScraper : INFO : stay in tune...', flush=True)

# TODO set a count loop
    while grab is None:
        try:
            with TorRequests() as tor_requests:
                with tor_requests.get_session() as sess:
                    grab = sess.get("https://elcano.top")
                    print(grab)
        except:
            print("elBarcoTorScraper : ERROR : line 25")
            sys.exit(1)

    soup = BeautifulSoup(grab.text, 'html.parser')
    for enlace in soup.find_all('a'):
        acelink = enlace.get('href')
        canal = enlace.text
        if not str(acelink).startswith("acestream://") or canal == "aquÃ­":
            pass
        else:
            link = str(acelink).replace("acestream://", "")
            lista += str((canal + "\n" + link + "\n"))

    # No esta claro que haya que hacer este replace porque la lista ya se escribe con espacios
    contenido = ((lista.replace(u'\xa0', u' ')).strip())

    if contenido != "":
        #print(contenido, flush=True)
        print("elBarcoTorScraper : OK : channels retrieved")
    else:
        print("elBarcoTorScraper : ERROR : channels could not be retrieved")
        #scraper()
        sys.exit(1)


    # TODO rewrite this extremely unelegant latin1 encoding
    #contenido1 = contenido.replace('Ã§', 'ç', 1)
    #contenido2 = contenido1.replace('Ã±', 'ñ')
    #contenido_lat = contenido2.replace('Ã³', 'ó')

    #with open('/Users/Jorge/Documents/AcestreamScraper/AceTorScraper/github/canales.txt', "wb") as f:
    #    f.write(contenido_lat)

    return contenido

#scraper()
