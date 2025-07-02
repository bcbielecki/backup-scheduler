# backup-scheduler
A primitive python-based tool which maintains information about and shedules rclone backups. The tool also exposes an unprotected (local use only) REST-ful web API meant for querying info about scheduled and past backup operations.

# Dependencies
- build-essential libssl-dev python-dev [See Why...](https://pypi.org/project/scrypt/])
- rclone

# Supported Systems
Debian and Ubuntu