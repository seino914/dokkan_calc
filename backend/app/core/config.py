"""
ドッカンバトル ダメージ計算アプリケーション - 設定管理

アプリケーションの設定値と環境変数を管理します。
"""

import os
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """
    アプリケーション設定クラス
    """
    
    # アプリケーション基本設定
    app_name: str = Field(default="ドッカンバトル ダメージ計算 API", description="アプリケーション名")
    app_version: str = Field(default="1.0.0", description="アプリケーションバージョン")
    debug: bool = Field(default=False, description="デバッグモード")
    
    # サーバー設定
    host: str = Field(default="0.0.0.0", description="サーバーホスト")
    port: int = Field(default=8000, description="サーバーポート")
    
    # CORS設定
    allowed_origins: List[str] = Field(
        default=["http://localhost:3000", "http://127.0.0.1:3000"],
        description="許可するオリジン一覧"
    )
    
    # 外部API設定
    external_api_base_url: str = Field(
        default="https://api.dokkan.example.com",
        description="外部キャラクターAPIのベースURL"
    )
    external_api_timeout: int = Field(default=30, description="外部API タイムアウト（秒）")
    external_api_retry_count: int = Field(default=3, description="外部API リトライ回数")
    
    # データベース設定（将来の拡張用）
    database_url: str = Field(
        default="postgresql://user:password@localhost/dokkan_calc",
        description="データベース接続URL"
    )
    
    # キャッシュ設定
    cache_ttl: int = Field(default=3600, description="キャッシュ有効期限（秒）")
    
    # ログ設定
    log_level: str = Field(default="INFO", description="ログレベル")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# グローバル設定インスタンス
settings = Settings()


def get_settings() -> Settings:
    """
    設定インスタンスを取得する関数
    
    Returns:
        Settings: アプリケーション設定
    """
    return settings