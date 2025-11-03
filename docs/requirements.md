

# Core Functionality

This is a lightweight backup utility which wraps a subset of RClone features, chiefly file copying to Amazon S3 services. The tool shall support the following capabilities:
- Scheduling backup jobs from local directories to Amazon S3 buckets
  - This can be done centrally via a config .yaml file OR a shell command which alters the file for you
- Performing scheduled file transfers using RClone
- Storing credentials needed to perform Amazon S3 operations
- [Optionally] Running a FastAPI-based web service for remotely retrieving information about scheduled backups and recently performed backups
- Running custom scripts alongside scheduled backups to support backups to services which may need to be temporarily shutdown or otherwised altered during file transfer
  - This will only be supported via .yaml
- Queueing active backup jobs so only one occurs at a time

The following sections outline what user input for the backup tool may look like.

## Example Scheduler YAML

```yaml
version: 0.0
jobs:
    backup-job-1:
        location: /usr/home/myfiles
        recursive: true
        compression: true
        destination: http://bucket-name.s3-website-Region.amazonaws.com
        schedule:
            time: 2:30
            timezone: PST
            days: MWF
        scripts:
            pre: /usr/home/myscript.sh
            post: /usr/home/myotherscript.sh
        retention: 3
        max-retention-size: 15GB

    backup-job-2:
        location: /usr/home/myfiles2
        recursive: true
        compression: false
        destination: http://bucket-name-2.s3-website-Region.amazonaws.com
        schedule:
            time: 18:00
            timezone: CST
            days: F
```

## Example Commands

- `abackup job create [location] [destination] [name] [frequency]`
  - Create a backup job and add it to the core yaml config file
- `abackup list`
  - List all scheduled backups in the shell
- `abackup abort [job name]`
  - Abort an active backup operation
- `abackup start [job name]`
  - Manually trigger a backup operation
  - Cannot do more than one backup operation concurrently for the same backup name
- `abackup down`
  - Do not trigger any scheduled backups until the `up` command is used
- `abackup up`
  - Allow regularly scheduled backups
- `abackup webapi up [port]`
  - Open an HTTP server at the given port (or 7080) by default
- `abackup webapi down`
  - Shutdown the HTTP server
- `abackup schedule update`
  - Update the service based on changes made to the config .yaml file at the set location
- `abackup schedule set [location]`
  - Configures the service to use the config .yaml file at the given location. The file is copied to a temporary location, which is consumed by the service at runtime.
