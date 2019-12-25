import hashlib
import json
import time
import os
from aiohttp import web

# CONSTANTS
SERVER_URL = "http://hestia.oraxen.com:8080" # A constant actually: the first dedicated vps for polymath
PACKS_FOLDER = "./packs/"
REGISTRY = {}

#-----------SERVER-------------------

# To upload a resourcepack with a spigot id
# test: curl -F "pack=@./file.zip" -F "id=EXAMPLE" -X POST http://localhost:8080/upload
async def upload(request):
    data = await request.post()
    spigot_id = data['id']
    id_hash = hashlib.sha256(spigot_id.encode('utf-8')).hexdigest()[0:32]
    pack = data['pack']

    sha1 = hashlib.sha1()

    with open(PACKS_FOLDER + id_hash, 'wb') as pack_file:
        data = pack.file.read()
        sha1.update(data)
        pack_file.write(data)
    register(id_hash, spigot_id, request.remote)

    return web.json_response({
        "url" : SERVER_URL + "/download?id=" + id_hash,
        "sha1" : sha1.hexdigest()
    })

# To download a resourcepack from its id
async def download(request):
    params = request.rel_url.query
    id_hash = params["id"]
    if os.path.exists(PACKS_FOLDER + id_hash):
        update(id_hash)
        return web.FileResponse(PACKS_FOLDER + id_hash)

# To debug
async def debug(request):
    return web.Response(body="It seems to be working...")

#------------REGISTRY-------------
def register(id_hash, spigot_id, ip):
    if id_hash not in REGISTRY:
        REGISTRY[id_hash] = {}
    REGISTRY[id_hash]["id"] = spigot_id
    REGISTRY[id_hash]["ip"] = ip
    REGISTRY[id_hash]["upload_time"] = time.time()

def update(id_hash):
    REGISTRY[id_hash]["last_download_time"] = time.time()

def main():
    #----------START CODE--------
    REGISTRY_file = './REGISTRY.json'
    if os.path.exists(REGISTRY_file):
        with open(REGISTRY_file) as json_file:
            REGISTRY = json.load(json_file)

    if not os.path.exists(PACKS_FOLDER):
        os.mkdir(PACKS_FOLDER)

    app = web.Application()
    app.add_routes([web.post('/upload', upload),
                    web.get('/download', download),
                    web.get('/debug', debug)])
    web.run_app(app)

    #-----------EXIT CODE--------------
    with open(REGISTRY_file, 'w') as json_output_file:
        json.dump(REGISTRY, json_output_file)

if __name__ == '__main__':
    main()