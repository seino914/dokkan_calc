"""
ドッカンバトル ダメージ計算アプリケーション - メインエントリーポイント

FastAPI アプリケーションの初期化とルーティング設定を行います。
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import logging

from app.api.routes import api_router, health_router
from app.core.config import get_settings

# 環境変数の読み込み
load_dotenv()

# 設定の取得
settings = get_settings()

# ログ設定
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# FastAPI アプリケーションの初期化
app = FastAPI(
    title=settings.app_name,
    description="ドラゴンボール Z ドッカンバトルのダメージ計算を行うAPI",
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS設定 - フロントエンドからのアクセスを許可
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーターの登録
app.include_router(health_router)
app.include_router(api_router)

logger.info(f"アプリケーション初期化完了: {settings.app_name} v{settings.app_version}")


if __name__ == "__main__":
    import uvicorn
    
    # 開発環境での実行設定
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # 開発時の自動リロード
        log_level="info"
    )