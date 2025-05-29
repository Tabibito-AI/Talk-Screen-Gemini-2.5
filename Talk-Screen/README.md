# Talk Screen AI

音声チャットとスクリーンシェアを組み合わせたAIアシスタントアプリケーション。最新のGemini 2.5 Flash Native Audio Live APIを使用して、AIと自然な音声対話を行いながら、画面を共有することができます。

## 機能

- **ネイティブオーディオ対話**: Gemini 2.5 Flash Native Audio Live APIによる自然で表現豊かな音声対話
- **思考機能**: AIの思考プロセスを可視化（thinking capabilities）
- **音声による双方向コミュニケーション**: 低遅延でリアルタイムな音声対話
- **リアルタイムスクリーンシェア**: 画面内容をAIと共有
- **テキスト入力サポート**: 音声とテキストの両方でコミュニケーション可能
- **高品質な音声合成**: より自然で人間らしい音声出力
- **エラーハンドリングとログ機能**: 堅牢なエラー処理とデバッグ支援

## 必要条件

- Python 3.11以上
- マイク入力デバイス
- スピーカー出力デバイス
- Gemini API キー（Gemini 2.5 Flash Native Audio Live API対応）
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
python -m src.main

or

PYTHONPATH=. python src/main.py

```

2. 操作方法:
- **音声で話しかける**: マイクに向かって話すだけで、Gemini 2.5 Flash Native Audio Live APIがリアルタイムで自然な音声で応答します
- **思考プロセスの確認**: AIの思考プロセスがログに表示され、どのように回答を生成しているかを確認できます
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

## エラーハンドリング

アプリケーションは以下の状況で適切なエラーハンドリングを行います：

- マイクやスピーカーデバイスの初期化エラー
- ネットワーク接続の問題
- API呼び出しの失敗
- 音声ストリームの問題

エラーが発生した場合は、`app.log`ファイルに詳細が記録されます。

## トラブルシューティング

### よくある問題と解決方法

#### 1. APIキーエラー
```
ValueError: GEMINI_API_KEY must be set in environment variables
```
**解決方法**: `.env`ファイルに正しいAPIキーが設定されているか確認してください。

#### 2. 音声デバイスエラー
```
マイク入力ストリームの初期化に失敗しました
```
**解決方法**:
- マイクが正しく接続されているか確認
- 他のアプリケーションがマイクを使用していないか確認
- システムの音声設定でマイクの許可を確認

#### 3. APIクォータエラー
```
You exceeded your current quota
```
**解決方法**:
- Gemini APIの使用制限を確認
- しばらく時間をおいてから再試行
- 必要に応じてAPIプランをアップグレード

#### 4. 接続エラー
```
ネットワーク接続の問題
```
**解決方法**:
- インターネット接続を確認
- ファイアウォール設定を確認
- VPN使用時は設定を確認

### ログの確認
詳細なエラー情報は`app.log`ファイルで確認できます：
```bash
tail -f app.log
```

## 注意事項

- マイクとスピーカーのデバイス設定が正しく行われていることを確認してください
- **Live API使用**: Gemini 2.5 Flash Native Audio Live APIを使用するため、安定したインターネット接続が必要です
- **セッション制限**: ネイティブオーディオモデルは128kトークンのコンテキスト制限があります
- **音声品質**: 最適な音声品質のため、16kHz、16-bit PCM、モノラル形式で音声を送信します
- **APIキー**: Gemini 2.5 Flash Native Audio Live API対応のAPIキーが必要です
- **利用制限**: APIキーの利用制限と料金に注意してください

## 貢献

プロジェクトへの貢献を歓迎します！

### 貢献方法
1. このリポジトリをフォーク
2. 機能ブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add some amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

### 報告
- バグ報告や機能要求は[Issues](../../issues)で受け付けています
- セキュリティに関する問題は直接連絡してください

## 更新履歴

### v1.0.0 (2025-05-29)
- Gemini 2.5 Flash Native Audio Live API対応
- リアルタイム音声対話機能
- 画面共有機能
- マルチモーダル入力サポート
- 包括的なエラーハンドリング

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は[LICENSE](LICENSE)ファイルを参照してください。

## 謝辞

- [Google Gemini API](https://ai.google.dev/gemini-api/docs) - 強力なAI機能を提供
- [PyAudio](https://pypi.org/project/PyAudio/) - 音声入出力処理
- [MSS](https://pypi.org/project/mss/) - 高速スクリーンキャプチャ
- [PIL](https://pypi.org/project/Pillow/) - 画像処理機能
