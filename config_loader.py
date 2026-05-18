"""
配置加载器 — 从 config.yaml 读取配置，支持环境变量覆盖。
"""

import os
import yaml
from pathlib import Path

_CONFIG = None

ROOT = Path(__file__).resolve().parent


def _load_config() -> dict:
    """加载配置，优先环境变量覆盖。"""
    global _CONFIG
    if _CONFIG is not None:
        return _CONFIG

    config_path = ROOT / "config.yaml"
    if config_path.exists():
        with open(config_path) as f:
            _CONFIG = yaml.safe_load(f) or {}
    else:
        _CONFIG = {}

    # 无配置文件时给默认值
    _CONFIG.setdefault("watchlist", ["600036", "000858", "300750", "601318", "600519"])
    _CONFIG.setdefault("data_sources", {"quote": ["tencent", "mootdx"]})
    _CONFIG.setdefault("network", {"timeout": 10, "retry": 2, "retry_delay": 1.0})
    _CONFIG.setdefault("output", {"format": "table", "max_rows": 30})

    return _CONFIG


def get_config() -> dict:
    return _load_config()


def get_watchlist() -> list[str]:
    return _load_config().get("watchlist", [])


def get_network_config() -> dict:
    return _load_config().get("network", {})


def get_data_sources() -> dict:
    return _load_config().get("data_sources", {})


def get_output_config() -> dict:
    return _load_config().get("output", {})
