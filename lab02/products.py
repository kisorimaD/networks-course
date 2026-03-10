import json

all_products = []
id_queue = []

def get_product(product_id):
    if product_id < 0 or product_id >= len(all_products):
        return None

    return all_products[product_id]


def add_product(name, description):
    if not id_queue:
        id_queue.append(len(all_products))
        all_products.append(None)

    next_id = id_queue[0]
    id_queue.pop(0)

    all_products[next_id] = json.dumps({
        'id': next_id,
        'name': name,
        'description': description
    })

    return all_products[next_id]


def update_product(id, update_json):
    product = get_product(id)

    if product is None:
        return None

    product_dict = json.loads(product)
    update_dict = json.loads(update_json)
    product_dict.update(update_dict)
    
    updated_product = json.dumps(product_dict)

    all_products[id] = updated_product

    return updated_product


def delete_product(id):
    product = get_product(id)
    
    if product is None:
        return None

    all_products[id] = None
    id_queue.append(id)
    
    return product


def get_all_products():
    return list(map(json.loads, filter(None, all_products)))
