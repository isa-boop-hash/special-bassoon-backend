from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Monster, User

monster_bp = Blueprint('monster', __name__)

@monster_bp.route('', methods=['GET'])
def get_monsters():
    monsters = Monster.query.all()
    return {'monsters': [m.to_dict() for m in monsters]}, 200


@monster_bp.route('/<monster_id>', methods=['GET'])
def get_monster(monster_id):
    monster = Monster.query.get(monster_id)
    
    if not monster:
        return {'error': 'モンスターが見つかりません'}, 404
    
    return {'monster': monster.to_dict()}, 200


@monster_bp.route('', methods=['POST'])
@jwt_required()
def create_monster():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data.get('name'):
        return {'error': 'モンスター名は必須です'}, 400
    
    monster = Monster(
        user_id=user_id,
        name=data['name'],
        level=data.get('level', 1),
        description=data.get('description'),
        emoji=data.get('emoji', '🐉'),
    )
    
    db.session.add(monster)
    db.session.commit()
    
    return {'message': 'モンスターを作成しました', 'monster': monster.to_dict()}, 201


@monster_bp.route('/<monster_id>', methods=['PUT'])
@jwt_required()
def update_monster(monster_id):
    user_id = get_jwt_identity()
    monster = Monster.query.get(monster_id)
    
    if not monster:
        return {'error': 'モンスターが見つかりません'}, 404
    
    if monster.user_id != user_id:
        return {'error': '権限がありません'}, 403
    
    data = request.get_json()
    
    if 'name' in data:
        monster.name = data['name']
    if 'level' in data:
        monster.level = data['level']
    if 'description' in data:
        monster.description = data['description']
    if 'emoji' in data:
        monster.emoji = data['emoji']
    
    db.session.commit()
    
    return {'message': '更新しました', 'monster': monster.to_dict()}, 200


@monster_bp.route('/<monster_id>', methods=['DELETE'])
@jwt_required()
def delete_monster(monster_id):
    user_id = get_jwt_identity()
    monster = Monster.query.get(monster_id)
    
    if not monster:
        return {'error': 'モンスターが見つかりません'}, 404
    
    if monster.user_id != user_id:
        return {'error': '権限がありません'}, 403
    
    db.session.delete(monster)
    db.session.commit()
    
    return {'message': '削除しました'}, 200
