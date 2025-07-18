# 要件定義書

## 概要

本文書は、ドラゴンボール Z ドッカンバトルのダメージ計算アプリケーションの要件を定義します。このシステムでは、ユーザーがキャラクターの防御ステータス、リーダースキル倍率、キャラクター情報、敵の攻撃値を入力して、受けるダメージを計算できます。アプリケーションは、Next.js の Web フロントエンドと FastAPI バックエンド、Supabase データベース統合で構成され、将来のモバイルアプリ開発に拡張可能な設計となっています。

## 要件

### 要件 1

**ユーザーストーリー:** ドッカンバトルプレイヤーとして、キャラクターの防御ステータスとバトルパラメータを入力して、敵の攻撃からどれだけのダメージを受けるかを計算したい。

#### 受入基準

1. ユーザーが Web アプリケーションにアクセスした時、システムは DEF ステータス、リーダースキル倍率、キャラクター選択、敵アタック値の入力フィールドを表示する
2. ユーザーが DEF ステータスフィールドに有効な数値を入力した時、システムは入力を受け入れて保存する
3. ユーザーが有効なリーダースキル倍率を入力した時、システムはパーセンテージ倍率を表す値を受け入れる
4. ユーザーがキャラクターを選択した時、システムは外部 API から利用可能なキャラクターを取得して表示する
5. ユーザーが敵アタック値を入力した時、システムは有効な数値入力を受け入れる

### 要件 2

**ユーザーストーリー:** ドッカンバトルプレイヤーとして、システムにキャラクターの実効防御力を計算してもらい、すべての修正値を適用した後の防御能力を理解したい。

#### 受入基準

1. ユーザーが計算ボタンをクリックした時、システムは DEF ステータスにリーダースキル倍率を適用して処理する
2. 実効防御力を計算する時、システムは選択されたキャラクターのパッシブスキル修正値を適用する
3. キャラクターが DEF 無限上昇能力を持つ場合、システムは実行された攻撃回数を考慮する
4. キャラクターがダメージ軽減能力を持つ場合、システムは適切な軽減計算を適用する
5. キャラクターが全属性ガード能力を持つ場合、システムは最終結果にガード計算を適用する

### 要件 3

**ユーザーストーリー:** ドッカンバトルプレイヤーとして、受けるダメージの計算結果を見て、バトルで戦略的な判断を下したい。

#### 受入基準

1. 防御計算が完了した時、システムは実効防御力と敵アタック値を比較する
2. 実効防御力が敵アタックを上回る場合、システムは最小またはゼロダメージを返す
3. 敵アタックが実効防御力を上回る場合、システムは受けるダメージを計算して返す
4. 結果がマイナス（防御力が攻撃力を下回る）の場合、システムは受けるダメージを正の値として返す
5. 計算が完了した時、システムはフロントエンドに結果を明確に表示する

### 要件 4

**ユーザーストーリー:** 開発者として、スケーラブルなバックエンド API アーキテクチャを構築し、モバイルアプリケーションや追加機能に拡張できるようにしたい。

#### 受入基準

1. バックエンドが実装される時、システムは RESTful API 設計で FastAPI フレームワークを使用する
2. データベース操作が必要な時、システムは Supabase 統合で SQLAlchemy を使用する
3. API エンドポイントが作成される時、システムはリソース管理に REST 規約に従う
4. レスポンスが送信される時、システムは適切な HTTP ステータスコードで JSON 形式のデータを返す
5. システムがデプロイされる時、システムはローカル開発環境と本番環境の両方をサポートする

### 要件 5

**ユーザーストーリー:** 開発者として、外部 API からのキャラクターデータ統合を適切に管理し、パッシブスキルとキャラクター情報を効率的に処理できるようにしたい。

#### 受入基準

1. 外部 API が呼び出される時、システムは適切なエラーハンドリングとタイムアウト処理を実装する
2. パッシブスキル計算が必要な時、システムは異なるスキルタイプに対してモジュラー関数構造を持つ
3. 外部 API からキャラクターデータを取得する時、システムはレスポンスデータの検証と正規化を行う
4. API レスポンスが遅い場合、システムはローディング状態をユーザーに表示する
5. 外部 API が利用できない場合、システムは適切なエラーメッセージをユーザーに表示する

### 要件 6

**ユーザーストーリー:** ドッカンバトルプレイヤーとして、DEF 無限上昇などの特殊なキャラクターメカニクスを処理し、すべてのキャラクタータイプの防御力を正確に計算したい。

#### 受入基準

1. キャラクターが DEF 無限上昇を持つ場合、システムは実行された攻撃回数の入力フィールドを提供する
2. スタッキング防御を計算する時、システムは攻撃回数に基づいて段階的な防御力増加を適用する
3. キャラクターが複数のパッシブ効果を持つ場合、システムは正しい順序ですべての関連修正値を適用する
4. パッシブスキルデータが不完全な場合、システムは後で実装可能なプレースホルダー関数を使用する
5. スタッキングキャラクターの結果を表示する時、システムはベース防御力とスタック後防御力の両方を表示する
