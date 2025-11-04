from abackup.jobs import BackupJob, JobStatus, JobRecurrence
from datetime import datetime


class BackupJobPool(set):
    def __init__(self):
        super().__init__()
        self.__job_pool_by_id = set()

    def add(self, o: BackupJob):
        if not isinstance(o, BackupJob):
            raise ValueError("Only BackupJob instances can be added to the job pool.")
        if o in self.job_pool:
            return ValueError("Job with id '{job.job_id}' already exists in the scheduler.")
        o.validate() # Will raise ValueError if invalid
        
        self.__job_pool_by_id.add(o.job_id)
        super().add(o)
    
    def __contains__(self, o: BackupJob):
        return isinstance(o, BackupJob) and o.job_id in self.__job_pool_by_id
    
    def get_by_id(self, job_id: str) -> BackupJob | None:
        for job in self:
            if job.job_id == job_id:
                return job
        return None
    
    def remove_by_id(self, job_id: str):
        job_to_remove = self.get_by_id(job_id)
        if job_to_remove:
            super().remove(job_to_remove)
            self.__job_pool_by_id.remove(job_id)


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
        self.job_pool = BackupJobPool()

    '''
    Adds a BackupJob to the scheduler's job pool after validating it.
    May return ValueError if the job is invalid or already exists.
    '''
    def add_job(self, job):
        # Jobs are validated in the BackupJobPool.add() method
        self.job_pool.add(job)
    
    '''
    Removes a BackupJob from the scheduler's job pool by its job ID.
    May return True if the job was found and removed, False otherwise.
    '''
    def remove_job_by_id(self, job_id) -> bool:
        return self.job_pool.remove_by_id(job_id)

    '''
    Returns a list of BackupJob instances that are ready to be executed
    at the given date_time.
    '''
    def get_ready_jobs(self, date_time: datetime) -> list(BackupJob):
        ready_jobs = []
        for job in self.job_pool:
            if job.status == JobStatus.SCHEDULED:
                match job.schedule_recurrence_policy:
                    case JobRecurrence.DAILY:
                        if job.schedule_time >= date_time.time():
                            ready_jobs.append(job)
                    case JobRecurrence.WEEKLY:
                        if (job.schedule_time >= date_time.time() and
                            date_time.weekday() in (day.value for day in job.schedule_days)):
                            ready_jobs.append(job)
                    case JobRecurrence.MONTHLY:
                        if (job.schedule_time >= date_time.time() and
                            job.schedule_day_of_month >= date_time.day):
                            ready_jobs.append(job)
                    case _: # Wildcard for default case
                        ValueError(f"Invalid job recurrence policy: {job.schedule_recurrence_policy}")
        return ready_jobs

