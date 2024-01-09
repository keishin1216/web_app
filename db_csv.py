import sqlite3
import csv
from ap import User, Post  # ap.py の中で定義されたモデル

# SQLiteデータベースに接続
db = sqlite3.connect('tour.db')
c = db.cursor()

# 特定のユーザの名前
target_user_name = 'kkk'  # ユーザ名を実際のユーザ名に変更してください

# 対象のユーザを取得
c.execute('SELECT * FROM User WHERE user_name = ?', (target_user_name,))
result = c.fetchone()

if result:
    # ユーザが見つかった場合
    user_id = result[0]

    # 対象のユーザの投稿を取得
    c.execute('SELECT * FROM Post WHERE user_id = ?', (user_id,))
    posts = c.fetchall()

    # CSVファイルへの書き込み
    with open(f'{target_user_name}_exported_data.csv', 'w', newline='') as csvfile:
        fieldnames = ['id', 'user_id', 'create_at', 't', 'impression', 'impression_counts', 'lat', 'lon']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # CSVファイルのヘッダーを書き込む
        writer.writeheader()

        # データをCSVファイルに書き込む
        for post in posts:
            writer.writerow({
                'id': post[0],
                'user_id': post[1],
                'create_at': post[2],
                't': post[3],
                'impression': post[4],
                'impression_counts': post[5],
                'lat': post[6],
                'lon': post[7]
            })

    print(f'Data for {target_user_name} exported successfully.')
else:
    print(f'User with user_name={target_user_name} not found.')

# カーソルと接続を閉じる
c.close()
db.close()
