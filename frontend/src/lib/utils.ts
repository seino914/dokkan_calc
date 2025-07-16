/**
 * ドッカンバトル ダメージ計算アプリケーション - ユーティリティ関数
 *
 * アプリケーション全体で使用される汎用的なユーティリティ関数を提供します。
 */

import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

/**
 * Tailwind CSS クラス名を結合・マージする
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

/**
 * 数値を日本語の桁区切り形式でフォーマットする
 */
export function formatNumber(value: number): string {
  return new Intl.NumberFormat("ja-JP").format(value);
}

/**
 * パーセンテージを日本語形式でフォーマットする
 */
export function formatPercentage(value: number, decimals: number = 1): string {
  return `${value.toFixed(decimals)}%`;
}

/**
 * 文字列が有効な数値かどうかをチェックする
 */
export function isValidNumber(value: string): boolean {
  const num = parseFloat(value);
  return !isNaN(num) && isFinite(num);
}

/**
 * 文字列を数値に安全に変換する
 */
export function safeParseNumber(
  value: string,
  defaultValue: number = 0
): number {
  const num = parseFloat(value);
  return isNaN(num) ? defaultValue : num;
}

/**
 * 文字列を整数に安全に変換する
 */
export function safeParseInt(value: string, defaultValue: number = 0): number {
  const num = parseInt(value, 10);
  return isNaN(num) ? defaultValue : num;
}

/**
 * 値を指定された範囲内にクランプする
 */
export function clamp(value: number, min: number, max: number): number {
  return Math.min(Math.max(value, min), max);
}

/**
 * デバウンス関数 - 連続した関数呼び出しを制限する
 */
export function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: NodeJS.Timeout;

  return (...args: Parameters<T>) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), wait);
  };
}

/**
 * スロットル関数 - 関数の実行頻度を制限する
 */
export function throttle<T extends (...args: any[]) => any>(
  func: T,
  limit: number
): (...args: Parameters<T>) => void {
  let inThrottle: boolean;

  return (...args: Parameters<T>) => {
    if (!inThrottle) {
      func(...args);
      inThrottle = true;
      setTimeout(() => (inThrottle = false), limit);
    }
  };
}

/**
 * エラーメッセージを日本語で取得する
 */
export function getErrorMessage(error: unknown): string {
  if (error instanceof Error) {
    return error.message;
  }

  if (typeof error === "string") {
    return error;
  }

  return "予期しないエラーが発生しました";
}

/**
 * キャラクター属性の日本語表示名を取得する
 */
export function getCharacterTypeDisplayName(type: string): string {
  const typeMap: Record<string, string> = {
    AGL: "技（AGL）",
    TEQ: "知（TEQ）",
    INT: "知（INT）",
    STR: "力（STR）",
    PHY: "体（PHY）",
  };

  return typeMap[type.toUpperCase()] || type;
}

/**
 * パッシブスキルタイプの日本語表示名を取得する
 */
export function getPassiveSkillTypeDisplayName(type: string): string {
  const typeMap: Record<string, string> = {
    defense_boost: "防御力アップ",
    damage_reduction: "ダメージ軽減",
    guard: "ガード",
    infinite_stacking: "DEF無限上昇",
  };

  return typeMap[type] || type;
}

/**
 * レアリティを星の文字列で表示する
 */
export function formatRarity(rarity: number): string {
  return "★".repeat(Math.max(0, Math.min(6, rarity)));
}

/**
 * 計算結果の詳細説明を生成する
 */
export function generateCalculationExplanation(
  defStat: number,
  leaderSkillMultiplier: number,
  effectiveDefense: number,
  enemyAttack: number,
  damageReceived: number
): string {
  const parts = [
    `基本DEF: ${formatNumber(defStat)}`,
    `リーダースキル倍率: ${leaderSkillMultiplier}倍`,
    `実効防御力: ${formatNumber(effectiveDefense)}`,
    `敵攻撃力: ${formatNumber(enemyAttack)}`,
    `受けるダメージ: ${formatNumber(damageReceived)}`,
  ];

  return parts.join(" → ");
}
