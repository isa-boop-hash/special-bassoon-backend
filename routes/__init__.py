from flask import Blueprint

# ブループリントをインポート
from .auth import auth_bp
from .monster import monster_bp
from .battle_video import battle_video_bp
from .interaction import interaction_bp

__all__ = ['auth_bp', 'monster_bp', 'battle_video_bp', 'interaction_bp']
