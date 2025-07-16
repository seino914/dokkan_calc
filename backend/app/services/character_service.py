"""
ドッカンバトル ダメージ計算アプリケーション - キャラクターサービス

外部APIからのキャラクターデータ取得と管理を行うサービスクラスです。
"""

from typing import List, Optional, Dict, Any
import asyncio
import logging
from datetime import datetime, timedelta

import httpx

from ..models.schemas import Character, PassiveSkill
from ..core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class CharacterService:
    """
    キャラクターサービスクラス
    
    外部APIからキャラクターデータを取得し、アプリケーション内で使用可能な
    形式に変換・キャッシュする機能を提供します。
    """
    
    def __init__(self):
        self._cache: Dict[str, Any] = {}
        self._cache_timestamps: Dict[str, datetime] = {}
        self._http_client: Optional[httpx.AsyncClient] = None
    
    async def __aenter__(self):
        """非同期コンテキストマネージャーの開始"""
        self._http_client = httpx.AsyncClient(
            timeout=httpx.Timeout(settings.external_api_timeout),
            limits=httpx.Limits(max_keepalive_connections=5, max_connections=10)
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """非同期コンテキストマネージャーの終了"""
        if self._http_client:
            await self._http_client.aclose()
    
    async def get_characters(self) -> List[Character]:
        """
        キャラクター一覧を取得する
        
        Returns:
            List[Character]: キャラクター一覧
            
        Raises:
            Exception: 外部API接続エラーまたはデータ変換エラー
        """
        cache_key = "characters_list"
        
        # キャッシュから取得を試行
        cached_data = self._get_from_cache(cache_key)
        if cached_data is not None:
            logger.info("キャラクター一覧をキャッシュから取得")
            return cached_data
        
        try:
            # 外部APIからデータを取得
            logger.info("外部APIからキャラクター一覧を取得中...")
            raw_characters = await self._fetch_characters_from_api()
            
            # データを正規化してCharacterオブジェクトに変換
            characters = [
                self._normalize_character_data(char_data)
                for char_data in raw_characters
            ]
            
            # キャッシュに保存
            self._save_to_cache(cache_key, characters)
            
            logger.info(f"キャラクター一覧を取得完了: {len(characters)}件")
            return characters
            
        except Exception as e:
            logger.error(f"キャラクター一覧の取得に失敗: {str(e)}")
            
            # フォールバック: モックデータを返す
            logger.info("モックデータを使用してフォールバック")
            return self._get_mock_characters()
    
    async def get_character(self, character_id: str) -> Optional[Character]:
        """
        指定されたIDのキャラクター詳細を取得する
        
        Args:
            character_id: キャラクターID
            
        Returns:
            Optional[Character]: キャラクター詳細（見つからない場合はNone）
            
        Raises:
            Exception: 外部API接続エラーまたはデータ変換エラー
        """
        cache_key = f"character_{character_id}"
        
        # キャッシュから取得を試行
        cached_data = self._get_from_cache(cache_key)
        if cached_data is not None:
            logger.info(f"キャラクター詳細をキャッシュから取得: {character_id}")
            return cached_data
        
        try:
            # 外部APIからデータを取得
            logger.info(f"外部APIからキャラクター詳細を取得中: {character_id}")
            raw_character = await self._fetch_character_from_api(character_id)
            
            if not raw_character:
                logger.warning(f"キャラクターが見つかりません: {character_id}")
                return None
            
            # データを正規化してCharacterオブジェクトに変換
            character = self._normalize_character_data(raw_character)
            
            # キャッシュに保存
            self._save_to_cache(cache_key, character)
            
            logger.info(f"キャラクター詳細を取得完了: {character.name}")
            return character
            
        except Exception as e:
            logger.error(f"キャラクター詳細の取得に失敗: {character_id}, エラー: {str(e)}")
            
            # フォールバック: モックデータから検索
            mock_characters = self._get_mock_characters()
            for char in mock_characters:
                if char.id == character_id:
                    logger.info(f"モックデータからキャラクターを取得: {character_id}")
                    return char
            
            return None
    
    async def _fetch_characters_from_api(self) -> List[Dict[str, Any]]:
        """
        外部APIからキャラクター一覧を取得する
        
        Returns:
            List[Dict[str, Any]]: 外部APIからの生データ
        """
        # TODO: 実際の外部API実装時に置き換え
        # 現在はモックデータを返す
        await asyncio.sleep(0.1)  # API呼び出しのシミュレーション
        
        return [
            {
                "id": "goku_ui",
                "name": "孫悟空（身勝手の極意）",
                "rarity": 6,
                "type": "AGL",
                "defense_multiplier": 150.0,
                "damage_reduction": 30.0,
                "guard_ability": True,
                "infinite_defense_stacking": False,
                "passive_skills": [
                    {
                        "id": "ui_defense",
                        "type": "defense_boost",
                        "value": 120.0,
                        "condition": "HP 80%以上時",
                        "stackable": False
                    }
                ]
            },
            {
                "id": "vegeta_evolution",
                "name": "ベジータ（進化の極限）",
                "rarity": 6,
                "type": "STR",
                "defense_multiplier": 130.0,
                "damage_reduction": 20.0,
                "guard_ability": False,
                "infinite_defense_stacking": True,
                "passive_skills": [
                    {
                        "id": "evolution_stacking",
                        "type": "infinite_stacking",
                        "value": 30.0,
                        "condition": "攻撃時",
                        "stackable": True
                    }
                ]
            }
        ]
    
    async def _fetch_character_from_api(self, character_id: str) -> Optional[Dict[str, Any]]:
        """
        外部APIから特定のキャラクター詳細を取得する
        
        Args:
            character_id: キャラクターID
            
        Returns:
            Optional[Dict[str, Any]]: 外部APIからの生データ
        """
        # TODO: 実際の外部API実装時に置き換え
        # 現在は一覧から該当するものを返す
        characters = await self._fetch_characters_from_api()
        for char in characters:
            if char["id"] == character_id:
                return char
        return None
    
    def _normalize_character_data(self, raw_data: Dict[str, Any]) -> Character:
        """
        外部APIの生データをCharacterオブジェクトに正規化する
        
        Args:
            raw_data: 外部APIからの生データ
            
        Returns:
            Character: 正規化されたキャラクターオブジェクト
        """
        # パッシブスキルの正規化
        passive_skills = []
        for skill_data in raw_data.get("passive_skills", []):
            passive_skill = PassiveSkill(
                id=skill_data["id"],
                type=skill_data["type"],
                value=skill_data["value"],
                condition=skill_data.get("condition"),
                stackable=skill_data.get("stackable", False)
            )
            passive_skills.append(passive_skill)
        
        # Characterオブジェクトの作成
        character = Character(
            id=raw_data["id"],
            name=raw_data["name"],
            rarity=raw_data["rarity"],
            type=raw_data["type"],
            passive_skills=passive_skills,
            defense_multiplier=raw_data.get("defense_multiplier"),
            damage_reduction=raw_data.get("damage_reduction"),
            guard_ability=raw_data.get("guard_ability", False),
            infinite_defense_stacking=raw_data.get("infinite_defense_stacking", False)
        )
        
        return character
    
    def _get_mock_characters(self) -> List[Character]:
        """
        モックキャラクターデータを取得する（フォールバック用）
        
        Returns:
            List[Character]: モックキャラクター一覧
        """
        return [
            Character(
                id="goku_ui",
                name="孫悟空（身勝手の極意）",
                rarity=6,
                type="AGL",
                passive_skills=[
                    PassiveSkill(
                        id="ui_defense",
                        type="defense_boost",
                        value=120.0,
                        condition="HP 80%以上時",
                        stackable=False
                    )
                ],
                defense_multiplier=150.0,
                damage_reduction=30.0,
                guard_ability=True,
                infinite_defense_stacking=False
            ),
            Character(
                id="vegeta_evolution",
                name="ベジータ（進化の極限）",
                rarity=6,
                type="STR",
                passive_skills=[
                    PassiveSkill(
                        id="evolution_stacking",
                        type="infinite_stacking",
                        value=30.0,
                        condition="攻撃時",
                        stackable=True
                    )
                ],
                defense_multiplier=130.0,
                damage_reduction=20.0,
                guard_ability=False,
                infinite_defense_stacking=True
            )
        ]
    
    def _get_from_cache(self, key: str) -> Optional[Any]:
        """
        キャッシュからデータを取得する
        
        Args:
            key: キャッシュキー
            
        Returns:
            Optional[Any]: キャッシュされたデータ（期限切れまたは存在しない場合はNone）
        """
        if key not in self._cache:
            return None
        
        # キャッシュの有効期限をチェック
        timestamp = self._cache_timestamps.get(key)
        if timestamp and datetime.now() - timestamp > timedelta(seconds=settings.cache_ttl):
            # 期限切れのキャッシュを削除
            del self._cache[key]
            del self._cache_timestamps[key]
            return None
        
        return self._cache[key]
    
    def _save_to_cache(self, key: str, data: Any) -> None:
        """
        データをキャッシュに保存する
        
        Args:
            key: キャッシュキー
            data: 保存するデータ
        """
        self._cache[key] = data
        self._cache_timestamps[key] = datetime.now()
        
        logger.debug(f"データをキャッシュに保存: {key}")