import json

def get_types(pokemonId):
    with open ('json File folder/evolution-chain.json', "r") as f:
        data = json.loads(f.read())
        return [t.capitalize() for t in data[pokemonId - 1]["types"]]

def get_weaknesses(types):
    damage = {}
    with open ('json File folder/types.json', "r") as f:
        data = json.loads(f.read())
        for t in types:
            entry = next(e for e in data if e["name"] == t)
            for v in entry["vulnerablities"]:
                if v in damage:
                    damage[v] = damage[v] * 2
                else:
                    damage[v] = 2
            for r in entry["resistant"]:
                if r in damage:
                    damage[r] = damage[r] * 0.5
                else:
                    damage[r] = 0
            for n in entry["noeffect"]:
                if n in damage:
                    damage[n] = damage[n] * 0
                else:
                    damage[n] = 0
    return [x[0] for x in damage.items() if x[1] >= 2]

def get_strengths(types):
    damage = {}
    with open ('json File folder/types.json', "r") as f:
        data = json.loads(f.read())
        for t in types:
            entry = next(e for e in data if e["name"] == t)
            for s in entry["strengths"]:
                if s in damage:
                    damage[s] = damage[s] * 2
                else:
                    damage[s] = 2
            for w in entry["weaknesses"]:
                if w in damage:
                    damage[w] = damage[w] * 0.5
                else:
                    damage[w] = 0
            for i in entry["immunes"]:
                if i in damage:
                    damage[i] = damage[i] * 0
                else:
                    damage[i] = 0
    return [x[0] for x in damage.items() if x[1] >= 2]

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

def get_types_string(list):
    with open ('json File folder/types.json', "r") as f:
        data = json.loads(f.read())
        tags = ["[color=" + next(c["color"] for c in data if c["name"] == t) + "]" + t + "[/color]" for t in list]
        return "   " + "   ".join(tags)



#"name": "Normal",
#"": [], // does 0 damage against
#"weaknesses": [ "Rock", "Steel" ], // does 1/2 damage against
#"strengths": [], // does 2 damage against
#"vulnerablities": [ "Fighting" ], // takes 2 damage from
#"resistant": [], // takes 1/2 damage from
#"noeffect": [ "Ghost" ], // takes 0 damage from
#"color": "#A8A878"


def get_moveset(pokemonId):
    with open ('json File folder/preferred-moves.json', "r") as preferredFile:
        preferredJson = json.loads(preferredFile.read())
        movesetList = next(l for l in preferredJson if l["id"] == pokemonId)["moveset"]
        if len(movesetList) == 0:
            movesetList = [0, 1, 2, 3]
        with open ('json File folder/' + str(pokemonId) + '.json', "r") as pokemonFile:
            pokemonJson = json.loads(pokemonFile.read())
            movesetNames = []
            for moveIndex in movesetList:
                movesetNames.append(pokemonJson["moves"][int(moveIndex)]["move"]["name"])
            return movesetNames

def get_abilities(pokemonId):
    with open ('json File folder/' + str(pokemonId) + '.json', "r") as pokemonFile:
        pokemonJson = json.loads(pokemonFile.read())
        return [a["ability"]["name"].capitalize() for a in pokemonJson["abilities"]]

#[hp, attack, defense, sp. attack, sp. defense, speed]
def get_stats(pokemonId):
    with open ('json File folder/' + str(pokemonId) + '.json', "r") as pokemonFile:
        pokemonJson = json.loads(pokemonFile.read())
        return [a["base_stat"] for a in pokemonJson["stats"]]

def get_description(pokemonId):
    with open ('json File folder/descriptions.json', "r") as f:
        data = json.loads(f.read())
        return next(d for d in data if d["id"] == pokemonId)["description"]

def get_color_list(value):
    if value > 15 / 18:
        return [0, .65, .62, 1]
    if value > 12 / 18:
        return [.14, .8, .37, 1]
    if value > 9 / 18:
        return [.63, .9, .08, 1]
    if value > 6 / 18:
        return [1, .87, .34, 1]
    if value > 3 / 18:
        return [1, .5, .06, 1]
    return [.95, .27, .27, 1]