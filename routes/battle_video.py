from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, BattleVideo, Monster, User
from werkzeug.utils import secure_filename
import os
from datetime import datetime

battle_video_bp = Blueprint('battle_video', __name__)

ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}
UPLOAD_FOLDER = 'uploads/videos'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@battle_video_bp.route('', methods=['GET'])
def get_battle_videos():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    query = BattleVideo.query.order_by(BattleVideo.created_at.desc())
    paginated = query.paginate(page=page, per_page=per_page)
    
    return {
        'battle_videos': [v.to_dict() for v in paginated.items],
        'total': paginated.total,
        'pages': paginated.pages,
        'current_page': page,
    }, 200


@battle_video_bp.route('/<video_id>', methods=['GET'])
def get_battle_video(video_id):
    video = BattleVideo.query.get(video_id)
    
    if not video:
        return {'error': '動画が見つかりません'}, 404
    
    return {'battle_video': video.to_dict()}, 200


@battle_video_bp.route('', methods=['POST'])
@jwt_required()
def upload_battle_video():
    user_id = get_jwt_identity()
    
    # ファイルがあるか確認
    if 'video' not in request.files:
        return {'error': '動画ファイルが必要です'}, 400
    
    file = request.files['video']
    
    if file.filename == '':
        return {'error': '動画ファイルを選択してください'}, 400
    
    if not allowed_file(file.filename):
        return {'error': 'サポートされていないファイル形式です'}, 400
    
    # フォームデータから情報を取得
    title = request.form.get('title')
    description = request.form.get('description')
    monster_id = request.form.get('monster_id')
    battle_result = request.form.get('battle_result')
    
    if not title or not monster_id or not battle_result:
        return {'error': 'タイトル、モンスター、結果は必須です'}, 400
    
    if battle_result not in ['win', 'loss', 'draw']:
        return {'error': '結果は win, loss, draw のいずれかである必要があります'}, 400
    
    # モンスターの確認
    monster = Monster.query.get(monster_id)
    if not monster or monster.user_id != user_id:
        return {'error': 'モンスターが見つかりません'}, 404
    
    # ファイルを保存
    filename = secure_filename(f"{datetime.utcnow().timestamp()}_{file.filename}")
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    
    # データベースに記録
    video = BattleVideo(
        user_id=user_id,
        monster_id=monster_id,
        title=title,
        description=description,
        video_url=f"/uploads/videos/{filename}",
        battle_result=battle_result,
    )
    
    db.session.add(video)
    db.session.commit()
    
    return {'message': 'アップロード成功', 'battle_video': video.to_dict()}, 201


@battle_video_bp.route('/<video_id>', methods=['DELETE'])
@jwt_required()
def delete_battle_video(video_id):
    user_id = get_jwt_identity()
    video = BattleVideo.query.get(video_id)
    
    if not video:
        return {'error': '動画が見つかりません'}, 404
    
    if video.user_id != user_id:
        return {'error': '権限がありません'}, 403
    
    # ファイルを削除
    try:
        os.remove(video.video_url)
    except:
        pass
    
    db.session.delete(video)
    db.session.commit()
    
    return {'message': '削除しました'}, 200
