import aiohttp
from colorama import Fore, init
import asyncio
from configparser import ConfigParser

config = ConfigParser()
title = f'''
{Fore.CYAN}┌───────────────────────────────────────────┐
{Fore.CYAN}│    ____  __               __              │
{Fore.CYAN}│   / __ \/ /_  ____  ___  / /_  __  _______│
{Fore.CYAN}│  / /_/ / __ \/ __ \/ _ \/ __ \/ / / / ___/│
{Fore.CYAN}│ / ____/ / / / /_/ /  __/ /_/ / /_/ (__  ) │
{Fore.CYAN}│/_/   /_/ /_/\____/\___/_.___/\__,_/____/  │
{Fore.CYAN}│                                           │
{Fore.CYAN}└─────────────────────────────nina🪴#6666───┘'''
print(title)

def loadconfig():
    global bearer, refresh, headers
    config.read('config.ini')
    bearer = config['Account']['bearer']
    refresh = config['Account']['refresh_token']
    headers={"Content-type": "application/json", "Authorization": "Bearer " + bearer}

async def bearercheck(bearer, refresh, headers):
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post("https://api.minecraftservices.com/minecraft/profile") as response:
            if response.status == 400:
                print(f'{Fore.GREEN}[Success] {response.status} {Fore.RESET}| Bearer is valid')
            else:
                async with session.post(f"https://api.gosnipe.tech/api/refresh?code={refresh}") as r:
                    res = r.json()
                    bearer = (await res)['access_token']
                    config.set('Account', 'bearer', bearer)
                    with open('config.ini', 'w') as cfg:
                        config.write(cfg)
                    print(f'{Fore.GREEN}[Success] {r.status} {Fore.RESET}| Updated bearer')

if __name__ == "__main__":
    loadconfig()
    results = asyncio.run(bearercheck(bearer, refresh, headers))