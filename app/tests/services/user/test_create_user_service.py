# run: pytest .\app\tests\services\user\test_create_user_service.py -s -v
import pytest
from flask_login import login_user, logout_user


from app.infrastructure.extensions import db, login_manager
from app.domains.entities.user import User
from app.domains.exceptions import UnauthorizedError, ForbiddenError, ConflictError
from app.application.services.user.create_user_service import CreateUserService


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@pytest.fixture
def admin_user(db_session):
    user = User(
        username="admin",
        password=b"hash",
        email="admin@email.com",
        role="admin",
    )
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def normal_user(db_session):
    user = User(
        username="user",
        password=b"hash",
        email="user@email.com",
        role="user",
    )
    db_session.add(user)
    db_session.commit()
    return user


def test_create_user_success(db_session, app, admin_user):
    with app.app_context():
        with app.test_request_context():
            login_user(admin_user)

            data = {
                "username": "gabriel",
                "password": "123456",
                "email": "gabriel@email.com",
                "role": "user",
            }

            service = CreateUserService(data, db_session)
            user = service.to_execute()

            saved = db_session.query(User).filter_by(username="gabriel").first()

            assert saved is not None
            assert saved.id == user.id
            assert saved.username == "gabriel"
            assert saved.email == "gabriel@email.com"
            assert saved.role == "user"


def test_create_user_without_authentication(db_session, app, admin_user):
    with app.app_context():
        with app.test_request_context():
            logout_user()

            data = {
                "username": "joao",
                "password": "123456",
                "email": "joao@email.com",
                "role": "user",
            }

            service = CreateUserService(data, db_session)

            with pytest.raises(UnauthorizedError) as error:
                service.to_execute()

            assert "Sessão inválida ou expirada" in str(error.value)


def test_create_user_with_user_role_forbidden(db_session, app, normal_user):
    with app.app_context():
        with app.test_request_context():
            login_user(normal_user)

            data = {
                "username": "maria",
                "password": "123456",
                "email": "maria@email.com",
                "role": "user",
            }

            service = CreateUserService(data, db_session)

            with pytest.raises(ForbiddenError) as error:
                service.to_execute()

            assert "não tem permissão" in str(error.value)


def test_create_user_with_existing_username_conflict(db_session, app, admin_user):
    with app.app_context():
        with app.test_request_context():
            login_user(admin_user)

            existing_user = User(
                username="gabriel",
                password=b"hash",
                email="old@email.com",
                role="user",
            )
            db_session.add(existing_user)
            db_session.commit()

            data = {
                "username": "gabriel",
                "password": "123456",
                "email": "gabriel@email.com",
                "role": "user",
            }

            service = CreateUserService(data, db_session)

            with pytest.raises(ConflictError) as error:
                service.to_execute()

            assert "Já existe usuário cadastrado com esse username" in str(error.value)
