from aiohttp import web
import hashlib
import json
import time
import os

# VARIABLES
SERVER_URL = "polymath-atlas.oraxen.com" # A constant actually: the first dedicated vps for polymath
registry = {}


#-----------SERVER-------------------

# To upload a resourcepack with its id
# test: curl -F "pack=./file.zip" -F "id=EXAMPLE" -X POST http://localhost:8080/upload
async def upload(request):
    data = await request.post()
    id = data['id']
    pack = data['pack']
    id_hash = hashlib.sha256(id.encode('utf-8')).hexdigest()[0:32]

    packs_folder = "./packs/"
    if not os.path.exists(packs_folder):
        os.mkdir(packs_folder)

    if os.path.exists(packs_folder + id_hash):
        os.remove(packs_folder + id_hash)

    with pack.file().open('w') as pack_file:
        pack_file.write(packs_folder + id_hash)
    register(id_hash, id, request.remote)

    return web.json_response({
        "url" : "http://" + SERVER_URL + "/download&id=" + id_hash
    })

# To download a resourcepack from its id
async def download(request):
    data = await request.get()
    id = data['id']
    # todo: check if a pack with this id exists
    return web.FileResponse('./' + id + '/pack.zip')


#------------REGISTRY-------------
def register(id_hash, id, ip):
    global registry
    registry["id_hash"]["id"] = id
    registry["id_hash"]["ip"] = ip
    registry["id_hash"]["upload_time"] = time.time()

def update(id_hash):
    global registry
    registry["id_hash"]["last_download_time"] = time.time()


#----------START CODE--------
registry_file = './registry.json'
if os.path.exists(registry_file):
    with open(registry_file) as json_file:
        registry = json_file

app = web.Application()
app.add_routes([web.post('/upload', upload),
                web.get('/download', download)])
web.run_app(app)

#-----------EXIT CODE--------------
with open(registry_file, 'w') as json_output_file:
    json.dump(registry, registry_file)

# todo:
# - keep a track of files (date of creation, ip, etc...)
# - create a garbage collector