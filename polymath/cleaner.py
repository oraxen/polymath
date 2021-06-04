import asyncio
import time
import os


async def start(packs_manager, config):
    while True:
        clean(packs_manager, config)
        await asyncio.sleep(config["cleaner"]["delay"])


def clean(packs_manager, config):
    for id_hash in list(packs_manager.registry.keys()):  # workaround to "copy" the keys
        pack = packs_manager.registry[id_hash]
        pack_file = packs_manager.packs_folder + id_hash

        if not os.path.exists(pack_file):
            packs_manager.registry.pop(id_hash)
        elif (
            time.time() - packs_manager.registry[id_hash]["last_download"]
            > config["cleaner"]["pack_lifespan"]
        ):
            packs_manager.registry.pop(id_hash)
            os.remove(pack_file)

    for id_hash in os.listdir(packs_manager.packs_folder):
        if (
            os.path.isfile(os.path.join(packs_manager.packs_folder, id_hash))
            and id_hash not in packs_manager.registry
        ):
            os.remove(os.path.join(packs_manager.packs_folder, id_hash))
