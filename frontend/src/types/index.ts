/**
 * ドッカンバトル ダメージ計算アプリケーション - 型定義
 *
 * アプリケーション全体で使用される TypeScript 型定義を管理します。
 */

// キャラクター関連の型定義
export interface Character {
  /** キャラクターの一意識別子 */
  id: string;
  /** キャラクター名 */
  name: string;
  /** レアリティ（星の数） */
  rarity: number;
  /** 属性タイプ（AGL, TEQ, INT, STR, PHY） */
  type: string;
  /** パッシブスキル一覧 */
  passiveSkills: PassiveSkill[];
  /** 防御力倍率（パッシブスキルによる） */
  defenseMultiplier?: number;
  /** ダメージ軽減率（パーセンテージ） */
  damageReduction?: number;
  /** ガード能力の有無 */
  guardAbility?: boolean;
  /** DEF無限上昇能力の有無 */
  infiniteDefenseStacking?: boolean;
}

// パッシブスキル関連の型定義
export interface PassiveSkill {
  /** パッシブスキルの一意識別子 */
  id: string;
  /** スキルタイプ */
  type: "defense_boost" | "damage_reduction" | "guard" | "infinite_stacking";
  /** スキル効果値 */
  value: number;
  /** 発動条件（オプション） */
  condition?: string;
  /** スタック可能かどうか */
  stackable: boolean;
}

// ダメージ計算リクエスト関連の型定義
export interface DamageCalculationRequest {
  /** DEFステータス値 */
  defStat: number;
  /** リーダースキル倍率 */
  leaderSkillMultiplier: number;
  /** 選択されたキャラクターのID */
  characterId: string;
  /** 敵の攻撃値 */
  enemyAttack: number;
  /** 攻撃回数（DEF無限上昇キャラクター用） */
  attackCount?: number;
}

// ダメージ計算結果関連の型定義
export interface DamageCalculationResult {
  /** 実効防御力 */
  effectiveDefense: number;
  /** 受けるダメージ */
  damageReceived: number;
  /** 適用された修正値の詳細 */
  appliedModifiers: {
    /** リーダースキル倍率 */
    leaderSkill: number;
    /** 適用されたパッシブスキル一覧 */
    passiveSkills: PassiveSkill[];
    /** スタッキングボーナス（DEF無限上昇用） */
    stackingBonus?: number;
  };
  /** 計算詳細の説明文 */
  calculationDetails: string;
}

// API レスポンス関連の型定義
export interface ApiResponse<T> {
  /** レスポンスデータ */
  data?: T;
  /** エラー情報 */
  error?: {
    /** エラーコード */
    code: string;
    /** エラーメッセージ */
    message: string;
    /** エラー詳細 */
    details?: string;
  };
}

// フォーム関連の型定義
export interface DamageCalculatorFormData {
  /** DEFステータス */
  defStat: string;
  /** リーダースキル倍率 */
  leaderSkillMultiplier: string;
  /** 選択されたキャラクター */
  selectedCharacter: Character | null;
  /** 敵の攻撃値 */
  enemyAttack: string;
  /** 攻撃回数（DEF無限上昇用） */
  attackCount: string;
}

// UI状態管理用の型定義
export interface LoadingState {
  /** ローディング中かどうか */
  isLoading: boolean;
  /** ローディングメッセージ */
  message?: string;
}

export interface ErrorState {
  /** エラーが発生しているかどうか */
  hasError: boolean;
  /** エラーメッセージ */
  message?: string;
  /** エラーコード */
  code?: string;
}
