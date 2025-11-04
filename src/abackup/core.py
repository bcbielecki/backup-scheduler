# Core class

## Stores a job queue
## Polls and regularly calls Update method on queue
## Checks for jobs in queue after update
## If jobs in queue, perform the job, pop from queue


# Food for thought:

# Maybe there should be an abstraction layer for each backup type 
# (i.e. a BackupHandler abstract class) that is implemented for Google Drive, Local,
# OneDrive, FTP, S3, etc. This way, the core backup logic can remain the same.
#
# There should be an abstraction layer for cloud-based backups (i.e. RCloneBackupHandler)
# on top of which specific cloud backup handlers (Google Drive, OneDrive, etc.)
# can be implemented. This way, common logic for cloud backups can be reused.
#
# Class tree could look like this:
# BackupHandler (abstract)
#   |
#   +-- LocalBackupHandler
#   |
#   +-- CloudBackupHandler (abstract)
#         |
#         +-- RCloneBackupHandler (abstract)
#               |
#               +-- GoogleDriveBackupHandler
#               |
#               +-- OneDriveBackupHandler
#               |