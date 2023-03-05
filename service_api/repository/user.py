from sqlalchemy.exc import IntegrityError

from service_api.models import UserModel
from service_api.services.logger import app_logger


class UserRepo:
    pass


def init_users():
    from service_api.models.user import UserRoles
    from service_api.services import db_session

    conn = db_session()

    admin = UserModel(email="admin@xart.com", role=UserRoles.ADMIN, password="password")

    kevin_qa = UserModel(email="kevin@xart.com", role=UserRoles.QA, password="password")
    qa2 = UserModel(email="qa2@xart.com", role=UserRoles.QA, password="password")
    qa3 = UserModel(email="qa3@xart.com", role=UserRoles.QA, password="password")
    qa4 = UserModel(email="qa4@xart.com", role=UserRoles.QA, password="password")

    conn.add_all([admin, kevin_qa, qa2, qa3, qa4])

    try:
        conn.commit()
    except IntegrityError:
        app_logger.warning("Users already exist")
    else:
        app_logger.info("Users successfully created")
