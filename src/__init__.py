import os
from flask import Flask, render_template
from src.routes import app_blueprint
from src import errors
from waitress import serve

app = Flask(__name__)
app.register_blueprint(app_blueprint)
app.secret_key = os.environ.get(
    "FLASK_SECRET_KEY"
)  # run python -c "import secrets; print(secrets.token_hex(32))" for this


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

#
if __name__ == "__main__":
    # app.run(debug=True)
    serve(app, host="0.0.0.0", port=8080)
