from flask import Flask, request, redirect, jsonify, session 
from model import db, URL
from auth import auth
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager 
import string
import random 

app = Flask(__name__)
app.register_blueprint(auth, url_prefix="/api/auth")
app.config["JWT_SECRET_KEY"] = "super-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///urls.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

jwt = JWTManager(app)
db.init_app(app)


def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))
    return "".join(random.choice(characters) for _ in range(length))

@app.route("/api/shorten", methods=["POST"])
@jwt_required()
def shorten_url():
    data = request.get_json()

    if not data or "url" not in data:
        return jsonify({"error": "URL is required"}), 404

    original_url = data["url"]
    custom_code = data.get("custom_code")

    if custom_code:
        existing_url = URL.query.filter_by(short_code=custom_code).first()
        if existing_url:
            return jsonify({"error": "Custom code already in use"}), 409
        
        short_code = custom_code
    else:
        short_code = generate_short_code()

        while URL.query.filter_by(short_code=short_code).first():
            short_code = generate_short_code()

    new_url = URL(original_url=original_url, short_code=short_code)
    db.session.add(new_url)
    db.session.commit()

    return jsonify({original_url: request.host_url + short_code}), 201

@app.route("/api/stats/<short_code>", methods=["GET"])
def get_stats(short_code):
    url = URL.query.filter_by(short_code=short_code).first()

    if not url:
        return jsonify({"error": "URL not found"}), 404

    return jsonify({
        "original_url": url.original_url,
        "short_code": url.short_code,
        "clicks": url.clicks
    }), 200


@app.route("/<short_code>", methods=["GET"])
def redirect_to_original_url(short_code):
    url = URL.query.filter_by(short_code=short_code).first()
    
    if not url:
        return jsonify({"error": "URL not found"}), 404
    
    url.clicks += 1
    db.session.commit()

    return redirect(url.original_url)
    
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)