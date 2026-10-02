from tempfile import TemporaryDirectory
import unittest
from pathlib import Path

from kraken_backup.config import BackupConfig, ResticConfig, TelegramConfig, load_config


class TestConfig(unittest.TestCase):
    def test_load_config_valid(self):
        with TemporaryDirectory() as tmpdir:
            config_file = Path(tmpdir) / "config.yaml"
            config_content = """
backup_root: /tmp/backups
local_retention_days: 3
min_free_bytes: 10737418240

restic:
  repository: "rclone:gdrive:backups/kraken"
  password_file: "/etc/kraken/restic.key"
  prune_keep_daily: 7
  prune_keep_weekly: 4
  prune_keep_monthly: 12

telegram:
  enabled: true
  bot_token: "123456:ABC"
  chat_id: "-100123"
"""
            config_file.write_text(config_content.strip())

            config = load_config(config_file)

            self.assertIsInstance(config, BackupConfig)
            self.assertIsInstance(config.restic, ResticConfig)
            self.assertIsInstance(config.telegram, TelegramConfig)
            self.assertEqual(config.backup_root, Path("/tmp/backups"))
            self.assertEqual(config.local_retention_days, 3)
            self.assertEqual(config.min_free_bytes, 10737418240)
            self.assertEqual(config.restic.repository, "rclone:gdrive:backups/kraken")
            self.assertEqual(
                config.restic.password_file, Path("/etc/kraken/restic.key")
            )
            self.assertEqual(config.restic.prune_keep_daily, 7)
            self.assertTrue(config.telegram.enabled)
            self.assertEqual(config.telegram.bot_token, "123456:ABC")
            self.assertEqual(config.telegram.chat_id, "-100123")

    def test_load_config_safeguard_retention(self):
        with TemporaryDirectory() as tmpdir:
            config_file = Path(tmpdir) / "config.yaml"
            config_content = """
backup_root: /tmp/backups
local_retention_days: 1
min_free_bytes: 10737418240

restic:
  repository: "rclone:gdrive:backups/kraken"
  password_file: "/etc/kraken/restic.key"
  prune_keep_daily: 7
  prune_keep_weekly: 4
  prune_keep_monthly: 12

telegram:
  enabled: true
  bot_token: "123456:ABC"
  chat_id: "-100123"
"""
            config_file.write_text(config_content.strip())

            with self.assertRaises(ValueError):
                load_config(config_file)

    def test_load_config_disk_threshold(self):
        with TemporaryDirectory() as tmpdir:
            config_file = Path(tmpdir) / "config.yaml"
            config_content = """
backup_root: /tmp/backups
local_retention_days: 2

restic:
    repository: "rclone:gdrive:backups/kraken"
    password_file: "/etc/kraken/restic.key"
    prune_keep_daily: 7
    prune_keep_weekly: 4
    prune_keep_monthly: 12

telegram:
    enabled: true
    bot_token: "123456:ABC"
    chat_id: "-100123"
"""
            config_file.write_text(config_content.strip())

            config = load_config(config_file)

            self.assertEqual(config.min_free_bytes, 10737418240)
