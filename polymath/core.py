from config import TomlConfig
from packs import PacksManager
from aiohttp import web
import asyncio
import server
import cleaner
import os

async def main():
    # load the config
    config = TomlConfig("config/settings.toml", "config/settings.template.toml")
    if not config.configured:
        return

    host_ip = config['nginx']['nginx_location'] if config['nginx']['enabled'] and config['nginx']['only_listen_nginx'] else '0.0.0.0'
    
    app = web.Application(client_max_size=config["request"]["max_size"])
    packs_manager = PacksManager(config)
    server.setup(app, config, packs_manager)

    print(config['server']['print_startup'])
    _ = os.system('cls') if os.name == 'nt' else os.system('clear')

    print("Oraxen Polymouth Listening on: http://"+host_ip+':'+config["server"]["port"])
    print("Test URL: http://127.0.0.1:"+config["server"]["port"]+"/debug")
    print("="*70)
    runner = web.AppRunner(app)
    await runner.setup()
    await web.TCPSite(runner,host=host_ip ,port=config["server"]["port"]).start()
    await cleaner.start(packs_manager, config)
    await asyncio.Event().wait()
    
asyncio.run(main())