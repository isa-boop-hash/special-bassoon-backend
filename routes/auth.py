from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User
import re

auth_bp = Blueprint('auth', __name__)

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # バリデーション
    if not data.get('username') or not data.get('email') or not data.get('password'):
        return {'error': 'ユーザー名、メール、パスワードは必須です'}, 400
    
    if not validate_email(data['email']):
        return {'error': 'メールアドレスが無効です'}, 400
    
    if len(data['password']) < 6:
        return {'error': 'パスワードは6文字以上である必要があります'}, 400
    
    # 既存ユーザーの確認
    if User.query.filter_by(username=data['username']).first():
        return {'error': 'このユーザー名は既に使用されています'}, 409
    
    if User.query.filter_by(email=data['email']).first():
        return {'error': 'このメールアドレスは既に登録されています'}, 409
    
    # ユーザー作成
    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    
    access_token = create_access_token(identity=user.id)
    
    return {
        'message': '登録成功',
        'token': access_token,
        'user': user.to_dict(),
    }, 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data.get('email') or not data.get('password'):
        return {'error': 'メールとパスワードは必須です'}, 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.check_password(data['password']):
        return {'error': 'メールまたはパスワードが不正です'}, 401
    
    access_token = create_access_token(identity=user.id)
    
    return {
        'message': 'ログイン成功',
        'token': access_token,
        'user': user.to_dict(),
    }, 200


@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return {'error': 'ユーザーが見つかりません'}, 404
    
    return {'user': user.to_dict()}, 200


@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return {'error': 'ユーザーが見つかりません'}, 404
    
    data = request.get_json()
    
    if 'username' in data:
        if User.query.filter_by(username=data['username']).filter(User.id != user_id).first():
            return {'error': 'このユーザー名は既に使用されています'}, 409
        user.username = data['username']
    
    db.session.commit()
    
    return {'message': '更新成功', 'user': user.to_dict()}, 200
