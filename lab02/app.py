from flask import Flask, request, abort
from products import get_product, add_product, update_product, delete_product, get_all_products


app = Flask(__name__)

@app.route('/product', methods=['POST'])
def handle_new_product():
    result = add_product(request.form["name"], request.form["description"])
    return result


@app.route('/product/<product_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_product_operations(product_id):
    if request.method == 'GET':
        result = get_product(int(product_id))
        if result is None:
            abort(404)
        return result
    
    if request.method == 'PUT':
        # print(request.data)
        result = update_product(int(product_id), request.data)
        
        if result is None:
            abort(404)
        return result
    
    if request.method == 'DELETE':
        result = delete_product(int(product_id))

        return result
    
@app.route('/products', methods=['GET'])
def handle_get_all_products():
    return get_all_products()


if __name__ == '__main__':
    app.run(debug=True)
