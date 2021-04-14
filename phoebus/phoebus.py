import requests
import aiohttp
import time
from colorama import Fore, init
import os
from datetime import datetime
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

skin = "https://www.minecraft.net/profile/skin/remote?url=https://www.minecraftskins.com/uploads/skins/2021/04/09/-all-the-good-girls-go-to-hell--17409322.png?v389"

def info():
    global name, offset, bearer
    name = input(f"What name should I target: {Fore.RESET}")
    offset = int(input(f"{Fore.CYAN}What offset should I use (in ms): {Fore.RESET}"))
    config.read('config.ini')
    bearer = config['Account']['bearer']

def nametiming(name):
    global droptime
    droptime = requests.get(f"https://api.kqzz.me/api/namemc/droptime/{name}")
    droptime = droptime.json()
    if droptime['droptime']:
        print(f"Sending requests for {name} @ {datetime.fromtimestamp(droptime['droptime'])}")

async def request(name, bearer):
    now = time.time()
    headers={"Content-type": "application/json", "Authorization": "Bearer " + bearer}
    json={"profileName": name}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post("https://api.minecraftservices.com/minecraft/profile", json=json) as response:
            if response.status == 403:
                print(f'{Fore.RED}[Fail] {response.status} {Fore.RESET}| Sent @ {datetime.fromtimestamp(now)}, Recieved @ {datetime.fromtimestamp(time.time())}')
            elif response.status == 200 or response.status == 204:
                print(f'{Fore.GREEN}[Success] {response.status} {Fore.RESET}| Sent @ {datetime.fromtimestamp(now)}, Recieved @ {datetime.fromtimestamp(time.time())}')
                payload = {"variant": "slim"}
                async with session.post(skin, headers=headers, data=payload) as r:
                    if r.status == 200 or r.status == 204:
                        print(f"{Fore.GREEN}[Success] {r.status} {Fore.RESET}| Changed skin of {name}")
                    else:
                        print(f"{Fore.RED}[Fail] {r.status} {Fore.RESET}| Failed to change skin of {name}")
            elif response.status == 400:
                print(f'{Fore.RED}[Fail] {response.status} {Fore.RESET}| Sent @ {datetime.fromtimestamp(now)}, Recieved @ {datetime.fromtimestamp(time.time())}')               

if __name__ == "__main__":
    info()
    nametiming(name)
    time.sleep(droptime['droptime'] + - time.time() - (offset / 1000))
    loop = asyncio.get_event_loop()
    coroutines = [request(name, bearer) for _ in range(6)]
    results = loop.run_until_complete(asyncio.gather(*coroutines))



