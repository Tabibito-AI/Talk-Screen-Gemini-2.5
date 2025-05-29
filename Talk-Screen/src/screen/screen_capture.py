import base64
import io
from typing import Optional, Dict
import PIL.Image
import mss
from logger import logger

class ScreenCapture:
    """スクリーンキャプチャを管理するクラス"""

    def __init__(self):
        """ScreenCaptureインスタンスを初期化"""
        self.sct = mss.mss()

    def capture_frame(self) -> Optional[Dict[str, str]]:
        """
        現在の画面をキャプチャし、base64エンコードされた画像データを返します。

        Returns:
            Optional[Dict[str, str]]:
                成功時: {"mime_type": "image/jpeg", "data": base64_encoded_string}
                失敗時: None
        """
        try:
            monitor = self.sct.monitors[1]  # プライマリモニターを使用
            sct_img = self.sct.grab(monitor)

            # PIL Imageに変換
            img = PIL.Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            img.thumbnail([1024, 1024])  # サイズを制限

            # JPEG形式でエンコード
            image_io = io.BytesIO()
            img.save(image_io, format="jpeg")
            image_io.seek(0)

            # base64エンコード
            mime_type = "image/jpeg"
            image_bytes = image_io.read()
            encoded_image = base64.b64encode(image_bytes).decode()

            return {
                "mime_type": mime_type,
                "data": encoded_image
            }

        except Exception as e:
            logger.error(f"スクリーンキャプチャ中にエラーが発生しました: {e}")
            return None

    def __enter__(self):
        """コンテキストマネージャーのエントリーポイント"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """コンテキストマネージャーの終了処理"""
        self.sct.close()
