import os
import pytest
from unittest.mock import patch, Mock
from flask import Flask, render_template

from src.routes import app_blueprint


@pytest.fixture(autouse=True)
def test_client():
    app = Flask(
        __name__,
        template_folder=os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "src", "templates")
        ),
    )
    app.secret_key = "test"
    app.register_blueprint(app_blueprint)

    @app.errorhandler(404)
    def page_not_found(e):
        return (
            render_template(
                "error.html",
                title="404",
                subtitle="Page Not Found",
                message="The page you're looking for doesn't exist.",
            ),
            404,
        )

    with app.test_client() as test_client:
        yield test_client
