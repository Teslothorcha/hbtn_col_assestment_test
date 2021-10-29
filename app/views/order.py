from flask import Blueprint, render_template
from flask_login import login_required
from datetime import datetime

from app import db
from app.models.userModel import User
from app.models.orderModel import Order

# Blueprint Configuration
order_bp = Blueprint(
    'order_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

#need to protect only for admin
@order_bp.route('/order/<int:order_id>', methods=['GET'])
@login_required
def order(order_id: int):
    """
    Gets singel order information
    """
    order = db.session.query(Order).get(order_id)
    if order:
        data = get_order_info(order)
        return render_template('order/order_base.html', order_data=data)
    data = {
        'error_msg': 'No order found'
        }
    return render_template('order/order_base.html', order_data=data), 404

#need to protect only for admin
@order_bp.route('/orders/<orders_ids>', methods=['GET'])
@login_required
def orders(orders_ids):
    """
    Gets orders information by given ids
    """
    list_orders_ids = list(orders_ids.split(","))
    orders = db.session.query(Order).filter(Order.id.in_(list_orders_ids))
    
    nested_order_data = [get_order_info(order) if order 
                        else {'error_msg': 'No order found'}
                        for order in orders]
    print(nested_order_data)
    return render_template('order/orders_base.html',
            nested_order_data=nested_order_data)

@order_bp.route('/orders_dates/<dates>', methods=['GET'])
@login_required
def orders_date(dates: str):
    """
    Gets single order information
    """
    dates_plitted = dates.split(",")
    orders_start = dates_plitted[0]
    orders_end = dates_plitted[1]
    start_date = datetime.strptime(orders_start, '%Y-%m-%d')
    end_date = datetime.strptime(orders_end, '%Y-%m-%d')
    orders = db.session.query(Order).filter(Order.date >= start_date,
    Order.date <= end_date).all()
    
    nested_order_data = [get_order_info(order) if order 
                        else {'error_msg': 'No order found'}
                        for order in orders]
    return render_template('order/orders_base.html',
                nested_order_data=nested_order_data)

@order_bp.route('/orders_user/<int:user_id>', methods=['GET'])
@login_required
def orders_user(user_id: str):
    """
    Gets singel order information
    """
    orders = db.session.query(Order).filter(Order.user_id == user_id).all()
    
    nested_order_data = [get_order_info(order) if order 
                        else {'error_msg': 'No order found'}
                        for order in orders]
    return render_template('order/orders_base.html',
                nested_order_data=nested_order_data)



def get_order_info(order: Order)-> dict:
    """
    get order information on a dictionariy
    """
    data = {
        'order_id': order.id,
        'order_date': str(order.date),
        'order_subtotal': str(order.subtotal),
        'order_taxes': str(order.subtotal),
        'order_paid': str(order.paid),
        'order_user_id': order.user_id,
        'order_products': [p.name for p in order.products],
        'order_payments': [p.paid for p in order.payments],
        'order_shipping_id': order.shipping.id if order.shipping else None,
    }
    return data