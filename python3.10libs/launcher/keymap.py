import logging
from pathlib import Path


def keymap_lookup(context: str, key: str):
    keymap = keymap_load()
    node = keymap[context][key]
    print(node)
    return node


def keymap_load():
    import json

    keymap_json = keymap_json_path()
    keymap = {}
    with open(keymap_json) as f:
        keymap = json.load(f)
    return keymap


def keymap_json_path():
    keymap_json = Path(__file__ + "/../keymap.json")
    return keymap_json


def keymap_append(context: str, key: str, node: str):
    for args in [context, key, node]:
        print(args)
        if args == "":
            logging.error("Empty arguments detected will not proceed")
            break

    import json
    keymap = keymap_load()
    key_pair = {key: node}

    keymap[context][key] = node

    keymap_json = keymap_json_path()
    with open(keymap_json, "w") as file:
        json.dump(keymap, file, indent=4)


def keymap_remove(context: str, key: str):
    import json
    
    keymap = keymap_load()
    keymap_json = keymap_json_path()
    try:
        del keymap[context][key]
        with open(keymap_json, "w") as file:
            json.dump(keymap, file, indent=4)
    except:
        logging.error(f"Unable to delete {context}:{key}")
    return
