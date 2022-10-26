import json

def get_types(pokemonId):
    with open ('json File folder/evolution-chain.json', "r") as f:
        data = json.loads(f.read())
        return [t.capitalize() for t in data[pokemonId - 1]["types"]]

def get_weaknesses(pokemonId):
    types = get_types(pokemonId)
    weaknesses = []
    with open ('json File folder/types.json', "r") as f:
        data = json.loads(f.read())
        for t in types:
            weaknesses = weaknesses + next(w["vulnerablities"] for w in data if w["name"] == t)
    return weaknesses

def get_chain(pokemonId):
    froms = []
    tos = []
    with open ('json File folder/evolution-chain.json', "r") as f:
        data = json.loads(f.read())
        pokemon = data[pokemonId - 1]
        prev = pokemon["from"]
        while prev != None:
            froms = [prev] + froms
            prev = data[prev - 1]["from"]
        next = pokemon["to"]
        while next != None:
            tos = tos + [next]
            next = data[next - 1]["to"]
    return froms + [pokemonId] + tos

def get_name(pokemonId):
    with open ('json File folder/evolution-chain.json', "r") as f:
        data = json.loads(f.read())
        return data[pokemonId - 1]["name"]

def get_chain_names(pokemonId):
    return [get_name(x) for x in get_chain(pokemonId)]