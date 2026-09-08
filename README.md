# バトル動画プラットフォーム - バックエンド API

**モンスターバトル動画をアップロード・共有するプラットフォーム**

## 📋 機能

- ✅ ユーザー認証（登録/ログイン）
- ✅ モンスター管理（作成/編集/削除）
- ✅ バトル動画アップロード
- ✅ コメント機能
- ✅ いいね機能
- ✅ JWT 認証

## 🛠️ 技術スタック

- **言語**: Python 3.9
- **フレームワーク**: Flask
- **データベース**: PostgreSQL
- **認証**: Flask-JWT-Extended
- **API**: RESTful API
- **デプロイ**: Docker, Render

## 📦 インストール

### 1. リポジトリをクローン

```bash
git clone https://github.com/isa-boop-hash/special-bassoon-backend.git
cd special-bassoon-backend
```

### 2. 環境変数を設定

```bash
cp .env.example .env
```

`.env` ファイルを編集：

```env
DATABASE_URL=postgresql://user:password@localhost/battle_videos_db
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
```

### 3. Docker で起動（推奨）

```bash
docker-compose up -d
```

バックエンドが `http://localhost:5000` で起動します。

### 4. ローカルで実行

```bash
pip install -r requirements.txt
flask run
```

## 🔌 API エンドポイント

### 認証

- `POST /api/auth/register` - ユーザー登録
- `POST /api/auth/login` - ログイン
- `GET /api/auth/profile` - プロフィール取得
- `PUT /api/auth/profile` - プロフィール更新

### モンスター

- `GET /api/monsters` - モンスター一覧
- `GET /api/monsters/<id>` - モンスター詳細
- `POST /api/monsters` - モンスター作成
- `PUT /api/monsters/<id>` - モンスター更新
- `DELETE /api/monsters/<id>` - モンスター削除

### バトル動画

- `GET /api/battle-videos` - 動画一覧
- `GET /api/battle-videos/<id>` - 動画詳細
- `POST /api/battle-videos` - 動画アップロード
- `DELETE /api/battle-videos/<id>` - 動画削除

### インタラクション

- `GET /api/interactions/videos/<id>/comments` - コメント一覧
- `POST /api/interactions/videos/<id>/comments` - コメント追加
- `DELETE /api/interactions/comments/<id>` - コメント削除
- `GET /api/interactions/videos/<id>/likes` - いいね一覧
- `POST /api/interactions/videos/<id>/likes` - いいね追加
- `DELETE /api/interactions/videos/<id>/likes` - いいね削除

## 🚀 デプロイ

### Render にデプロイ

1. GitHub に push
2. [Render](https://render.com) にアクセス
3. New Web Service を作成
4. このリポジトリを接続
5. 環境変数を設定
6. Deploy！

## 📄 ライセンス

MIT
