from aiohttp import web


def setup(app, config, packs_manager):
    routes = Routes(config, packs_manager)
    app.add_routes(
        [
            web.post("/upload", routes.upload),
            web.get("/pack.zip", routes.download),
            web.get("/debug", routes.debug),
        ]
    )


class Routes:
    def __init__(self, config, packs_manager):
        self.config = config
        self.packs = packs_manager

    def start(self):
        web.run_app(self.app)

    async def upload(self, request):
        """
        Allow to upload a resourcepack with a spigot id

           Test: curl -F "pack=@./file.zip" -F "id=EXAMPLE" -X POST http://localhost:8080/upload

           Parameters:
               self (Routes): An instance of Routes
               request (aiohttp.web_request.Request): The web request

           Returns:
               pack (web.json_response): Pack url and its SHA1 hash
        """
        data = await request.post()
        spigot_id = data["id"]

        if spigot_id in []:
            return web.json_response({"error": "This license has been disabled"})

        pack = data["pack"].file.read()
        id_hash = self.packs.register(pack, spigot_id, request.remote)

        return web.json_response(
            {
                "url": self.config["server"]["url"] + "/pack.zip?id=" + id_hash,
                "sha1": id_hash,
            }
        )

    # To download a resourcepack from its id
    async def download(self, request):
        """
        Allow to download a resourcepack with a spigot id

            Test: curl http://localhost:8080/download?id=EXAMPLE

            Parameters:
                self (Routes): An instance of Routes
                request (aiohttp.web_request.Request): The web request

            Returns:
                pack (web.FileResponse): the resource pack
        """
        params = request.rel_url.query
        pack = self.packs.fetch(params["id"])
        if not pack:
            return web.Response(body=b"Pack not found")
        else:
            return web.FileResponse(pack, headers={"content-type": "application/zip"})

    async def debug(self, request):
        print(type(request))
        """
        Allow to test the connection

            Test: curl http://localhost:8080/debug
        
            Parameters:
                self (Routes): An instance of Routes
                request (aiohttp.web_request.Request): The web request
        """
        return web.Response(body="It seems to be working...")