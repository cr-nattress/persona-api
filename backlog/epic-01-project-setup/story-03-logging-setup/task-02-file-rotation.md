# TASK-01-03-02: Setup Log File Rotation and Cleanup

**Story:** US-01-03

**Estimated Time:** 5 minutes

**Description:** Configure log file rotation and retention policies for production stability.

## Agent Prompt

You are implementing **EPIC-01: Project Setup & Infrastructure**.

**Goal:** Update logging.py to include proper file rotation and cleanup policies.

**Context:** Log files can grow unbounded without rotation. Proper rotation prevents disk space issues and keeps logs manageable.

**Instructions:**

1. Update the file handler in `app/core/logging.py` with rotation settings:
   - Daily rotation at midnight (rotation="00:00")
   - Keep 7 days of logs (retention="7 days")
   - Maximum file size check (rotation="500 MB" for large production logs)

2. Create a cleanup function:

```python
def cleanup_old_logs(days_to_keep: int = 7) -> None:
    \"\"\"Remove log files older than specified days.\"\"\"
    from datetime import datetime, timedelta
    import glob

    log_dir = Path("logs")
    cutoff_time = datetime.now() - timedelta(days=days_to_keep)

    for log_file in glob.glob(str(log_dir / "*.log")):
        file_mtime = datetime.fromtimestamp(Path(log_file).stat().st_mtime)
        if file_mtime < cutoff_time:
            Path(log_file).unlink()
            logger.info(f"Deleted old log file: {log_file}")
```

## Verification Steps

1. Verify rotation configuration exists in logging.py
2. Test log rotation settings are applied
3. Verify logs directory structure

## Expected Output

Logging configuration with:
- Daily rotation at midnight
- 7-day retention
- Cleanup function available

## Commit Message

```
feat(logging): add file rotation and retention policies

Configure daily log rotation with 7-day retention and cleanup function for production stability.
```

---

**Completion Time:** ~5 minutes
**Dependencies:** TASK-01-03-01
