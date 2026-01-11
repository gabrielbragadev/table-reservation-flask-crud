# run: pytest .\app\tests\services\user\test_create_user_service.py -s -v
import pytest
from flask_login import login_user

from app.extensions import db, login_manager
from app.models.user import User
from app.exceptions import UnauthorizedError, ForbiddenError, ConflictError
from app.services.user.create_user_service import CreateUserService


# user_loader necessário para o Flask-Login funcionar em teste
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# -------------------- FIXTURES --------------------


@pytest.fixture
def admin_user(db_session):
    user = User(
        username="admin",
        password=b"hash",
        email="admin@email.com",
        role="admin",
    )
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def normal_user(db_session):
    user = User(
        username="user",
        password=b"hash",
        email="user@email.com",
        role="user",
    )
    db.session.add(user)
    db.session.commit()
    return user


# -------------------- TESTES --------------------


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

            service = CreateUserService(data)
            user = service.create_user()

            saved = User.query.filter_by(username="gabriel").first()

            assert saved is not None
            assert saved.id == user.id
            assert saved.username == "gabriel"
            assert saved.email == "gabriel@email.com"
            assert saved.role == "user"


def test_create_user_without_authentication(db_session, app, admin_user):
    with app.app_context():
        with app.test_request_context():
            data = {
                "username": "joao",
                "password": "123456",
                "email": "joao@email.com",
                "role": "user",
            }

            service = CreateUserService(data)

            with pytest.raises(UnauthorizedError) as error:
                service.create_user()

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

            service = CreateUserService(data)

            with pytest.raises(ForbiddenError) as error:
                service.create_user()

            assert "não tem permissão" in str(error.value)


def test_create_user_with_existing_username_conflict(db_session, app, admin_user):
    with app.test_request_context():
        login_user(admin_user)

        existing_user = User(
            username="gabriel",
            password=b"hash",
            email="old@email.com",
            role="user",
        )
        db.session.add(existing_user)
        db.session.commit()

        data = {
            "username": "gabriel",
            "password": "123456",
            "email": "gabriel@email.com",
            "role": "user",
        }

        service = CreateUserService(data)

        with pytest.raises(ConflictError) as error:
            service.create_user()

        assert "Já existe usuário cadastrado com esse username" in str(error.value)
