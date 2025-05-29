import os
from dataclasses import dataclass
import pyaudio
from dotenv import load_dotenv

@dataclass
class AudioConfig:
    """オーディオ設定のデータクラス"""
    FORMAT: int = pyaudio.paInt16
    CHANNELS: int = 1
    SEND_SAMPLE_RATE: int = 16000
    RECEIVE_SAMPLE_RATE: int = 24000
    CHUNK_SIZE: int = 1024

@dataclass
class GeminiConfig:
    """Gemini API設定のデータクラス"""
    MODEL: str = "models/gemini-2.5-flash-preview-native-audio-dialog"
    API_VERSION: str = "v1alpha"
    TIMEOUT: int = 3000

@dataclass
class AppConfig:
    """アプリケーション全体の設定を管理するデータクラス"""
    audio: AudioConfig
    gemini: GeminiConfig
    api_key: str
    system_prompt: str

def load_config() -> AppConfig:
    """
    環境変数から設定を読み込み、AppConfigインスタンスを返します。

    Returns:
        AppConfig: アプリケーション設定

    Raises:
        ValueError: 必要な環境変数が設定されていない場合
    """
    load_dotenv()

    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("GEMINI_API_KEY must be set in environment variables")

    system_prompt = os.getenv(
        'SYSTEM_PROMPT',
        'You are a professional and detailed AI assistant. Please provide as thorough an answer as possible to the user\'s questions.'
    )

    return AppConfig(
        audio=AudioConfig(),
        gemini=GeminiConfig(),
        api_key=api_key,
        system_prompt=system_prompt
    )

# グローバル設定インスタンス
config = load_config()
