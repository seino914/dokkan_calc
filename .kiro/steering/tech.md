---
inclusion: always
---

# 技術スタック・開発規約

このプロジェクトの技術基盤と開発実践に関するガイドラインです。

## 技術スタック

- **言語**: 未定（決定時に更新）
- **フレームワーク**: 未定（選択時に更新）
- **データベース**: 未定（実装時に更新）
- **実行環境**: 未定（デプロイ対象決定時に更新）

## 開発ツール

- **バージョン管理**: Git
- **エディタ**: Kiro AI アシスタント対応
- **パッケージマネージャー**: 言語・フレームワーク決定時に更新

## コード品質基準

### 命名規則

- ファイル名: ケバブケース（例: `user-service.js`）
- 変数・関数名: 言語固有の慣例に従う
- 意味のある説明的な名前を使用

### コードスタイル

- 言語固有のスタイルガイドに従う
- 一貫したインデントとフォーマット
- 複雑なロジックには適切なコメントを記述
- 日本語コメントを推奨

### アーキテクチャパターン

- 関心の分離を徹底
- 関連機能は論理的にグループ化
- 共通ユーティリティは適切な場所に配置
- 明確なモジュール境界を維持

### 開発実践

- 意味のあるコミットメッセージ
- 重要な機能にはテストカバレッジを確保
- 適切なドキュメント作成
- セキュリティベストプラクティスの遵守

## プロジェクト構造規約

```
/
├── src/                # メインソースコード
├── tests/              # テストファイル
├── docs/               # ドキュメント
├── config/             # 設定ファイル
└── README.md           # プロジェクト概要
```

## 共通コマンド

技術スタック決定後に以下を更新：

- ビルドコマンド
- テスト実行コマンド
- アプリケーション起動コマンド
- 依存関係インストールコマンド
- コード品質チェックコマンド
