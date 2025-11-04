from enum import Enum
from pathlib import Path
from datetime import time, tzinfo

# Job class

# <bcbielecki> 2025-11-02 alphaV0.1
# Description of Job Statuses:
#    - RUNNING: Job is currently executing
#    - COMPLETED: Job has succeeded and logs are being saved
#    - FAILED: Job has failed and logs are being saved
#    - SCHEDULED: Job is scheduled to run at a future time, but it is not queued
#    - DISABLED: Job is disabled and will not run, even if its schedule time arrives
#    - QUEUED: Job is queued because its schedule time arrived and is waiting for execution
#    - NULL: Job has no status—either it is the default value at initialization or something went wrong
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
#   - NULL: No backup type specified—either it is the default value at initialization or something went wrong
# TODO: Add more backup types in the future (e.g., Local, OneDrive, FTP, S3, etc.)
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
# These values are more self-explanatory, but one should expect that with each value,
# different properties will be needed to specify the job schedule
class JobRecurrence(Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

# <bcbielecki> 2025-11-02 alphaV0.1
# Days of the week for scheduling purposes—should be used in conjunction with
# JobRecurrence.WEEKLY
class JobScheduleDays(Enum):
    MONDAY = "M"
    TUESDAY = "T"
    WEDNESDAY = "W"
    THURSDAY = "R"
    FRIDAY = "F"
    SATURDAY = "U"
    SUNDAY = "S"

# <bcbielecki> 2025-11-02 alphaV0.1
# An instance of the BackupJob class represents a job that will be executed by the core system.
# The job may also exist in the BackupSchedule. This is a dumb object, meaning it should
# only hold data; it shouldn't have any execution logic, only some validation code.
class BackupJob:

    # See comment below about unique job IDs
    # __job_id_set = {}

    def __init__(self, job_id):

        # I think this logic should be done at a higher level, perhaps in the Schedule class
        # if job_id in BackupJob.__job_id_set:
        #     raise ValueError(f"Job ID '{job_id}' already exists. Job IDs must be unique.")
        self.__job_id = job_id

        # Initialize some default values

        self.status = JobStatus.NULL

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
        self.schedule_time = None # Should be a datetime.time object w/ timezone specified
        self.schedule_days = [] # Should be a list of JobScheduleDays enum values—meant only for JobRecurrence.WEEKLY
        self.schedule_day_of_month = None # Should be an integer between 1 and 31—meant only for JobRecurrence.MONTHLY
        self.schedule_recurrence_policy = JobRecurrence.DAILY

        # Backup script settings (Optional)
        self.script_pre_path = None # Should be a Path object
        self.script_post_path = None # Should be a Path object 

    @property
    def job_id(self):
        return self.__job_id

    # Define equality and hashing based on job_id to ensure uniqueness in sets
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.job_id == other.job_id

    def __hash__(self):
        return hash(self.job_id)

    def __repr__(self):
        return f"BackupJob(ID={self.job_id})"    

    def validate(self):
        # This is where we can validate all the job properties

        if self.job_id is None or not isinstance(self.job_id, str) or self.job_id.strip() == "":
            raise ValueError("Job ID must be a non-empty string.")

        if self.status not in JobStatus:
            raise ValueError(f"Invalid job status: {self.status}")
        elif self.status == JobStatus.NULL:
            raise ValueError("Job status cannot be NULL.")
        
         # Backup source file/folder settings
        if not isinstance(self.source_path, Path):
            raise ValueError("Source path must be a valid Path object.")
        if not self.source_path.exists():
            raise ValueError(f"Source path '{self.source_path}' does not exist.")
        if not isinstance(self.recursive, bool):
            raise ValueError("Recursive flag must be a boolean value.")
        
        # Backup destination settings
        if not isinstance(self.compression, bool):
            raise ValueError("Compression flag must be a boolean value.")
        
        if self.BackupType not in BackupType:
            raise ValueError(f"Invalid backup type: {self.BackupType}")
        elif self.BackupType == BackupType.NULL:
            raise ValueError("Backup type cannot be NULL.")
        
        if not isinstance(self.destination_url, str):
            raise ValueError("Destination URL must be a valid string.")
        
        if self.max_file_retention_size is not None:
            if not isinstance(self.max_file_retention_size, int) or self.max_file_retention_size <= 0:
                raise ValueError("Max file retention size must be a positive integer in MB.")
            
        if self.retention_policy not in BackupRetentionPolicy:
            raise ValueError(f"Invalid retention policy: {self.retention_policy}")

        # Backup scheduling settings
        self._validate_schedule_time()
        
        if self.schedule_recurrence_policy in JobRecurrence:
            if self.schedule_recurrence_policy == JobRecurrence.WEEKLY:
                self._validate_weekly_schedule()
            elif self.schedule_recurrence_policy == JobRecurrence.MONTHLY:    
                self._validate_monthly_schedule()
            elif self.schedule_recurrence_policy == JobRecurrence.DAILY:
                self._validate_daily_schedule()
            else:
                raise ValueError(f"Recurrence policy with unimplemented validation: {self.schedule_recurrence_policy}")
        else:
            raise ValueError(f"Invalid recurrence policy: {self.schedule_recurrence_policy}")

        # Backup script settings
        if self.script_pre_path is not None:
            if not isinstance(self.script_pre_path, Path):
                raise ValueError("Pre-backup script path must be a valid Path object.")
            if not self.script_pre_path.exists():
                raise ValueError(f"Pre-backup script path '{self.script_pre_path}' does not exist.")
        if self.script_post_path is not None:
            if not isinstance(self.script_post_path, Path):
                raise ValueError("Post-backup script path must be a valid Path object.")
            if not self.script_post_path.exists():
                raise ValueError(f"Post-backup script path '{self.script_post_path}' does not exist.")
            
    # Private validation methods

    def _validate_schedule_time(self):
        if self.schedule_time is not None:
            if isinstance(self.schedule_time, time):
                if self.schedule_time.tzinfo is None:
                    raise ValueError("Schedule time must have timezone information.")
            else:
                raise ValueError("Schedule time must be a valid datetime.time object.")

    def _validate_weekly_schedule(self):
        if not isinstance(self.schedule_days, list):
            raise ValueError("Schedule days must be a list of JobScheduleDays enum values.")
        for day in self.schedule_days:
            if day not in JobScheduleDays:
                raise ValueError(f"Invalid schedule day: {day}")

    def _validate_monthly_schedule(self):
        if self.schedule_day_of_month is not None:
            if not isinstance(self.schedule_day_of_month, int) or not (1 <= self.schedule_day_of_month <= 31):
                raise ValueError("Schedule day of month must be an integer between 1 and 31.")

    def _validate_daily_schedule(self):
        pass  # No additional validation needed for daily recurrence

# Job Queue class