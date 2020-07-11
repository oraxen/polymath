import hashlib
import json
import time
import os
from aiohttp import web

def get_path(name):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), name)

# CONSTANTS

PACKS_FOLDER = get_path("packs/")
REGISTRY_FILE = get_path("registry.json")
BLACKLIST_FILE = get_path("blacklist.json")

INSTANT_SAVE = True

#-----------SERVER-------------------
class PolymathServer:

    def __init__(self, blacklist, registry, packs_folder):
        self.server_url = "http://atlas.oraxen.com:8080" # The first dedicated vps for polymath
        self.blacklist = blacklist
        self.registry = registry
        self.packs_folder = packs_folder
        self.app = web.Application(client_max_size = 10000 * 2**10) # we don't accept file larger than 100MiB
        self.app.add_routes([web.post('/upload', self.upload),
                        web.get('/pack.zip', self.download),
                        web.get('/debug', self.debug)])

    def start(self):
        web.run_app(self.app)

    async def upload(self, request):
        """" Allow to upload a resourcepack with a spigot id
        test: curl -F "pack=@./file.zip" -F "id=EXAMPLE" -X POST http://localhost:8080/upload """
        data = await request.post()
        spigot_id = data['id']

        if spigot_id in self.blacklist:
            return web.json_response({
                "error" : "This license has been disabled"
            })

        pack = data['pack']

        sha1 = hashlib.sha1()
        data = pack.file.read()
        sha1.update(data)
        id_hash = sha1.hexdigest()
        with open(self.packs_folder + id_hash, 'wb') as pack_file:
            pack_file.write(data)
        self._register(id_hash, spigot_id, request.remote)

        if INSTANT_SAVE:
            write_to_file()

        return web.json_response({
            "url" : self.server_url + "/pack.zip?id=" + id_hash,
            "sha1" : id_hash
        })

    # To download a resourcepack from its id
    async def download(self, request):
        """" Allow to download a resourcepack with a spigot id
        test: curl http://localhost:8080/download?id=EXAMPLE """
        params = request.rel_url.query
        id_hash = params["id"]
        if id_hash not in self.registry:
            return web.Response(body=b"Pack not found")
        if os.path.exists(self.packs_folder + id_hash):
            self._update(id_hash)
            return web.FileResponse(self.packs_folder + id_hash, headers = {'content-type': 'application/zip'})

    # To debug
    async def debug(self, request):
        """" Allow to test the connection
        test: curl http://localhost:8080/debug """
        return web.Response(body="It seems to be working...")

    #------------REGISTRY-------------
    def _register(self, id_hash, spigot_id, ip):
        """ Store informations about the server
        """
        if id_hash not in self.registry:
            self.registry[id_hash] = {}
        self.registry[id_hash]["id"] = spigot_id
        self.registry[id_hash]["ip"] = ip
        self.registry[id_hash]["last_download_time"] = time.time()

    def _update(self, id_hash):
        """ Store the date of the last download of a pack
        """
        REGISTRY[id_hash]["last_download_time"] = time.time()

def read_file(file):
    """ Read olds registry informations on startup
    """
    #----------START CODE--------
    if os.path.exists(file):
        with open(file) as json_file:
            return json.load(json_file)


def main():
    """ Core process of the program
    """
    REGISTRY = read_file(REGISTRY_FILE)
    BLACKLIST = read_file(BLACKLIST_FILE)

    if not os.path.exists(PACKS_FOLDER):
        os.mkdir(PACKS_FOLDER)

    server = PolymathServer(BLACKLIST, REGISTRY, PACKS_FOLDER)
    server.start()

    #-----------EXIT CODE--------------
    if not INSTANT_SAVE:
        with open(REGISTRY_FILE, 'w') as json_output_file:
            json.dump(server.registry, json_output_file)

if __name__ == '__main__':
    main()
