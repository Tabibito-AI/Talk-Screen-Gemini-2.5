import asyncio
import traceback
from typing import Optional
from google import genai
from google.genai import types

from config.settings import config
from logger import logger
from audio.audio_handler import AudioHandler
from screen.screen_capture import ScreenCapture

# Python 3.11以上が必要条件のため、TaskGroupとExceptionGroupは標準で利用可能

class TalkScreenAI:
    """音声チャットとスクリーンシェアを組み合わせたAIアシスタントアプリケーション"""

    def __init__(self):
        """TalkScreenAIインスタンスを初期化"""
        self.audio_handler = AudioHandler(config.audio)
        self.is_running = True

        # Gemini APIクライアントの初期化
        self.client = genai.Client(
            api_key=config.api_key,
            http_options={
                "api_version": config.gemini.API_VERSION,
                "timeout": config.gemini.TIMEOUT
            }
        )

        # キューの初期化
        self.audio_in_queue: Optional[asyncio.Queue] = None
        self.audio_out_queue: Optional[asyncio.Queue] = None
        self.data_out_queue: Optional[asyncio.Queue] = None
        self.session = None

    async def send_text(self) -> None:
        """テキスト入力を処理し、セッションに送信"""
        while self.is_running:
            try:
                text = await asyncio.to_thread(input, "message > ")
                if text.lower() == "q":
                    self.is_running = False
                    break
                # Live API用の正しい送信方法を使用
                await self.session.send(input=text or ".", end_of_turn=True)
            except EOFError:
                logger.warning("入力ストリームが終了しました。1秒後に再試行します...")
                await asyncio.sleep(1)
            except Exception as e:
                logger.error(f"テキスト送信中にエラーが発生しました: {e}")
                await asyncio.sleep(1)

    async def process_screen_capture(self) -> None:
        """画面キャプチャを処理し、セッションに送信"""
        with ScreenCapture() as screen_capture:
            while self.is_running:
                try:
                    frame_data = screen_capture.capture_frame()
                    if frame_data is None:
                        await asyncio.sleep(1)
                        continue

                    await asyncio.sleep(1.0)  # キャプチャ間隔
                    await self.data_out_queue.put(frame_data)
                except Exception as e:
                    logger.error(f"画面キャプチャ処理中にエラーが発生しました: {e}")
                    await asyncio.sleep(1)

    async def process_audio_input(self) -> None:
        """マイク入力を処理"""
        while self.is_running:
            try:
                audio_data = await self.audio_handler.read_audio()
                if audio_data:
                    await self.audio_out_queue.put(audio_data)
            except Exception as e:
                logger.error(f"音声入力処理中にエラーが発生しました: {e}")
                await asyncio.sleep(1)

    async def process_audio_output(self) -> None:
        """AIからの音声出力を処理"""
        while self.is_running:
            try:
                bytestream = await self.audio_in_queue.get()
                await self.audio_handler.play_audio(bytestream)
            except Exception as e:
                logger.error(f"音声出力処理中にエラーが発生しました: {e}")
                await asyncio.sleep(1)

    async def send_realtime_data(self) -> None:
        """リアルタイムデータ（音声と画面）をセッションに送信"""
        async def process_audio_queue():
            while self.is_running:
                try:
                    audio_msg = await self.audio_out_queue.get()
                    # Live API用のBlobオブジェクトを作成
                    audio_blob = types.Blob(
                        data=audio_msg["data"],
                        mime_type=audio_msg["mime_type"]
                    )
                    # Live API用の正しい送信方法を使用
                    await self.session.send(input=audio_blob)
                except Exception as e:
                    logger.error(f"音声キュー処理中にエラーが発生しました: {e}")
                    await asyncio.sleep(1)

        async def process_data_queue():
            while self.is_running:
                try:
                    data_msg = await self.data_out_queue.get()
                    # 画面キャプチャデータの送信
                    await self.session.send(input=data_msg)
                except Exception as e:
                    logger.error(f"データキュー処理中にエラーが発生しました: {e}")
                    await asyncio.sleep(1)

        await asyncio.gather(process_audio_queue(), process_data_queue())

    async def receive_ai_response(self) -> None:
        """AIからのレスポンスを受信して処理"""
        while self.is_running:
            try:
                # Live APIの新しい受信方法を使用
                async for response in self.session.receive():
                    # ネイティブオーディオデータの処理
                    if response.data is not None:
                        self.audio_in_queue.put_nowait(response.data)
                        continue

                    # テキストレスポンスの処理（デバッグ用）
                    if response.text is not None:
                        print(response.text, end="")

                    # サーバーコンテンツの処理
                    if response.server_content:
                        # 思考プロセスの表示（thinking capabilities）
                        if hasattr(response.server_content, 'model_turn') and response.server_content.model_turn:
                            for part in response.server_content.model_turn.parts:
                                if hasattr(part, 'thought') and part.thought:
                                    logger.info(f"AI思考プロセス: {part.thought}")

                        # 生成完了の確認
                        if hasattr(response.server_content, 'generation_complete') and response.server_content.generation_complete:
                            logger.info("AI応答生成が完了しました")

                        # 割り込み処理
                        if hasattr(response.server_content, 'interrupted') and response.server_content.interrupted:
                            logger.info("AI応答が割り込まれました")
                            # 未処理のオーディオキューをクリア
                            while not self.audio_in_queue.empty():
                                self.audio_in_queue.get_nowait()

            except Exception as e:
                logger.error(f"AIレスポンス処理中にエラーが発生しました: {e}")
                await asyncio.sleep(1)

    async def run(self) -> None:
        """アプリケーションのメインループを実行"""
        try:
            # Gemini 2.5 Flash Native Audio Live API設定
            config_dict = {
                "response_modalities": ["AUDIO"],  # ネイティブオーディオ出力を使用
                "generation_config": {
                    "temperature": 0.7,
                    "top_p": 0.8,
                    "top_k": 40
                },
                # ネイティブオーディオモデル用の追加設定
                "realtime_input_config": {
                    "automatic_activity_detection": {
                        "disabled": False,
                        "start_of_speech_sensitivity": "START_SENSITIVITY_MEDIUM",
                        "end_of_speech_sensitivity": "END_SENSITIVITY_MEDIUM",
                        "prefix_padding_ms": 20,
                        "silence_duration_ms": 100,
                    }
                }
            }

            # 各種キューの初期化
            self.audio_in_queue = asyncio.Queue()
            self.audio_out_queue = asyncio.Queue(maxsize=5)
            self.data_out_queue = asyncio.Queue(maxsize=5)

            # オーディオストリームのセットアップ
            await self.audio_handler.setup_input_stream()
            await self.audio_handler.setup_output_stream()

            logger.info("Gemini 2.5 Flash Native Audio Live APIでアプリケーションを開始します")

            async with (
                self.client.aio.live.connect(
                    model=config.gemini.MODEL,
                    config=config_dict
                ) as session,
                asyncio.TaskGroup() as tg,
            ):
                self.session = session

                # 各タスクの開始
                send_text_task = tg.create_task(self.send_text())
                tg.create_task(self.send_realtime_data())
                tg.create_task(self.process_audio_input())
                tg.create_task(self.process_screen_capture())
                tg.create_task(self.receive_ai_response())
                tg.create_task(self.process_audio_output())

                await send_text_task
                self.is_running = False

        except asyncio.CancelledError:
            logger.info("アプリケーションがキャンセルされました")
            self.is_running = False
        except ExceptionGroup as eg:
            logger.error("エラーが発生しました:")
            traceback.print_exception(eg)
        finally:
            self.is_running = False
            self.audio_handler.cleanup()
            logger.info("アプリケーションを終了します")

if __name__ == "__main__":
    def main():
        """アプリケーションのエントリーポイント"""
        app = TalkScreenAI()
        asyncio.run(app.run())

    main()
