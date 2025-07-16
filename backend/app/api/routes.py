"""
ドッカンバトル ダメージ計算アプリケーション - API ルーター

FastAPI のルーティング設定とエンドポイント定義を管理します。
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List

from ..models.schemas import (
    Character,
    DamageCalculationRequest,
    DamageCalculationResult,
    ApiError,
    HealthCheckResponse
)
from ..services.damage_calculator import DamageCalculatorService
from ..services.character_service import CharacterService
from ..core.config import get_settings, Settings

# APIルーターの初期化
api_router = APIRouter(prefix="/api", tags=["api"])

# サービス依存関係の設定
def get_damage_calculator_service() -> DamageCalculatorService:
    """ダメージ計算サービスのインスタンスを取得"""
    return DamageCalculatorService()

def get_character_service() -> CharacterService:
    """キャラクターサービスのインスタンスを取得"""
    return CharacterService()


@api_router.post(
    "/calculate-damage",
    response_model=DamageCalculationResult,
    summary="ダメージ計算",
    description="キャラクターの防御ステータスと敵の攻撃値からダメージを計算します"
)
async def calculate_damage(
    request: DamageCalculationRequest,
    calculator_service: DamageCalculatorService = Depends(get_damage_calculator_service),
    character_service: CharacterService = Depends(get_character_service)
) -> DamageCalculationResult:
    """
    ダメージ計算エンドポイント
    
    Args:
        request: ダメージ計算リクエストデータ
        calculator_service: ダメージ計算サービス
        character_service: キャラクターサービス
        
    Returns:
        DamageCalculationResult: 計算結果
        
    Raises:
        HTTPException: キャラクターが見つからない場合や計算エラーの場合
    """
    try:
        # キャラクター情報の取得
        character = await character_service.get_character(request.character_id)
        if not character:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "CHARACTER_NOT_FOUND",
                    "message": f"キャラクターID '{request.character_id}' が見つかりません",
                    "details": "有効なキャラクターIDを指定してください"
                }
            )
        
        # ダメージ計算の実行
        result = await calculator_service.calculate_damage(request, character)
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "code": "CALCULATION_ERROR",
                "message": "ダメージ計算中にエラーが発生しました",
                "details": str(e)
            }
        )


@api_router.get(
    "/characters",
    response_model=List[Character],
    summary="キャラクター一覧取得",
    description="利用可能なキャラクターの一覧を取得します"
)
async def get_characters(
    character_service: CharacterService = Depends(get_character_service)
) -> List[Character]:
    """
    キャラクター一覧取得エンドポイント
    
    Args:
        character_service: キャラクターサービス
        
    Returns:
        List[Character]: キャラクター一覧
        
    Raises:
        HTTPException: 外部API接続エラーの場合
    """
    try:
        characters = await character_service.get_characters()
        return characters
        
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail={
                "code": "EXTERNAL_API_ERROR",
                "message": "キャラクターデータの取得に失敗しました",
                "details": str(e)
            }
        )


@api_router.get(
    "/characters/{character_id}",
    response_model=Character,
    summary="キャラクター詳細取得",
    description="指定されたIDのキャラクター詳細情報を取得します"
)
async def get_character(
    character_id: str,
    character_service: CharacterService = Depends(get_character_service)
) -> Character:
    """
    キャラクター詳細取得エンドポイント
    
    Args:
        character_id: キャラクターID
        character_service: キャラクターサービス
        
    Returns:
        Character: キャラクター詳細情報
        
    Raises:
        HTTPException: キャラクターが見つからない場合
    """
    try:
        character = await character_service.get_character(character_id)
        if not character:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "CHARACTER_NOT_FOUND",
                    "message": f"キャラクターID '{character_id}' が見つかりません",
                    "details": "有効なキャラクターIDを指定してください"
                }
            )
        
        return character
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail={
                "code": "EXTERNAL_API_ERROR",
                "message": "キャラクターデータの取得に失敗しました",
                "details": str(e)
            }
        )


# ヘルスチェックエンドポイント（ルートレベル）
health_router = APIRouter(tags=["health"])

@health_router.get(
    "/health",
    response_model=HealthCheckResponse,
    summary="ヘルスチェック",
    description="APIサーバーの稼働状況を確認します"
)
async def health_check(
    settings: Settings = Depends(get_settings)
) -> HealthCheckResponse:
    """
    ヘルスチェックエンドポイント
    
    Args:
        settings: アプリケーション設定
        
    Returns:
        HealthCheckResponse: サーバー稼働状況
    """
    return HealthCheckResponse(
        status="healthy",
        service="dokkan-damage-calculator-api"
    )


@health_router.get(
    "/",
    summary="ルートエンドポイント",
    description="API の基本情報を返します"
)
async def root(settings: Settings = Depends(get_settings)):
    """
    ルートエンドポイント
    
    Args:
        settings: アプリケーション設定
        
    Returns:
        dict: API基本情報
    """
    return {
        "message": "ドッカンバトル ダメージ計算 API へようこそ",
        "version": settings.app_version,
        "status": "running",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }