from abackup.jobs import BackupJob


class BackupJobScheduleFileParser:
    def __init__(self, filepath):
        self.filepath = filepath

    def parse(self) -> list(BackupJob):
        # Logic to parse the YAML file and return a list of BackupJob instances
        pass
    
    def parse_job(self, job_data) -> BackupJob:
        # Logic to parse individual job data and return a BackupJob instance
        pass

# Schedule class

# Holds a job pool and hands jobs to core for execution when
# their scheduled time arrives
class BackupJobScheduler:
    def __init__(self):
        self.job_pool = set()
        self.job_pool_by_id = set()

    '''
    Adds a BackupJob to the scheduler's job pool after validating it.
    May return ValueError if the job is invalid or already exists.
    '''
    def add_job(self, job):
        if not isinstance(job, BackupJob):
            raise ValueError("Only BackupJob instances can be added to the scheduler.")
        if job in self.job_pool:
            return ValueError("This job is already in the scheduler.")
        if job.job_id in self.job_pool_by_id:
            raise ValueError(f"Job ID '{job.job_id}' already exists in the scheduler.")
        job.validate() # Will raise ValueError if invalid
        
        self.job_pool.add(job)
        self.job_pool_by_id.add(job.job_id)

