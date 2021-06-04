from config import TomlConfig
from packs import PacksManager
from aiohttp import web
import server

# load the config
config = TomlConfig("config/settings.toml", "config/settings.template.toml")
if config.configured:
    app = web.Application()
    packs_manager = PacksManager(config)
    server.setup(app, config, packs_manager)
    web.run_app(app)
