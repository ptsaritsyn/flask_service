from app import app
from service.blueprint import service_app
import views

app.register_blueprint(service_app, url_prefix='/service')

if __name__ == '__main__':
    app.run()
