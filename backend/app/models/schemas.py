"""
ドッカンバトル ダメージ計算アプリケーション - データスキーマ定義

Pydantic を使用したデータモデルとバリデーション機能を提供します。
"""

from typing import List, Optional, Literal
from pydantic import BaseModel, Field, validator


class PassiveSkill(BaseModel):
    """
    パッシブスキルのデータモデル
    """
    id: str = Field(..., description="パッシブスキルの一意識別子")
    type: Literal["defense_boost", "damage_reduction", "guard", "infinite_stacking"] = Field(
        ..., description="スキルタイプ"
    )
    value: float = Field(..., ge=0, description="スキル効果値（0以上）")
    condition: Optional[str] = Field(None, description="発動条件")
    stackable: bool = Field(default=False, description="スタック可能かどうか")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "def_boost_1",
                "type": "defense_boost",
                "value": 120.0,
                "condition": "HP 80%以上時",
                "stackable": False
            }
        }


class Character(BaseModel):
    """
    キャラクターのデータモデル
    """
    id: str = Field(..., description="キャラクターの一意識別子")
    name: str = Field(..., min_length=1, description="キャラクター名")
    rarity: int = Field(..., ge=1, le=6, description="レアリティ（1-6星）")
    type: str = Field(..., description="属性タイプ（AGL, TEQ, INT, STR, PHY）")
    passive_skills: List[PassiveSkill] = Field(default=[], description="パッシブスキル一覧")
    defense_multiplier: Optional[float] = Field(None, ge=0, description="防御力倍率")
    damage_reduction: Optional[float] = Field(None, ge=0, le=100, description="ダメージ軽減率（0-100%）")
    guard_ability: Optional[bool] = Field(default=False, description="ガード能力の有無")
    infinite_defense_stacking: Optional[bool] = Field(default=False, description="DEF無限上昇能力の有無")

    @validator('type')
    def validate_type(cls, v):
        """属性タイプのバリデーション"""
        valid_types = ['AGL', 'TEQ', 'INT', 'STR', 'PHY']
        if v.upper() not in valid_types:
            raise ValueError(f'属性タイプは {valid_types} のいずれかである必要があります')
        return v.upper()

    class Config:
        json_schema_extra = {
            "example": {
                "id": "goku_ui",
                "name": "孫悟空（身勝手の極意）",
                "rarity": 6,
                "type": "AGL",
                "passive_skills": [],
                "defense_multiplier": 150.0,
                "damage_reduction": 30.0,
                "guard_ability": True,
                "infinite_defense_stacking": False
            }
        }


class DamageCalculationRequest(BaseModel):
    """
    ダメージ計算リクエストのデータモデル
    """
    def_stat: int = Field(..., ge=0, description="DEFステータス値（0以上）")
    leader_skill_multiplier: float = Field(..., ge=1.0, description="リーダースキル倍率（1.0以上）")
    character_id: str = Field(..., description="選択されたキャラクターのID")
    enemy_attack: int = Field(..., ge=0, description="敵の攻撃値（0以上）")
    attack_count: Optional[int] = Field(default=0, ge=0, description="攻撃回数（DEF無限上昇用、0以上）")

    @validator('leader_skill_multiplier')
    def validate_leader_skill_multiplier(cls, v):
        """リーダースキル倍率のバリデーション"""
        if v > 10.0:  # 現実的な上限値
            raise ValueError('リーダースキル倍率は10.0以下である必要があります')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "def_stat": 15000,
                "leader_skill_multiplier": 1.7,
                "character_id": "goku_ui",
                "enemy_attack": 50000,
                "attack_count": 3
            }
        }


class AppliedModifiers(BaseModel):
    """
    適用された修正値の詳細
    """
    leader_skill: float = Field(..., description="リーダースキル倍率")
    passive_skills: List[PassiveSkill] = Field(default=[], description="適用されたパッシブスキル一覧")
    stacking_bonus: Optional[float] = Field(None, description="スタッキングボーナス（DEF無限上昇用）")


class DamageCalculationResult(BaseModel):
    """
    ダメージ計算結果のデータモデル
    """
    effective_defense: float = Field(..., ge=0, description="実効防御力")
    damage_received: float = Field(..., ge=0, description="受けるダメージ")
    applied_modifiers: AppliedModifiers = Field(..., description="適用された修正値の詳細")
    calculation_details: str = Field(..., description="計算詳細の説明文")

    class Config:
        json_schema_extra = {
            "example": {
                "effective_defense": 25500.0,
                "damage_received": 24500.0,
                "applied_modifiers": {
                    "leader_skill": 1.7,
                    "passive_skills": [],
                    "stacking_bonus": None
                },
                "calculation_details": "DEF 15000 × リーダースキル 1.7 = 実効防御力 25500、受けるダメージ 24500"
            }
        }


class ApiError(BaseModel):
    """
    API エラーレスポンスのデータモデル
    """
    code: str = Field(..., description="エラーコード")
    message: str = Field(..., description="エラーメッセージ")
    details: Optional[str] = Field(None, description="エラー詳細")

    class Config:
        json_schema_extra = {
            "example": {
                "code": "VALIDATION_ERROR",
                "message": "入力データが無効です",
                "details": "DEFステータスは0以上の値である必要があります"
            }
        }


class HealthCheckResponse(BaseModel):
    """
    ヘルスチェックレスポンスのデータモデル
    """
    status: str = Field(..., description="サービスの状態")
    service: str = Field(..., description="サービス名")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "service": "dokkan-damage-calculator-api"
            }
        }