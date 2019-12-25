from aiohttp import web
import hashlib
import json
import time
import os

# VARIABLES
SERVER_URL = "http://hestia.oraxen.com:8080" # A constant actually: the first dedicated vps for polymath
registry = {}
packs_folder = "./packs/"

#-----------SERVER-------------------

# To upload a resourcepack with a spigot id
# test: curl -F "pack=@./file.zip" -F "id=EXAMPLE" -X POST http://localhost:8080/upload
async def upload(request):
    data = await request.post()
    spigot_id = data['id']
    id_hash = hashlib.sha256(spigot_id.encode('utf-8')).hexdigest()[0:32]
    pack = data['pack']

    if os.path.exists(packs_folder + id_hash):
        os.remove(packs_folder + id_hash)

    with open(packs_folder + id_hash, 'wb') as pack_file:
        pack_file.write(pack.file.read())
    register(id_hash, spigot_id, request.remote)

    return web.json_response({
        "url" : SERVER_URL + "/download?id=" + id_hash
    })

# To download a resourcepack from its id
async def download(request):
    params = request.rel_url.query
    id_hash = params["id"]
    if os.path.exists(packs_folder + id_hash):
        update(id_hash)
        return web.FileResponse(packs_folder + id_hash)

# To debug
async def debug(request):
    return web.Response(body="It seems to be working...")

#------------REGISTRY-------------
def register(id_hash, spigot_id, ip):
    if id_hash not in registry:
        registry[id_hash] = {}
    registry[id_hash]["id"] = spigot_id
    registry[id_hash]["ip"] = ip
    registry[id_hash]["upload_time"] = time.time()

def update(id_hash):
    registry[id_hash]["last_download_time"] = time.time()


#----------START CODE--------
registry_file = './registry.json'
if os.path.exists(registry_file):
    with open(registry_file) as json_file:
        registry = json.load(json_file)

if not os.path.exists(packs_folder):
    os.mkdir(packs_folder)

app = web.Application()
app.add_routes([web.post('/upload', upload),
                web.get('/download', download),
                web.get('/debug', debug)])
web.run_app(app)

#-----------EXIT CODE--------------
with open(registry_file, 'w') as json_output_file:
    json.dump(registry, json_output_file)

# todo:
# - keep a track of files (date of creation, ip, etc...)
# - create a garbage collector