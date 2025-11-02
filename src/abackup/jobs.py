from enum import Enum
from pathlib import Path
from urllib.parse import urlparse

# Job class

# <bcbielecki> 2025-11-02 alphaV0.1
# Description of Job Statuses:
#    - RUNNING: Job is currently executing
#    - COMPLETED: Job has succeeded and logs are being saved
#    - FAILED: Job has failed and logs are being saved
#    - SCHEDULED: Job is scheduled to run at a future time, but it is not queued
#    - DISABLED: Job is disabled and will not run, even if its schedule time arrives
#    - QUEUED: Job is queued because its schedule time arrived and is waiting for execution
#    - NULL: Job has no status -either it is the default value at initialization or something went wrong
class JobStatus(Enum):
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SCHEDULED = "scheduled"
    DISABLED = "disabled"
    QUEUED = "queued"
    NULL = "null"

# <bcbielecki> 2025-11-02 alphaV0.1
# The BackupType enum defines the types of backup destinations supported.
# Currently supported types are:
#   - GOOGLEDRIVE: Backup to Google Drive
#   - NULL: No backup type specified -either it is the default value at initialization or something went wrong
class BackupType(Enum):
    GOOGLEDRIVE = "Google Drive"
    NULL = "null"

# <bcbielecki> 2025-11-02 alphaV0.1
# Description of Backup Retention Policies:
#    - KEEP_ALL: Keep all backup files indefinitely. If a maximum retention size is reached, new backup jobs will fail.
#    - DELETE_OLDEST: Delete the oldest backup files when the maximum retention size is exceeded
class BackupRetentionPolicy(Enum):
    KEEP_ALL = "keep_all"
    DELETE_OLDEST = "delete_old"

# <bcbielecki> 2025-11-02 alphaV0.1
# An instance of the BackupJob class represents a job that will be executed by the core system.
# The job may also exist in the BackupSchedule. This is a dumb object, meaning it should
# only hold data; it shouldn't have any execution logic, only some validation code.
class BackupJob:

    __job_id_set = {}

    def __init__(self, job_id):

        if job_id in BackupJob.__job_id_set:
            raise ValueError(f"Job ID '{job_id}' already exists. Job IDs must be unique.")
        self.job_id = job_id

        # Initialize some default values

        self.status = JobStatus.DISABLED

        # Backup source file/folder settings
        self.source_path = None # Should be a Path object
        self.recursive = True

        # Backup destination settings
        self.compression = True
        self.BackupType = BackupType.NULL
        self.destination_url = None # Should be a URL string
        self.max_file_retention_size = None # Should be an interger in MB
        self.retention_policy = BackupRetentionPolicy.DELETE_OLDEST
        
        # Backup scheduling settings
        # self.schedule_time = 2:30
        # self.schedule_timezone: PST
        # self.schedule_days: MWF

        # # Backup script settings
        # scripts:
        #     pre: /usr/home/myscript.sh
        #     post: /usr/home/myotherscript.sh
        # retention: 3
        

    def validate(self):
        # This is where we can validate all the job properties
        pass

# Job Queue class