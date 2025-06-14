from functools import wraps
from flask_login import current_user
from flask import abort, request
import logging

logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

def role_required(*roles):
    """
    Decorador para restringir el acceso a vistas según el rol del usuario.
    Uso: @role_required('admin', 'director')
    """
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not hasattr(current_user, 'role') or current_user.role not in roles:
                logger.warning(
                    f"Acceso denegado: Usuario '{getattr(current_user, 'email', 'desconocido')}' con rol '{getattr(current_user, 'role', 'ninguno')}' intentó acceder a '{request.path}'"
                )
                abort(403)
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper
