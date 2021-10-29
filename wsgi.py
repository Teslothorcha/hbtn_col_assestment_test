"""Application entry point."""
from app import create_app, db
from app.models.orderModel import Order
from app.models.auditModel import Audit
from app.models.userModel import User
from app.models.addressModel import Address
from app.models.shippingModel import Shipping
from app.models.productModel import Product, OrderedProduct
from app.models.paymentModel import Payment, Wallet

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Order': Order, 'Audit': Audit, 'User': User,
    'Address': Address, 'Shipping': Shipping, 'Product': Product,
    'Payment': Payment, 'OrderedProdcut': OrderedProduct, 'Wallet': Wallet}

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)