import asyncio
from typing import Optional, Dict, Any
import pyaudio
from ..config.settings import AudioConfig
from ..logger import logger

class AudioHandler:
    """オーディオの入出力を管理するクラス"""

    def __init__(self, config: AudioConfig):
        """
        AudioHandlerインスタンスを初期化

        Args:
            config (AudioConfig): オーディオ設定
        """
        self.config = config
        self.pya = pyaudio.PyAudio()
        self.audio_stream: Optional[pyaudio.Stream] = None
        self.play_stream: Optional[pyaudio.Stream] = None
        self.is_running = True

    async def setup_input_stream(self) -> None:
        """マイク入力ストリームをセットアップ"""
        try:
            mic_info = self.pya.get_default_input_device_info()
            self.audio_stream = await asyncio.to_thread(
                self.pya.open,
                format=self.config.FORMAT,
                channels=self.config.CHANNELS,
                rate=self.config.SEND_SAMPLE_RATE,
                input=True,
                input_device_index=mic_info["index"],
                frames_per_buffer=self.config.CHUNK_SIZE,
            )
            logger.info("マイク入力ストリームを初期化しました")
        except Exception as e:
            logger.error(f"マイク入力ストリームの初期化に失敗しました: {e}")
            raise

    async def setup_output_stream(self) -> None:
        """オーディオ出力ストリームをセットアップ"""
        try:
            self.play_stream = await asyncio.to_thread(
                self.pya.open,
                format=self.config.FORMAT,
                channels=self.config.CHANNELS,
                rate=self.config.RECEIVE_SAMPLE_RATE,
                output=True,
            )
            logger.info("オーディオ出力ストリームを初期化しました")
        except Exception as e:
            logger.error(f"オーディオ出力ストリームの初期化に失敗しました: {e}")
            raise

    async def read_audio(self) -> Optional[Dict[str, Any]]:
        """
        マイクから音声データを読み取ります

        Returns:
            Optional[Dict[str, Any]]: 音声データとMIMEタイプを含む辞書、エラー時はNone
        """
        if not self.audio_stream:
            logger.error("オーディオ入力ストリームが初期化されていません")
            return None

        try:
            kwargs = {"exception_on_overflow": False} if __debug__ else {}
            data = await asyncio.to_thread(
                self.audio_stream.read,
                self.config.CHUNK_SIZE,
                **kwargs
            )
            # Live API用のBlobオブジェクト形式で返す
            return {"data": data, "mime_type": f"audio/pcm;rate={self.config.SEND_SAMPLE_RATE}"}
        except Exception as e:
            logger.error(f"音声データの読み取り中にエラーが発生しました: {e}")
            return None

    async def play_audio(self, bytestream: bytes) -> bool:
        """
        音声データを再生します

        Args:
            bytestream (bytes): 再生する音声データ

        Returns:
            bool: 再生成功時True、失敗時False
        """
        if not self.play_stream:
            logger.error("オーディオ出力ストリームが初期化されていません")
            return False

        try:
            await asyncio.to_thread(self.play_stream.write, bytestream)
            return True
        except Exception as e:
            logger.error(f"音声データの再生中にエラーが発生しました: {e}")
            return False

    def cleanup(self) -> None:
        """オーディオストリームとPyAudioインスタンスをクリーンアップ"""
        self.is_running = False

        if self.audio_stream:
            self.audio_stream.stop_stream()
            self.audio_stream.close()

        if self.play_stream:
            self.play_stream.stop_stream()
            self.play_stream.close()

        self.pya.terminate()
        logger.info("オーディオリソースをクリーンアップしました")
