import server as polymath
import json
import time
import os

registry = {}

print(os.path.dirname(os.path.realpath(__file__)))

if os.path.exists(polymath.REGISTRY_FILE):
    with open(polymath.REGISTRY_FILE) as json_file:
        registry = json.load(json_file)

def clean_registry():
    global registry
    registry_clone = {}
    print("\n--- cleaning registry ---")
    for hash in registry:
        if not os.path.exists(polymath.PACKS_FOLDER + hash):
            print("removing not written ", hash)
        elif time.time() - registry[hash]["upload_time"] > 3600*24*30: # one month old
            print("removing old ", hash)
        else:
            registry_clone[hash] = registry[hash]
    registry = registry_clone
    print("--- registry cleaned ---")


def clean_packs_folder():
    print("\n--- cleaning packs ---")
    for pack in [f for f in os.listdir(polymath.PACKS_FOLDER) if os.path.isfile(os.path.join(polymath.PACKS_FOLDER, f))]:
        if pack not in registry:
            os.remove(os.path.join(polymath.PACKS_FOLDER, pack))
            print("removing", pack)
    print("--- packs cleaned ---")

clean_registry()
clean_packs_folder()

with open(polymath.REGISTRY_FILE, 'w') as json_output_file:
    json.dump(registry, json_output_file)