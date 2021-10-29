from flask import Blueprint, render_template


from app.models.productModel import Product
from app import db

# Blueprint Configuration
public_bp = Blueprint(
    'public_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@public_bp.route("/")
def index():
    """
    Gets all products information
    """
    products = db.session.query(Product).all()
    nested_product_data = [get_product_info(product)
                        for product in products]

    return render_template('public/index.html',
                nested_product_data=nested_product_data)

def get_product_info(product: Product)-> dict:
    """
    get order information on a dictionariy
    """
    data = {
        'product_id': product.id,
        'product_name': product.name,
        'product_price': product.price,
        'product_image_path': product.image_path
    }
    return data