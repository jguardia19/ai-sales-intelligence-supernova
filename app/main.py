from flask import Flask, jsonify
from flask_cors import CORS

from app.api.v1.api import api_v1_bp


def create_app():
    app = Flask(__name__)

    origins = [
        "http://localhost:9000",
        "http://localhost:9001",
        "http://127.0.0.1:9000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    CORS(
        app,
        resources={r"/*": {"origins": origins}},
        supports_credentials=True
    )

    app.register_blueprint(api_v1_bp)

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "ok"})

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)