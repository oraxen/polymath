from polymath.config import TomlConfig
from polymath.packs import PacksManager
from aiohttp import web
from colorama import Fore,init
import asyncio
from polymath import server
from polymath import cleaner
import os
import logging 

init()

async def main():
    # load the config
    config = TomlConfig("config/settings.toml", "config/settings.template.toml")
    if not config.configured:
        return

    host_ip = config['nginx']['nginx_location'] if config['nginx']['enabled'] and config['nginx']['only_listen_nginx'] else '0.0.0.0'
    
    app = web.Application(client_max_size=config["request"]["max_size"])
    packs_manager = PacksManager(config)
    
    # set debugging Level.
    logging.basicConfig(
        level=config['extra']['debug_level'],
        format="[%(asctime)s] "+Fore.YELLOW+"[%(levelname)s] "+Fore.RESET+"%(message)s",
        filename= str(config['extra']['log2file']) if str(config['extra']['log2file']) != "-1" else None
    )

    server.setup(app, config, packs_manager) # setup the routes and server.

    print(config['extra']['print_startup'])
    _ = os.system('cls') if os.name == 'nt' else os.system('clear')

    print("Oraxen Polymouth Listening on: http://"+host_ip+':'+config["server"]["port"])
    print("Test URL: http://127.0.0.1:"+config["server"]["port"]+"/debug")
    print("="*70)
    
    # disable access log if debug is not set.
    if config['extra']['debug_level'] <= 10:
        runner = web.AppRunner(app)
    else:
        runner = web.AppRunner(app,access_log=None)
    
    await runner.setup()
    await web.TCPSite(runner,host=host_ip ,port=config["server"]["port"]).start()
    await cleaner.start(packs_manager, config)
    await asyncio.Event().wait()
    
asyncio.run(main())