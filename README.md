# ドッカンバトル ダメージ計算ツール

ドラゴンボール Z ドッカンバトルのキャラクター防御力とダメージを正確に計算する Web アプリケーションです。

## 概要

このアプリケーションでは、以下の機能を提供します：

- キャラクターの防御ステータス（DEF）とリーダースキル倍率を考慮した実効防御力の計算
- パッシブスキル（DEF 無限上昇、ダメージ軽減、ガード能力など）の適用
- 敵の攻撃値に対する受けるダメージの算出
- 計算過程と適用された修正値の詳細表示

## 技術スタック

### フロントエンド

- **Next.js 14** - React フレームワーク
- **TypeScript** - 型安全性の確保
- **Tailwind CSS** - スタイリング
- **React** - UI コンポーネント

### バックエンド

- **FastAPI** - Python Web フレームワーク
- **Pydantic** - データバリデーション
- **httpx** - 外部 API 通信
- **SQLAlchemy** - データベース ORM（将来の拡張用）

### データベース

- **Supabase (PostgreSQL)** - データ永続化（将来の拡張用）

## プロジェクト構造

```
/
├── frontend/           # Next.js フロントエンドアプリケーション
│   ├── src/
│   │   ├── app/       # App Router ページ
│   │   └── types/     # TypeScript 型定義
│   └── package.json
├── backend/            # FastAPI バックエンドアプリケーション
│   ├── app/
│   │   ├── api/       # API ルーター
│   │   ├── core/      # 設定とコア機能
│   │   ├── models/    # データモデル
│   │   └── services/  # ビジネスロジック
│   ├── tests/         # テストファイル
│   ├── main.py        # アプリケーションエントリーポイント
│   └── requirements.txt
└── .kiro/             # Kiro AI 設定
    └── specs/         # 機能仕様書
```

## セットアップ

### 前提条件

- Node.js 18.0.0 以上
- Python 3.11 以上
- npm または yarn

### フロントエンド

```bash
cd frontend
npm install
npm run dev
```

フロントエンドは http://localhost:3000 で起動します。

### バックエンド

```bash
cd backend

# 仮想環境の作成（推奨）
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 依存関係のインストール
pip install -r requirements.txt

# 環境変数の設定
cp .env.example .env
# .env ファイルを編集して適切な値を設定

# アプリケーションの起動
python main.py
```

バックエンドは http://localhost:8000 で起動します。
API ドキュメントは http://localhost:8000/docs で確認できます。

## 開発

### コード品質

- **フロントエンド**: ESLint + Prettier
- **バックエンド**: Black + isort + flake8

### テスト

- **フロントエンド**: Jest + React Testing Library
- **バックエンド**: pytest

## API エンドポイント

### ダメージ計算

```
POST /api/calculate-damage
```

リクエスト例：

```json
{
  "def_stat": 15000,
  "leader_skill_multiplier": 1.7,
  "character_id": "goku_ui",
  "enemy_attack": 50000,
  "attack_count": 3
}
```

### キャラクター取得

```
GET /api/characters
GET /api/characters/{character_id}
```

## ライセンス

このプロジェクトは MIT ライセンスの下で公開されています。

## 貢献

プルリクエストやイシューの報告を歓迎します。開発に参加する場合は、まずイシューを作成して議論してください。
