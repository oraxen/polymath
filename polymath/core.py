from polymath.config import TomlConfig
from polymath.packs import PacksManager
from aiohttp import web
import asyncio
from polymath import server
from polymath import cleaner


async def main():
    # load the config
    config = TomlConfig("config/settings.toml", "config/settings.template.toml")
    if not config.configured:
        return

    app = web.Application(client_max_size=config["request"]["max_size"])
    packs_manager = PacksManager(config)
    server.setup(app, config, packs_manager)

    runner = web.AppRunner(app)
    await runner.setup()
    await web.TCPSite(runner, port=config["server"]["port"]).start()
    await cleaner.start(packs_manager, config)
    await asyncio.Event().wait()


asyncio.run(main())