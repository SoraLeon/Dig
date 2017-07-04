import asyncio
import datetime
import urllib
import urllib.request

async def hello_world():
    #u(string, safe='/', encoding=None, errors=None)
    image = urllib.parse.quote('http://www.romhackers.org/imagens/traducoes/[SNES] Super Mario World - Samus - 2.png', safe='/:[]()-.!@#$%&*~^´`{}?;><\\|\'')
    print(image)
    #image = 'http://www.romhackers.org/imagens/traducoes/[SNES]%20Super%20Mario%20World%20-%20Samus%20-%202.png'
    data = urllib.request.urlopen(image)
    print(data)

loop = asyncio.get_event_loop()
# Blocking call which returns when the hello_world() coroutine is done
loop.run_until_complete(hello_world())
loop.close()