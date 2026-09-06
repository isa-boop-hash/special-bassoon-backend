from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Comment, Like, BattleVideo

interaction_bp = Blueprint('interaction', __name__)

# コメント API
@interaction_bp.route('/videos/<video_id>/comments', methods=['GET'])
def get_comments(video_id):
    video = BattleVideo.query.get(video_id)
    if not video:
        return {'error': '動画が見つかりません'}, 404
    
    comments = Comment.query.filter_by(battle_video_id=video_id).order_by(Comment.created_at.desc()).all()
    return {'comments': [c.to_dict() for c in comments]}, 200


@interaction_bp.route('/videos/<video_id>/comments', methods=['POST'])
@jwt_required()
def create_comment(video_id):
    user_id = get_jwt_identity()
    
    video = BattleVideo.query.get(video_id)
    if not video:
        return {'error': '動画が見つかりません'}, 404
    
    data = request.get_json()
    
    if not data.get('content'):
        return {'error': 'コメント内容は必須です'}, 400
    
    comment = Comment(
        user_id=user_id,
        battle_video_id=video_id,
        content=data['content'],
    )
    
    db.session.add(comment)
    db.session.commit()
    
    return {'message': 'コメントを追加しました', 'comment': comment.to_dict()}, 201


@interaction_bp.route('/comments/<comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(comment_id):
    user_id = get_jwt_identity()
    comment = Comment.query.get(comment_id)
    
    if not comment:
        return {'error': 'コメントが見つかりません'}, 404
    
    if comment.user_id != user_id:
        return {'error': '権限がありません'}, 403
    
    db.session.delete(comment)
    db.session.commit()
    
    return {'message': '削除しました'}, 200


# いいね API
@interaction_bp.route('/videos/<video_id>/likes', methods=['GET'])
def get_likes(video_id):
    video = BattleVideo.query.get(video_id)
    if not video:
        return {'error': '動画が見つかりません'}, 404
    
    likes = Like.query.filter_by(battle_video_id=video_id).all()
    return {'likes_count': len(likes), 'likes': [l.to_dict() for l in likes]}, 200


@interaction_bp.route('/videos/<video_id>/likes', methods=['POST'])
@jwt_required()
def add_like(video_id):
    user_id = get_jwt_identity()
    
    video = BattleVideo.query.get(video_id)
    if not video:
        return {'error': '動画が見つかりません'}, 404
    
    # 既にいいんしているか確認
    existing_like = Like.query.filter_by(user_id=user_id, battle_video_id=video_id).first()
    if existing_like:
        return {'error': '既にいいね済みです'}, 409
    
    like = Like(user_id=user_id, battle_video_id=video_id)
    
    db.session.add(like)
    video.likes_count += 1
    db.session.commit()
    
    return {'message': 'いいねしました', 'like': like.to_dict()}, 201


@interaction_bp.route('/videos/<video_id>/likes', methods=['DELETE'])
@jwt_required()
def remove_like(video_id):
    user_id = get_jwt_identity()
    
    video = BattleVideo.query.get(video_id)
    if not video:
        return {'error': '動画が見つかりません'}, 404
    
    like = Like.query.filter_by(user_id=user_id, battle_video_id=video_id).first()
    if not like:
        return {'error': 'いいねが見つかりません'}, 404
    
    db.session.delete(like)
    video.likes_count -= 1
    db.session.commit()
    
    return {'message': 'いいねを取り消しました'}, 200
