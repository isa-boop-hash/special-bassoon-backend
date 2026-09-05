from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import uuid

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # リレーション
    monsters = db.relationship('Monster', backref='owner', lazy=True, cascade='all, delete-orphan')
    battle_videos = db.relationship('BattleVideo', backref='uploader', lazy=True, cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='user', lazy=True, cascade='all, delete-orphan')
    likes = db.relationship('Like', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
        }


class Monster(db.Model):
    __tablename__ = 'monsters'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    level = db.Column(db.Integer, default=1)
    description = db.Column(db.Text)
    emoji = db.Column(db.String(10), default='🐉')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # リレーション
    battle_videos = db.relationship('BattleVideo', backref='monster', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'level': self.level,
            'description': self.description,
            'emoji': self.emoji,
            'created_at': self.created_at.isoformat(),
        }


class BattleVideo(db.Model):
    __tablename__ = 'battle_videos'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    monster_id = db.Column(db.String(36), db.ForeignKey('monsters.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    video_url = db.Column(db.String(255), nullable=False)
    battle_result = db.Column(db.String(20), nullable=False)  # 'win', 'loss', 'draw'
    likes_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # リレーション
    comments = db.relationship('Comment', backref='battle_video', lazy=True, cascade='all, delete-orphan')
    likes = db.relationship('Like', backref='battle_video', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'monster_id': self.monster_id,
            'title': self.title,
            'description': self.description,
            'video_url': self.video_url,
            'battle_result': self.battle_result,
            'likes_count': self.likes_count,
            'uploader': self.uploader.to_dict() if self.uploader else None,
            'monster': self.monster.to_dict() if self.monster else None,
            'created_at': self.created_at.isoformat(),
        }


class Comment(db.Model):
    __tablename__ = 'comments'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    battle_video_id = db.Column(db.String(36), db.ForeignKey('battle_videos.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'battle_video_id': self.battle_video_id,
            'content': self.content,
            'user': self.user.to_dict() if self.user else None,
            'created_at': self.created_at.isoformat(),
        }


class Like(db.Model):
    __tablename__ = 'likes'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    battle_video_id = db.Column(db.String(36), db.ForeignKey('battle_videos.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # ユーザーと動画の組み合わせはユニークであるべき
    __table_args__ = (db.UniqueConstraint('user_id', 'battle_video_id', name='unique_user_video_like'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'battle_video_id': self.battle_video_id,
            'created_at': self.created_at.isoformat(),
        }
