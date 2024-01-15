import pandas as pd
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz
from ap import app, User, Post  # ap.py内のFlaskアプリケーションおよびモデルをインポート

# Flaskアプリケーションのコンテキストを手動で作成
with app.app_context():
    # ユーザー 'renshu' の情報を取得
    user = User.query.filter_by(user_name='a').first()
    users = User.query.all()
    for u in users:
     print(u.user_name)
    if user:
        # ユーザーに関連する投稿データを取得
        user_posts = Post.query.filter_by(user_id=user.id).all()

        # 取得したデータをDataFrameに変換
        data = {
            'id': [post.id for post in user_posts],
            'user_id': [post.user_id for post in user_posts],
            'create_at': [post.create_at for post in user_posts],
            't': [post.t for post in user_posts],
            'impression': [post.impression for post in user_posts],
            'impression_counts': [post.impression_counts for post in user_posts],
            'lat': [post.lat for post in user_posts],
            'lon': [post.lon for post in user_posts]
        }
        df = pd.DataFrame(data)

        
        df.to_csv('output23.csv', index=False)
        print("CSV")
    else:
        print("User 'db' not found.")
