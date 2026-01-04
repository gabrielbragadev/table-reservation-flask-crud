import pytest
from app import create_app
from app.extensions import db


@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True

    with app.app_context():
        yield app


@pytest.fixture
def db_session(app):
    db.drop_all()
    db.create_all()

    yield db.session

    db.session.remove()
    db.drop_all()
