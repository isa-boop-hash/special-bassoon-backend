from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from models import db
from routes import auth_bp, monster_bp, battle_video_bp, interaction_bp
import os

app = Flask(__name__)
app.config.from_object(Config)

# データベース初期化
db.init_app(app)

# JWT 初期化
jwt = JWTManager(app)

# CORS 設定
CORS(app, resources={r"/api/*": {"origins": "*"}})

# ブループリント登録
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(monster_bp, url_prefix='/api/monsters')
app.register_blueprint(battle_video_bp, url_prefix='/api/battle-videos')
app.register_blueprint(interaction_bp, url_prefix='/api/interactions')

@app.route('/api/health', methods=['GET'])
def health_check():
    return {'status': 'ok'}, 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
