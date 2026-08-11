# Backup, Retention & Recovery

## Backup scope
SQLite DB, configuration metadata, semantic manifests, model registry/artifacts, report metadata/artifacts, dataset metadata; raw/processed analytical data inclusion configurable.

## Requirements
- Manual Admin backup in v1.0.
- Restore validates manifest/checksums/version compatibility before replacing active state.
- Backup/restore operations are audited.
- Retention policies support simulation/log/report/data lifecycle.
- Deletion is dependency aware to avoid orphan model/run references.
