import os
from flask import Flask, jsonify
from backend.config import config_by_name
from backend.extensions import db, migrate

def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # Ensure upload and export directories exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['EXPORT_FOLDER'], exist_ok=True)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints (to be done soon)
    from backend.api.health_routes import health_bp
    from backend.api.project_routes import project_bp
    from backend.api.processing_routes import processing_bp
    from backend.api.export_routes import export_bp
    
    app.register_blueprint(health_bp, url_prefix='/api/v1')
    app.register_blueprint(project_bp, url_prefix='/api/v1/projects')
    app.register_blueprint(processing_bp, url_prefix='/api/v1/projects')
    app.register_blueprint(export_bp, url_prefix='/api/v1/projects')

    # Register global error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({
            "success": False,
            "data": None,
            "error": {
                "code": "NOT_FOUND",
                "message": "The requested URL was not found on the server.",
                "details": {}
            },
            "meta": {}
        }), 404

    @app.errorhandler(Exception)
    def internal_error(error):
        # Log the error in production
        return jsonify({
            "success": False,
            "data": None,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred.",
                "details": {"error": str(error)}
            },
            "meta": {}
        }), 500

    return app

if __name__ == '__main__':
    app = create_app(os.getenv("FLASK_ENV", "development"))
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 5000))
    app.run(host=host, port=port)
