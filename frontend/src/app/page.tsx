/**
 * ドッカンバトル ダメージ計算アプリケーション - メインページ
 *
 * アプリケーションのメインページコンポーネントです。
 */

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-400 via-red-500 to-pink-500">
      <div className="container mx-auto px-4 py-8">
        {/* ヘッダー */}
        <header className="text-center mb-12">
          <h1 className="text-4xl md:text-6xl font-bold text-white mb-4 drop-shadow-lg">
            ドッカンバトル
          </h1>
          <h2 className="text-2xl md:text-3xl font-semibold text-white mb-2 drop-shadow-md">
            ダメージ計算ツール
          </h2>
          <p className="text-lg text-white/90 drop-shadow-sm">
            キャラクターの防御力とダメージを正確に計算
          </p>
        </header>

        {/* メインコンテンツエリア */}
        <main className="max-w-4xl mx-auto">
          <div className="bg-white/95 backdrop-blur-sm rounded-2xl shadow-2xl p-8">
            <div className="text-center">
              <h3 className="text-2xl font-bold text-gray-800 mb-4">
                計算機能を準備中...
              </h3>
              <p className="text-gray-600 mb-8">
                キャラクターの防御ステータス、リーダースキル倍率、パッシブスキルを考慮した
                <br />
                正確なダメージ計算を提供します。
              </p>

              {/* 機能紹介カード */}
              <div className="grid md:grid-cols-3 gap-6 mt-8">
                <div className="bg-blue-50 p-6 rounded-xl border border-blue-200">
                  <div className="text-blue-600 text-3xl mb-3">🛡️</div>
                  <h4 className="font-semibold text-gray-800 mb-2">
                    防御力計算
                  </h4>
                  <p className="text-sm text-gray-600">
                    DEFステータスとリーダースキルを考慮した実効防御力を算出
                  </p>
                </div>

                <div className="bg-green-50 p-6 rounded-xl border border-green-200">
                  <div className="text-green-600 text-3xl mb-3">⚡</div>
                  <h4 className="font-semibold text-gray-800 mb-2">
                    パッシブスキル対応
                  </h4>
                  <p className="text-sm text-gray-600">
                    DEF無限上昇やダメージ軽減などの特殊効果に対応
                  </p>
                </div>

                <div className="bg-purple-50 p-6 rounded-xl border border-purple-200">
                  <div className="text-purple-600 text-3xl mb-3">📊</div>
                  <h4 className="font-semibold text-gray-800 mb-2">
                    詳細な結果表示
                  </h4>
                  <p className="text-sm text-gray-600">
                    計算過程と適用された修正値を詳細に表示
                  </p>
                </div>
              </div>
            </div>
          </div>
        </main>

        {/* フッター */}
        <footer className="text-center mt-12">
          <p className="text-white/80 text-sm">
            ドラゴンボール Z ドッカンバトル ダメージ計算ツール v1.0.0
          </p>
        </footer>
      </div>
    </div>
  );
}
