"""
ドッカンバトル ダメージ計算アプリケーション - ダメージ計算サービス

ダメージ計算のコアロジックを提供するサービスクラスです。
"""

from typing import Optional
import logging

from ..models.schemas import (
    Character,
    DamageCalculationRequest,
    DamageCalculationResult,
    AppliedModifiers,
    PassiveSkill
)

logger = logging.getLogger(__name__)


class DamageCalculatorService:
    """
    ダメージ計算サービスクラス
    
    キャラクターの防御ステータス、パッシブスキル、リーダースキルを考慮して
    最終的な受けるダメージを計算します。
    """
    
    async def calculate_damage(
        self,
        request: DamageCalculationRequest,
        character: Character
    ) -> DamageCalculationResult:
        """
        ダメージ計算のメイン処理
        
        Args:
            request: ダメージ計算リクエスト
            character: キャラクター情報
            
        Returns:
            DamageCalculationResult: 計算結果
        """
        logger.info(f"ダメージ計算開始: キャラクター={character.name}, DEF={request.def_stat}")
        
        # 1. 基本防御力の計算（DEF × リーダースキル倍率）
        base_defense = self._calculate_base_defense(
            request.def_stat,
            request.leader_skill_multiplier
        )
        
        # 2. パッシブスキルによる防御力修正の計算
        passive_defense_bonus = self._calculate_passive_defense_bonus(
            character,
            base_defense,
            request.attack_count or 0
        )
        
        # 3. 実効防御力の計算
        effective_defense = base_defense + passive_defense_bonus
        
        # 4. ダメージ軽減の適用
        damage_reduction_rate = self._calculate_damage_reduction(character)
        
        # 5. 最終ダメージの計算
        raw_damage = max(0, request.enemy_attack - effective_defense)
        final_damage = raw_damage * (1 - damage_reduction_rate / 100)
        
        # 6. ガード能力の適用
        if character.guard_ability and self._should_apply_guard(character, request):
            final_damage = self._apply_guard_reduction(final_damage)
        
        # 7. 適用された修正値の詳細を作成
        applied_modifiers = AppliedModifiers(
            leader_skill=request.leader_skill_multiplier,
            passive_skills=character.passive_skills,
            stacking_bonus=passive_defense_bonus if character.infinite_defense_stacking else None
        )
        
        # 8. 計算詳細の説明文を生成
        calculation_details = self._generate_calculation_details(
            request, character, base_defense, effective_defense, final_damage
        )
        
        result = DamageCalculationResult(
            effective_defense=effective_defense,
            damage_received=max(0, final_damage),  # 負のダメージは0にクランプ
            applied_modifiers=applied_modifiers,
            calculation_details=calculation_details
        )
        
        logger.info(f"ダメージ計算完了: 実効防御力={effective_defense}, 受けるダメージ={final_damage}")
        return result
    
    def _calculate_base_defense(self, def_stat: int, leader_skill_multiplier: float) -> float:
        """
        基本防御力を計算する（DEF × リーダースキル倍率）
        
        Args:
            def_stat: DEFステータス値
            leader_skill_multiplier: リーダースキル倍率
            
        Returns:
            float: 基本防御力
        """
        return def_stat * leader_skill_multiplier
    
    def _calculate_passive_defense_bonus(
        self,
        character: Character,
        base_defense: float,
        attack_count: int
    ) -> float:
        """
        パッシブスキルによる防御力ボーナスを計算する
        
        Args:
            character: キャラクター情報
            base_defense: 基本防御力
            attack_count: 攻撃回数（DEF無限上昇用）
            
        Returns:
            float: 防御力ボーナス
        """
        total_bonus = 0.0
        
        # キャラクター固有の防御力倍率を適用
        if character.defense_multiplier:
            total_bonus += base_defense * (character.defense_multiplier / 100)
        
        # パッシブスキルによるボーナスを計算
        for skill in character.passive_skills:
            if skill.type == "defense_boost":
                total_bonus += base_defense * (skill.value / 100)
            elif skill.type == "infinite_stacking" and character.infinite_defense_stacking:
                # DEF無限上昇の計算
                stacking_bonus = self._calculate_infinite_stacking_bonus(
                    skill, base_defense, attack_count
                )
                total_bonus += stacking_bonus
        
        return total_bonus
    
    def _calculate_infinite_stacking_bonus(
        self,
        skill: PassiveSkill,
        base_defense: float,
        attack_count: int
    ) -> float:
        """
        DEF無限上昇による防御力ボーナスを計算する
        
        Args:
            skill: 無限上昇パッシブスキル
            base_defense: 基本防御力
            attack_count: 攻撃回数
            
        Returns:
            float: スタッキングボーナス
        """
        if attack_count <= 0:
            return 0.0
        
        # 攻撃回数に応じた段階的な防御力増加
        # skill.value は1回の攻撃あたりの増加率（パーセンテージ）
        total_stacking_rate = skill.value * attack_count
        return base_defense * (total_stacking_rate / 100)
    
    def _calculate_damage_reduction(self, character: Character) -> float:
        """
        ダメージ軽減率を計算する
        
        Args:
            character: キャラクター情報
            
        Returns:
            float: ダメージ軽減率（パーセンテージ）
        """
        total_reduction = 0.0
        
        # キャラクター固有のダメージ軽減
        if character.damage_reduction:
            total_reduction += character.damage_reduction
        
        # パッシブスキルによるダメージ軽減
        for skill in character.passive_skills:
            if skill.type == "damage_reduction":
                total_reduction += skill.value
        
        # ダメージ軽減率は100%を超えないようにクランプ
        return min(total_reduction, 100.0)
    
    def _should_apply_guard(self, character: Character, request: DamageCalculationRequest) -> bool:
        """
        ガード能力を適用するかどうかを判定する
        
        Args:
            character: キャラクター情報
            request: ダメージ計算リクエスト
            
        Returns:
            bool: ガード適用可否
        """
        # 基本的にはガード能力があれば適用
        # 将来的には属性相性や条件判定を追加可能
        return character.guard_ability or False
    
    def _apply_guard_reduction(self, damage: float) -> float:
        """
        ガード能力によるダメージ軽減を適用する
        
        Args:
            damage: 軽減前のダメージ
            
        Returns:
            float: ガード適用後のダメージ
        """
        # ガード時は通常50%のダメージ軽減
        # TODO: キャラクターやスキルに応じた軽減率の設定
        guard_reduction_rate = 0.5
        return damage * (1 - guard_reduction_rate)
    
    def _generate_calculation_details(
        self,
        request: DamageCalculationRequest,
        character: Character,
        base_defense: float,
        effective_defense: float,
        final_damage: float
    ) -> str:
        """
        計算詳細の説明文を生成する
        
        Args:
            request: ダメージ計算リクエスト
            character: キャラクター情報
            base_defense: 基本防御力
            effective_defense: 実効防御力
            final_damage: 最終ダメージ
            
        Returns:
            str: 計算詳細の説明文
        """
        details = []
        
        # 基本計算
        details.append(f"基本DEF: {request.def_stat:,}")
        details.append(f"リーダースキル: ×{request.leader_skill_multiplier}")
        details.append(f"基本防御力: {base_defense:,.0f}")
        
        # パッシブスキル適用
        if character.defense_multiplier or character.passive_skills:
            details.append(f"パッシブ適用後: {effective_defense:,.0f}")
        
        # DEF無限上昇
        if character.infinite_defense_stacking and request.attack_count:
            details.append(f"攻撃{request.attack_count}回後")
        
        # 最終結果
        details.append(f"敵攻撃力: {request.enemy_attack:,}")
        details.append(f"受けるダメージ: {final_damage:,.0f}")
        
        return " → ".join(details)