import logging
import sys
from logging.handlers import RotatingFileHandler

def setup_logger(name: str = "TalkScreenAI") -> logging.Logger:
    """
    アプリケーション全体で使用するロガーをセットアップします。
    
    Args:
        name (str): ロガーの名前
        
    Returns:
        logging.Logger: 設定されたロガーインスタンス
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # ファイルハンドラーの設定（ローテーション付き）
    file_handler = RotatingFileHandler(
        "app.log",
        maxBytes=1024 * 1024,  # 1MB
        backupCount=5,
        encoding="utf-8"
    )
    file_handler.setLevel(logging.INFO)
    
    # コンソールハンドラーの設定
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    
    # フォーマッターの設定
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # ハンドラーの追加
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# グローバルロガーインスタンスの作成
logger = setup_logger()
