from flask import Blueprint
from app.api.v1.endpoints.rag import rag_bp

api_v1_bp = Blueprint("api_v1", __name__, url_prefix="/api/v1")
api_v1_bp.register_blueprint(rag_bp)