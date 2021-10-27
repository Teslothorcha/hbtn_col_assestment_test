from flask import Blueprint, render_template
from flask import current_app as app


# Blueprint Configuration
order_bp = Blueprint(
    'order_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@order_bp.route('/', methods=['GET'])
def order():
    """orders main page"""
    return render_template('order/order_base.html')
