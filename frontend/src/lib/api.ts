/**
 * ドッカンバトル ダメージ計算アプリケーション - API クライアント
 *
 * バックエンド API との通信を管理するクライアント機能を提供します。
 */

import {
  Character,
  DamageCalculationRequest,
  DamageCalculationResult,
  ApiResponse,
} from "@/types";

// API ベース URL の設定
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * API リクエストのベース設定
 */
const defaultHeaders = {
  "Content-Type": "application/json",
};

/**
 * API エラーハンドリング用のカスタムエラークラス
 */
export class ApiError extends Error {
  constructor(
    public status: number,
    public code: string,
    message: string,
    public details?: string
  ) {
    super(message);
    this.name = "ApiError";
  }
}

/**
 * HTTP リクエストを実行する汎用関数
 */
async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;

  try {
    const response = await fetch(url, {
      headers: { ...defaultHeaders, ...options.headers },
      ...options,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new ApiError(
        response.status,
        errorData.code || "UNKNOWN_ERROR",
        errorData.message || `HTTP ${response.status}: ${response.statusText}`,
        errorData.details
      );
    }

    return await response.json();
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }

    // ネットワークエラーやその他の例外
    throw new ApiError(
      0,
      "NETWORK_ERROR",
      "ネットワークエラーが発生しました。接続を確認してください。",
      error instanceof Error ? error.message : String(error)
    );
  }
}

/**
 * キャラクター一覧を取得する
 */
export async function getCharacters(): Promise<Character[]> {
  const response = await apiRequest<ApiResponse<Character[]>>(
    "/api/characters"
  );

  if (response.error) {
    throw new ApiError(
      400,
      response.error.code,
      response.error.message,
      response.error.details
    );
  }

  return response.data || [];
}

/**
 * 特定のキャラクター情報を取得する
 */
export async function getCharacter(characterId: string): Promise<Character> {
  const response = await apiRequest<ApiResponse<Character>>(
    `/api/characters/${characterId}`
  );

  if (response.error) {
    throw new ApiError(
      400,
      response.error.code,
      response.error.message,
      response.error.details
    );
  }

  if (!response.data) {
    throw new ApiError(
      404,
      "CHARACTER_NOT_FOUND",
      "キャラクターが見つかりませんでした"
    );
  }

  return response.data;
}

/**
 * ダメージ計算を実行する
 */
export async function calculateDamage(
  request: DamageCalculationRequest
): Promise<DamageCalculationResult> {
  const response = await apiRequest<ApiResponse<DamageCalculationResult>>(
    "/api/calculate-damage",
    {
      method: "POST",
      body: JSON.stringify(request),
    }
  );

  if (response.error) {
    throw new ApiError(
      400,
      response.error.code,
      response.error.message,
      response.error.details
    );
  }

  if (!response.data) {
    throw new ApiError(500, "CALCULATION_ERROR", "ダメージ計算に失敗しました");
  }

  return response.data;
}

/**
 * API の健康状態をチェックする
 */
export async function healthCheck(): Promise<{
  status: string;
  service: string;
}> {
  return await apiRequest<{ status: string; service: string }>("/health");
}
