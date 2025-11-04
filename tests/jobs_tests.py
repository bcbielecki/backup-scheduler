import unittest
import abackup.jobs as jobs
from pathlib import Path
from datetime import time, tzinfo
from zoneinfo import ZoneInfo

def InitializeJobWithGoodValues():
    job = jobs.BackupJob()
    job.status = jobs.JobStatus.SCHEDULED
    job.source_path = Path(".")  # Current directory should exist
    job.recursive = True
    job.compression = True
    job.BackupType = jobs.BackupType.GOOGLEDRIVE
    job.destination_url = "file:///backup/location"
    job.max_file_retention_size = 1024  # 1 GB
    job.retention_policy = jobs.BackupRetentionPolicy.DELETE_OLDEST
    job.schedule_time = time(2, 0, tzinfo=ZoneInfo("America/Los_Angeles"))# 2:00 AM PST
    job.schedule_recurrence_policy = jobs.JobRecurrence.DAILY
    job.script_pre_path = None
    job.script_post_path = None
    return job

class TestJobDataValidation(unittest.TestCase):

    def test_valid_job(self):
        job = InitializeJobWithGoodValues()
        try:
            job.validate()  # Should not raise
        except ValueError:
            self.fail("BackupJob.validate() raised ValueError unexpectedly!")

    def test_invalid_job_status(self):
        job = InitializeJobWithGoodValues()
        job.status = "invalid_status"
        with self.assertRaises(ValueError) as context:
            job.validate()

    def test_null_job_status(self):
        job = InitializeJobWithGoodValues()
        job.status = jobs.JobStatus.NULL
        with self.assertRaises(ValueError) as context:
            job.validate()
    
    def test_invalid_source_path(self):
        job = InitializeJobWithGoodValues()
        job.source_path = "not_a_path_object"
        with self.assertRaises(ValueError) as context:
            job.validate()
    
    def test_nonexistent_source_path(self):
        job = InitializeJobWithGoodValues()
        job.source_path = Path("/path/that/does/not/exist")
        with self.assertRaises(ValueError) as context:
            job.validate()
    
    def test_valid_source_path(self):
        job = InitializeJobWithGoodValues()
        job.status = jobs.JobStatus.SCHEDULED
        job.source_path = Path(".")  # Current directory should exist
        try:
            job.validate()  # Should not raise
        except ValueError:
            self.fail("validate() raised ValueError unexpectedly!")
    
    def test_invalid_recursive_flag(self):
        job = InitializeJobWithGoodValues()
        job.source_path = Path(".")
        job.recursive = "not_a_boolean"
        with self.assertRaises(ValueError) as context:
            job.validate()

if __name__ == '__main__':
    unittest.main()