from app import app
import view
from clothes.routes import clothes
from cart.routes import cart

app.register_blueprint(clothes, url_prefix='/clothes')
app.register_blueprint(cart, url_prefix='/cart')

if __name__ == '__main__':
    app.run()