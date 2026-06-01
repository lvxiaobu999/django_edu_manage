import logging
import threading
from datetime import datetime
from pathlib import Path


_request_local = threading.local()


def get_request_id():
    """获取当前线程的 request_id，不存在时返回 '-'。"""
    return getattr(_request_local, 'request_id', '-')


def set_request_id(request_id):
    """设置当前线程的 request_id。"""
    _request_local.request_id = request_id


class RequestIdFilter:
    """日志过滤器：将当前请求的 request_id 注入每条日志记录。

    配合 logging 格式中的 {request_id} 占位符使用，确保每条日志都能追踪到具体请求。
    """

    def filter(self, record):
        record.request_id = get_request_id()
        return True


class DailyRotatingFileHandler(logging.Handler):
    """按天分割的日志 Handler，文件名包含日期和日志级别。

    文件名格式：{log_dir}/{prefix}-{date}-{level}.log
    示例：logs/app-2025-06-01-INFO.log

    每到新的一天自动切换到新文件，超过 backup_count 天的旧文件自动删除。
    """

    def __init__(self, log_dir, prefix, level_name='ALL', backup_count=30):
        super().__init__()
        self._log_dir = Path(log_dir)
        self._prefix = prefix
        self._level_name = level_name
        self._backup_count = backup_count
        self._current_date = None
        self._handler = None

    def _get_filename(self, date_str):
        return str(self._log_dir / f'{self._prefix}-{date_str}-{self._level_name}.log')

    def _rotate(self, today):
        self._log_dir.mkdir(parents=True, exist_ok=True)
        filename = self._get_filename(today)

        if self._handler:
            self._handler.close()

        self._handler = logging.FileHandler(filename, encoding='utf-8')
        if self.formatter:
            self._handler.setFormatter(self.formatter)
        self._current_date = today

    def _cleanup(self):
        pattern = f'{self._prefix}-*-{self._level_name}.log'
        files = sorted(self._log_dir.glob(pattern))
        if len(files) > self._backup_count:
            for f in files[:-self._backup_count]:
                f.unlink()

    def emit(self, record):
        today = datetime.now().strftime('%Y-%m-%d')
        if today != self._current_date:
            self._rotate(today)
            self._cleanup()
        self._handler.emit(record)

    def close(self):
        if self._handler:
            self._handler.close()
        super().close()
