import asyncio
import io
import datetime
import urllib
import urllib.request
import aiohttp
import re
import html

url_pobre = "http://romhackers.org/search.php?query={0}&mid={1}&action=showall&andor=AND&start={2}"

# Constants
network_retry_delay = 0.5
ERROR_NETWORK = 0
ERROR_DOESNTEXIST = 1
ERROR_NOTINDATABASE = 2

def get_search(name,mid,pagenum,tries=5):
    """Returns a dictionary containing search results, if exact match was found, it returns details of the search item."""

    url = url_pobre.format(name,mid,pagenum)
    # Fetch website
    try:
        page = yield from aiohttp.get(url)
        content = yield from page.text(encoding='ISO-8859-1')
    except Exception:
        if tries == 0:
            log.error("get_search: Couldn't fetch {0}, page {1}, network error.".format(name,pagenum))
            return ERROR_NETWORK
        else:
            tries -= 1
            yield from asyncio.sleep(network_retry_delay)
            ret = yield from get_search(name,mid,pagenum,tries)
            return ret 

    # Trimming content to reduce load
    try:
        start_index = content.index('<body>')
        end_index = content.index('</body>')
        content = content[start_index:end_index]
    except ValueError:
        # Website fetch was incomplete, due to a network error
        if tries == 0:
            log.error("get_search: Couldn't fetch {0}, page {1}, network error.".format(name,pagenum))
            return ERROR_NETWORK
        else:
            tries -= 1
            yield from asyncio.sleep(network_retry_delay)
            ret = yield from get_search(name,mid,pagenum,tries)
            return ret
    
    regex_deaths = r"<a href='([^<]+)'>([^<]+)</a></b><br />[^<]+<small>[^<]+<a href='([^<]+)'>([^<]+)</a>([^<]+)</small><br />"
    pattern = re.compile(regex_deaths, re.MULTILINE + re.S)
    matches = re.findall(pattern, content)
    searchList = []
    for m in matches:
        details = []
        if len(matches) == 1:
            details = yield from get_details('http://romhackers.org/' + m[0],mid)

        searchList.append({'link': 'http://romhackers.org/' + m[0], 'name': html.unescape(m[1]), 'user_link': m[2], 'user': m[3], 'date': m[4].replace('\n', '').replace(')','').replace('(',''), 'details': details})                                    
    if (searchList == []):
        searchList = None

    #print(searchList)
    return searchList     

def get_details(url,mid,tries=5):
    # Fetch website
    try:
        page = yield from aiohttp.get(url)
        content = yield from page.text(encoding='ISO-8859-1')
        print(content)
    except Exception:
        if tries == 0:
            log.error("get_details: Couldn't fetch the url {0} network error.".format(url))
            return ERROR_NETWORK
        else:
            tries -= 1
            yield from asyncio.sleep(network_retry_delay)
            ret = yield from get_details(name,mid,tries)
            return ret 

    # Trimming content to reduce load
    try:
        start_index = content.index('<body>')
        end_index = content.index('</body>')
        content = content[start_index:end_index]
    except ValueError:
        # Website fetch was incomplete, due to a network error
        if tries == 0:
            log.error("get_details: Couldn't fetch the url {0} network error.".format(url))
            return ERROR_NETWORK
        else:
            tries -= 1
            yield from asyncio.sleep(network_retry_delay)
            ret = yield from get_details(name,mid,tries)
            return ret
    
    details = dict()

    if mid == "26": # 26 - detalhes de um utilitário
        # Verifica se existe
        if "<b>Nome" not in content:
            return ERROR_DOESNTEXIST
        
        # Nome
        m = re.search(r'Nome</b>:[ ]*([^<]+).*', content)
        if m:
            char['nome'] = m.group(1).strip()

        # Autor
        m = re.search(r'Autor</b>:[ ]*([^<]+).*', content)
        if m:
            char['autor'] = m.group(1).strip()

        # Grupo
        m = re.search(r'Grupo</b>:[ ]*([^<]+).*', content)
        if m:
            char['grupo'] = m.group(1).strip()

        # Site
        m = re.search(r'Site</b>:[^<]+<a href="([^<]+)" target="_blank">', content)
        if m:
            char['site'] = m.group(1).strip()

        # Categoria
        m = re.search(r'Categoria</b>:[ ]*([^<]+).*', content)
        if m:
            char['categoria'] = m.group(1).strip()

        # Sistema
        m = re.search(r'Sistema</b>:[ ]*([^<]+).*', content)
        if m:
            char['sistema'] = m.group(1).strip()

        # Versão
        m = re.search(r'Versão</b>:[ ]*([^<]+).*', content)
        if m:
            char['versao'] = m.group(1).strip()

        # Lançamento
        m = re.search(r'Lançamento</b>:[ ]*([^<]+).*', content)
        if m:
            char['lancamento'] = m.group(1).strip()

        # Idioma
        m = re.search(r'Idioma</b>:[ ]*([^<]+).*', content)
        if m:
            char['idioma'] = m.group(1).strip()

        # Plataforma
        m = re.search(r'Plataforma</b>:[ ]*([^<]+).*', content)
        if m:
            char['plataforma'] = m.group(1).strip()

        # Descrição
        m = re.search(r'[\s\S.]*<b>DESCRIÇÃO:[\s\S.]*(?=<div class="even">)<div[^<]+>(.+).*(?=</div>)', content)
        if m:
            char['descricao'] = m.group(1).strip()

        # Download
        m = re.search(r'<a href="([^"]+)(?=.*DOWNLOAD)', content)
        if m:
            char['download'] = 'http://romhackers.org/modules/PDdownloads2/' + m.group(1).strip()

        '''regex_deaths = r'<b>Nome</b>:[ ]*([^<]+).*<b>Autor</b>:[ ]*([^<]+).*<b>Grupo</b>:[ ]*([^<]+).*<b>Site</b>:[^<]+<a href="([^<]+)" target="_blank">[^<]+</a>.*<b>Categoria</b>:[ ]*([^<]+).*<b>Sistema</b>:[ ]*([^<]+).*<b>Versão</b>:[ ]*([^<]+).*<b>Lançamento</b>:[ ]*([^<]+).*<b>Idioma</b>:[ ]*([^<]+).*<b>Plataforma</b>:[ ]*([^<]+)</div>[\s\S.]*<b>DESCRIÇÃO:[\s\S.]*(?=<div class="even">)<div[^<]+>(.+).*(?=</div>)'
        pattern = re.compile(regex_deaths, re.MULTILINE + re.S)
        matches = re.findall(pattern, content)
        
        for m in matches:
            details.append({'nome': html.unescape(m[0]), 'autor': html.unescape(m[1]), 'grupo': html.unescape(m[2]), 'site': m[3], 'categoria': html.unescape(m[4]), 'sistema': html.unescape(m[5]), 'versao': html.unescape(m[6]), 'lancamento': html.unescape(m[7]), 'idioma': html.unescape(m[8]), 'plataforma': html.unescape(m[9])})
        if (details == []):
            details = None
        else:
            details = details[0]'''
    
    return details         

loop = asyncio.get_event_loop()
# Blocking call which returns when the hello_world() coroutine is done
loop.run_until_complete(get_search('mario+64+level','26','0'))
loop.close()