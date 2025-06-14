from flask import Flask, render_template
from flask_login import LoginManager
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from flask_talisman import Talisman 
from dotenv import load_dotenv
from app.extensions import db, login_manager
import os
import logging
from logging.handlers import RotatingFileHandler

# Inicialización de extensiones
mail = Mail()
csrf = CSRFProtect()
talisman = Talisman()  

def create_app(config_name=None):
    load_dotenv()
    
    app = Flask(__name__)
    
    # Configuración basada en el entorno
    if config_name == 'testing':
        app.config.from_mapping(
            TESTING=True,
            SQLALCHEMY_DATABASE_URI='sqlite:///:memory:',
            WTF_CSRF_ENABLED=False,
            SECRET_KEY='test',
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            MAIL_SUPPRESS_SEND=True  # Para pruebas con mail
        )
    else:
        app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
        app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
        app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True') == 'True'
        app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
        app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
        app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar extensiones con la app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    mail.init_app(app)
    csrf.init_app(app)

    # Configuración de Talisman (excepto en testing y development)
    if config_name != 'testing':
        if os.getenv("FLASK_ENV") != "development":
            csp = {
                'default-src': "'self'",
                'script-src': "'self' https://cdn.jsdelivr.net",   
                'connect-src': "'self'",
                'img-src': "'self' data:",
                'style-src': "'self' https://cdn.jsdelivr.net",   
                'font-src': "'self' https://cdn.jsdelivr.net"   
            }
            talisman.init_app(app, content_security_policy=csp)  # Usamos la instancia global

    # Importar modelos después de inicializar db
    from app.models import Usuario

    # Registrar Blueprints
    from app.auth.routes import auth
    from app.main.routes import main
    app.register_blueprint(auth)
    app.register_blueprint(main)

    # Cargar usuario
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    # Manejo de errores
    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('403.html'), 403

    # Configuración de logs (solo para producción)
    if config_name != 'testing':
        if not os.path.exists('logs'):
            os.mkdir('logs')

        file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=3)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        ))
        file_handler.setLevel(logging.INFO)

        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('App iniciada')

    return app