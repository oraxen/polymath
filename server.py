import hashlib
import json
import time
import os
from aiohttp import web

# CONSTANTS
SERVER_URL = "http://hestia.oraxen.com:8080" # The first dedicated vps for polymath
PACKS_FOLDER = "./packs"
REGISTRY_FILE = './registry.json'
REGISTRY = {}

INSTANT_SAVE = True

#-----------SERVER-------------------

async def upload(request):
    """" Allow to upload a resourcepack with a spigot id
    test: curl -F "pack=@./file.zip" -F "id=EXAMPLE" -X POST http://localhost:8080/upload """
    data = await request.post()
    spigot_id = data['id']
    id_hash = hashlib.sha256(spigot_id.encode('utf-8')).hexdigest()[0:32]
    pack = data['pack']

    sha1 = hashlib.sha1()

    with open(PACKS_FOLDER + id_hash, 'wb') as pack_file:
        data = pack.file.read()
        if len(data) >= 100 * 2**10: # we don't accept file larger than 100MiB
            return
        sha1.update(data)
        pack_file.write(data)
    register(id_hash, spigot_id, request.remote)

    if INSTANT_SAVE:
        write_to_file()

    return web.json_response({
        "url" : SERVER_URL + "/download?id=" + id_hash,
        "sha1" : sha1.hexdigest()
    })

# To download a resourcepack from its id
async def download(request):
    """" Allow to download a resourcepack with a spigot id
    test: curl http://localhost:8080/download?id=EXAMPLE """
    params = request.rel_url.query
    id_hash = params["id"]
    if os.path.exists(PACKS_FOLDER + id_hash):
        update(id_hash)
        return web.FileResponse(PACKS_FOLDER + id_hash)

# To debug
async def debug(request):
    """" Allow to test the connection
    test: curl http://localhost:8080/debug """
    return web.Response(body="It seems to be working...")

#------------REGISTRY-------------
def register(id_hash, spigot_id, ip):
    """ Store informations about the server
    """
    if id_hash not in REGISTRY:
        REGISTRY[id_hash] = {}
    REGISTRY[id_hash]["id"] = spigot_id
    REGISTRY[id_hash]["ip"] = ip
    REGISTRY[id_hash]["upload_time"] = time.time()

def update(id_hash):
    """ Store the date of the last download of a pack
    """
    REGISTRY[id_hash]["last_download_time"] = time.time()

def read_registry():
    """ Read olds registry informations on startup
    """
    global REGISTRY
    #----------START CODE--------
    if os.path.exists(REGISTRY_FILE):
        with open(REGISTRY_FILE) as json_file:
            REGISTRY = json.load(json_file)

def write_to_file():
    """ Save registry informations to disk
    """
    with open(REGISTRY_FILE, 'w') as json_output_file:
        json.dump(REGISTRY, json_output_file)

def main():
    """ Core process of the program
    """
    read_registry()

    if not os.path.exists(PACKS_FOLDER):
        os.mkdir(PACKS_FOLDER)

    app = web.Application()
    app.add_routes([web.post('/upload', upload),
                    web.get('/download', download),
                    web.get('/debug', debug)])
    web.run_app(app)

    #-----------EXIT CODE--------------
    if not INSTANT_SAVE:
        write_to_file()

if __name__ == '__main__':
    main()
