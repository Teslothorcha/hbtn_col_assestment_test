"""Application entry point."""
from app import create_app, db
from app.models.orderModel import Order
from app.models.auditModel import Audit

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Order': Order, 'Audit': Audit}
    
if __name__ == "__main__":
    app.run(host="0.0.0.0")