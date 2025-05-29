# Talk Screen AI

音声チャットとスクリーンシェアを組み合わせたAIアシスタントアプリケーション。最新のGemini 2.5 Flash Native Audio Live APIを使用して、AIと自然な音声対話を行いながら、画面を共有することができます。

## 機能

- **ネイティブオーディオ対話**: Gemini 2.5 Flash Native Audio Live APIによる自然で表現豊かな音声対話
- **音声による双方向コミュニケーション**: 低遅延でリアルタイムな音声対話
- **リアルタイムスクリーンシェア**: 画面内容をAIと共有
- **テキスト入力サポート**: 音声とテキストの両方でコミュニケーション可能
- **高品質な音声合成**: より自然で人間らしい音声出力
- **エラーハンドリングとログ機能**: 堅牢なエラー処理とデバッグ支援

## 必要条件

- Python 3.11以上
- マイク入力デバイス
- イヤホン(スピーカーは使用しないでください)
- Gemini API キー
- 安定したインターネット接続（Live API使用のため）

## インストール

1. リポジトリをクローン:
```bash
git clone https://github.com/yourusername/Talk-Screen-AI.git
cd Talk-Screen-AI
```

2. 依存パッケージをインストール:
```bash
pip install -r requirements.txt
```

3. 環境変数の設定:
`.env`ファイルをプロジェクトのルートディレクトリに作成し、以下の内容を設定:
```
GEMINI_API_KEY=your_api_key_here
SYSTEM_PROMPT=カスタムシステムプロンプト（オプション）
```

## 使用方法

1. アプリケーションを起動:
```bash
# 方法1: srcディレクトリから実行（推奨）
cd src
python main.py

# 方法2: プロジェクトルートから実行
python -m src.main

# 方法3: PYTHONPATHを設定して実行
PYTHONPATH=. python src/main.py
```

2. 操作方法:
- **音声で話しかける**: マイクに向かって話すだけで、Gemini 2.5 Flash Native Audio Live APIがリアルタイムで自然な音声で応答します
- **テキスト入力**: プロンプトに直接テキストを入力することもできます
- **画面共有**: アプリケーション実行中は自動的に画面がAIと共有され、画面内容について質問できます
- **終了**: 'q'を入力してEnterを押すと終了します

## プロジェクト構造

```
Talk-Screen/
├── .gitignore              # Git除外設定
├── README.md               # プロジェクト説明（このファイル）
├── requirements.txt        # Python依存パッケージ
├── .env                    # 環境変数（要作成）
└── src/
    ├── __init__.py
    ├── main.py             # メインアプリケーション
    ├── logger.py           # ログ機能
    ├── audio/
    │   ├── __init__.py
    │   └── audio_handler.py    # 音声入出力の処理
    ├── config/
    │   ├── __init__.py
    │   └── settings.py         # アプリケーション設定
    └── screen/
        ├── __init__.py
        └── screen_capture.py   # スクリーンキャプチャの処理
```

## 技術仕様

### 使用モデル
- **Gemini 2.5 Flash Preview Native Audio Dialog**: `gemini-2.5-flash-preview-native-audio-dialog`
- **API**: Google Gemini Live API (v1alpha)
- **音声形式**: 16kHz、16-bit PCM、モノラル
- **出力音声**: 24kHz、ネイティブオーディオ生成

### 主要機能
- **リアルタイム音声対話**: 低遅延での双方向音声コミュニケーション
- **音声活動検出**: 自動的な発話開始・終了の検出
- **画面共有**: リアルタイムでの画面キャプチャと共有
- **マルチモーダル入力**: 音声、テキスト、画像の組み合わせ
- **エラー回復**: 接続エラーや割り込みからの自動復旧

### システム要件
- **Python**: 3.11以上
- **OS**: macOS、Windows、Linux対応
- **メモリ**: 最低2GB RAM推奨
- **ネットワーク**: 安定したブロードバンド接続

## ライセンス

MITライセンス
