import os
from flask import Flask, request, abort, send_from_directory
from products import get_product, add_product, update_product, delete_product, get_all_products
import json


app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'pics')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
        result = update_product(int(product_id), request.data)

        if result is None:
            abort(404)
        return result

    if request.method == 'DELETE':
        result = delete_product(int(product_id))

        return result


@app.route('/product/<product_id>/image', methods=['GET', 'POST'])
def handle_product_image(product_id):
    pid = int(product_id)
    product_raw = get_product(pid)

    if product_raw is None:
        abort(404, description="File not found")

    product = json.loads(product_raw)

    if request.method == 'POST':
        if 'icon' not in request.files:
            abort(400, description="No file part")

        file = request.files['icon']

        if file.filename == '':
            abort(400, description="No selected file")

        if file and allowed_file(file.filename):
            filename = f"icon_{pid}_{file.filename}"
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)

            update_product(pid, {'icon': file_path})

            return {"message": "Image uploaded successfully", "path": file_path}

        abort(400)

    if request.method == 'GET':
        icon_path = product.get('icon')
        if not icon_path or not os.path.exists(icon_path):
            abort(404, description="No icon upload for this product")

        directory = os.path.dirname(icon_path)
        filename = os.path.basename(icon_path)
        return send_from_directory(directory, filename)


@app.route('/products', methods=['GET'])
def handle_get_all_products():
    return get_all_products()


if __name__ == '__main__':
    app.run(debug=True, extra_files=['pics'])
