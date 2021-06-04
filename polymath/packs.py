import utils
import hashlib
import time
import os


class PacksManager:
    def __init__(self, config):
        self.config = config
        self.folder = utils.get_path("storage/")
        if not os.path.exists(self.folder):
            os.mkdir(self.folder)
        self.packs_folder = self.folder + "packs/"
        self.registry = utils.SavedDict(self.folder + "registry.json")
        if not os.path.exists(self.packs_folder):
            os.mkdir(self.packs_folder)

    def register(self, pack, spigot_id, ip):
        sha1 = hashlib.sha1()
        sha1.update(pack)
        id_hash = sha1.hexdigest()

        with open(self.packs_folder + id_hash, "wb") as pack_file:
            pack_file.write(pack)

        self.registry[id_hash] = {
            "id": spigot_id,
            "ip": ip,
            "last_download": time.time(),
        }

        return id_hash

    def fetch(self, id_hash):
        output = self.packs_folder + id_hash
        if id_hash in self.registry and os.path.exists(output):
            self.registry[id_hash]["last_download"] = time.time()
            return output