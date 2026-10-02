from dataclasses import dataclass
from operator import itemgetter
from pathlib import Path

import yaml


@dataclass
class ResticConfig:
    repository: str
    password_file: Path | None = None
    prune_keep_daily: int = 7
    prune_keep_weekly: int = 4
    prune_keep_monthly: int = 12


@dataclass
class TelegramConfig:
    enabled: bool = False
    bot_token: str | None = None
    chat_id: str | None = None


@dataclass
class BackupConfig:
    backup_root: Path
    restic: ResticConfig
    telegram: TelegramConfig
    local_retention_days: int = 3
    min_free_bytes: int = 10 * 1024 * 1024 * 1024  # 10 GB


def load_config(path: str | Path) -> BackupConfig:
    file_path = Path(path)
    with open(file_path, "r") as f:
        try:
            config = yaml.safe_load(f) or {}
            restic, telegram = itemgetter("restic", "telegram")(config)
            if config.get("local_retention_days", 3) < 2:
                raise ValueError("local_retention_days must be at least 2")

        except yaml.YAMLError as exc:
            raise yaml.YAMLError(f"invalid yaml file, error: {exc}")
        except KeyError as exc:
            raise yaml.YAMLError(
                f"invalid yaml file, keys: restic or telegram dont exist: {exc}"
            )

    config["backup_root"] = Path(config["backup_root"])

    if restic.get("password_file"):
        restic["password_file"] = Path(restic["password_file"])

    restic = ResticConfig(**restic)
    telegram = TelegramConfig(**telegram)
    config["restic"] = restic
    config["telegram"] = telegram

    config["local_retention_days"] = config.get("local_retention_days", 3)
    config["min_free_bytes"] = config.get("min_free_bytes", 10 * 1024**3)

    config = BackupConfig(**config)

    return config
