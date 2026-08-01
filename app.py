from flask import Flask
from extensions import db, login_manager
from models.scan import Scan
from flask import render_template




def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    # Import models (AFTER app + db init)
    from models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from routes.auth import auth_bp
    from routes.user import user_bp
    from routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)

    @app.route("/")
    def home():
        return render_template("home.html")
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)


app = Flask(__name__)

app.secret_key = "phishguard_secret_key_2026"