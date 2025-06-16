from flask import render_template
from src.routes import app_blueprint


@app_blueprint.errorhandler(500)
def internal_error(e):
    return (
        render_template(
            "error.html",
            title=e,
            subtitle="Oops!",
            message="Something went wrong on our end. Please try again later.",
        ),
        500,
    )


@app_blueprint.errorhandler(Exception)
def catch_all(e):
    return (render_template("error.html", title="Error", message=str(e)), 500)
