# KrakenBackup

Autonomous, modular container and service backup orchestrator with Restic client-side encryption and Google Drive synchronization.

[![Python](https://img.shields.io/badge/Python-3.14%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Package Manager](https://img.shields.io/badge/uv-package%20manager-purple?logo=astral)](https://github.com/astral-sh/uv)
[![Code Style](https://img.shields.io/badge/code%20style-PEP%208-green)](https://peps.python.org/pep-0008/)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

---

## Overview

KrakenBackup is an autonomous, service-scoped backup tool designed for containerized environments and homelab infrastructure. It orchestrates zero-downtime database dumps and configuration captures, applies compression, and ships encrypted deduplicated snapshots off-site.

### Key Capabilities
- **Hot Database Dumps:** Performs non-blocking database dumps (MariaDB, PostgreSQL) via container execution.
- **Client-Side Encryption & Deduplication:** Integrates with Restic and Rclone to produce encrypted, content-defined deduplicated snapshots sent to remote object or cloud storage (e.g., Google Drive).
- **Atomic Staging & Integrity:** Stages snapshots in isolated directories prior to publication, generating SHA-256 manifests for every artifact.
- **Grandfather-Father-Son (GFS) Retention:** Automatically enforces daily, weekly, and monthly pruning policies while guaranteeing a minimum local snapshot safety floor.
- **Operational Telemetry:** Dispatches execution summaries and failure alerts directly to Telegram channels.

---

## Tech Stack

- **Language:** Python 3.14+
- **Packaging & Environment:** `uv` (`uv_build`)
- **Core Dependencies:** Standard Library first, `docker`, `pyyaml`
- **Backup Engine:** Restic (client-side AES-256-GCM encryption and deduplication)
- **Transport Layer:** Rclone (Google Drive backend)
- **Scheduling:** Linux `systemd --user` timers

---

## Project Structure

```text
kraken-backup/
├── .github/                  # CI workflows (if configured)
├── src/
│   └── kraken_backup/        # Core package source code
│       ├── __init__.py       # Package marker and version metadata
│       ├── cli.py            # Command-line interface entry point
│       ├── config.py         # Configuration models and validation
│       ├── manifest.py       # Snapshot hashing and manifest generation
│       ├── restic.py         # Restic execution client
│       ├── drivers/          # Service dump drivers (MariaDB, PostgreSQL, FS)
│       └── notifiers/        # Telegram and webhook alerts
├── tests/                    # Automated test suite (Python unittest)
│   ├── __init__.py
│   └── test_config.py        # Configuration and contract tests
├── AGENTS.md                 # Copilot pairing contract and invariants
├── pyproject.toml            # Project metadata and dependency definitions
└── README.md                 # Project documentation
```

---

## Getting Started

### Prerequisites

- Python `>= 3.14`
- [`uv`](https://github.com/astral-sh/uv) (version `0.12.19` or higher recommended)
- `restic` and `rclone` installed and configured on the host system
- Docker Engine (with user access to `/var/run/docker.sock`)

### Installation

1. Clone the repository:
   ```bash
   git clone git@github.com:georgesantana/kraken-backup.git
   cd kraken-backup
   ```

2. Initialize the virtual environment and install dependencies:
   ```bash
   uv sync
   ```

3. Run the automated test suite to verify the environment:
   ```bash
   uv run python -m unittest discover -s tests -v
   ```

---

## Usage

### Command Line Interface

KrakenBackup provides a unified CLI via the entry point configured in `pyproject.toml`:

```bash
# Run a scheduled or one-off backup run
uv run kraken-backup run

# Validate configuration without running dumps
uv run kraken-backup verify

# Check status of local snapshots and remote Restic snapshots
uv run kraken-backup status

# Prune snapshots according to retention policy
uv run kraken-backup prune
```

### Configuration

KrakenBackup reads configuration from a YAML file (e.g., `config.yaml`) or environment variables:

```yaml
backup_root: /mnt/storage/backups
min_free_bytes: 10737418240 # 10 GB minimum free disk space
local_retention_days: 3

restic:
  repository: "rclone:gdrive:backups/kraken"
  password_file: "/etc/kraken/restic.key"
  prune_keep_daily: 7
  prune_keep_weekly: 4
  prune_keep_monthly: 12

telegram:
  bot_token_env: "TELEGRAM_BOT_TOKEN"
  chat_id_env: "TELEGRAM_CHAT_ID"
```

---

## Contributing

1. Review the pairing guidelines and invariants in [`AGENTS.md`](AGENTS.md).
2. Create a feature branch: `git checkout -b feat/your-feature`.
3. Ensure all tests pass: `uv run python -m unittest discover -s tests -v`.
4. Commit your changes using Conventional Commits: `feat(scope): ...`.
5. Open a Pull Request detailing the changes and verification steps.

---

## License

This project is licensed under the terms of the MIT License. See [LICENSE](LICENSE) for details.
