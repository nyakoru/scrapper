#ALL PAYLOAD
def gamePL(name):
    return {
    "name": name
    }

def setPL(variant_id, name, product_code, metadata=None):
    return {
    "metadata": metadata,
    "name": name,
    "product_code": product_code,
    "variant_id": variant_id
    }

def varPL(name, game_id):

    return {
    "name": name,
    "game_id":game_id
    }

def prodPL(name, description, product_code, rarity, set_id, variant_id, metadata=None):
    return {
    "name":name,
    "description": description,
    "product_code": product_code,
    "rarity": rarity,
    "metadata": metadata,
    "set_id": set_id,
    "variant_id":variant_id
    }

if __name__ == "__main__":
    prodPL
    pass