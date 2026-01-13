# run: pytest .\app\tests\services\user\test_delete_user_service.py -s -v
import pytest
from flask_login import login_user, logout_user

from app.infrastructure.extensions import db, login_manager
from app.domains.entities.user import User
from app.domains.exceptions import ForbiddenError, NotFoundError
from app.application.services.user.delete_user_service import DeleteUserService


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


@pytest.fixture
def target_user(db_session):
    user = User(
        username="target",
        password=b"hash",
        email="target@email.com",
        role="user",
    )
    db_session.add(user)
    db_session.commit()
    return user


# -------------------- TESTES --------------------

def test_delete_user_success(db_session, app, admin_user, target_user):
    with app.app_context():
        with app.test_request_context():
            login_user(admin_user)

            service = DeleteUserService(target_user.id, db_session)
            result = service.to_execute()

            assert result["id"] == target_user.id
            assert result["username"] == "target"
            # Confirma que o usuário foi realmente removido do banco
            deleted = db_session.query(User).filter_by(id=target_user.id).first()
            assert deleted is None


def test_delete_user_not_found(db_session, app, admin_user):
    with app.app_context():
        with app.test_request_context():
            login_user(admin_user)

            service = DeleteUserService(user_id=999, session=db_session)

            with pytest.raises(NotFoundError) as error:
                service.to_execute()

            assert "Registro não encontrado" in str(error.value)


def test_delete_user_forbidden_self(db_session, app, admin_user):
    with app.app_context():
        with app.test_request_context():
            login_user(admin_user)

            service = DeleteUserService(admin_user.id, db_session)

            with pytest.raises(ForbiddenError) as error:
                service.to_execute()

            assert "Você não pode excluir seu próprio usuário" in str(error.value)


def test_delete_user_forbidden_role(db_session, app, normal_user, target_user):
    with app.app_context():
        with app.test_request_context():
            login_user(normal_user)

            service = DeleteUserService(target_user.id, db_session)

            with pytest.raises(ForbiddenError) as error:
                service.to_execute()

            assert "Você não tem permissão pra realizar essa ação" in str(error.value)
