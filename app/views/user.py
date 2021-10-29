from flask import Blueprint, render_template
from flask_login import login_required
from app import db
from app.models.userModel import User

# Blueprint Configuration
user_bp = Blueprint(
    'user_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

#need to protect only for admin
@user_bp.route('/user/<int:user_id>', methods=['GET'])
@login_required
def user(user_id: int):
    """
    Gets single user information
    """
    user = db.session.query(User).get(user_id)
    if user:
        data = get_user_info(user)
        return render_template('user/user_base.html', order_data=data)
    data = {
        'error_msg': 'No order found'
        }
    return render_template('user/user_base.html', order_data=data), 404

def get_user_info(user: User)-> dict:
    """
    get user information on a dictionariy
    """
    data = {
        'user_id': user.id,
        'user_name': user.name,
        'user_last_name': user.last_name,
        'user_gov_id': user.gov_id,
        'user_email': user.email,
        'user_company': user.company,
        'user_orders': [f'id {o.id}  paid{o.paid}.'
                         for o in user.orders],
        'user_addresses': [f"id {a.id }{a.country}-{a.state}-{a.city}."
                             for a in user.addresses],
        'user_is_admin': user.is_admin,
    }
    return data