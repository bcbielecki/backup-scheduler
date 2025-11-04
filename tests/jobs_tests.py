import unittest
import abackup.jobs as jobs
from pathlib import Path
from datetime import time, tzinfo
from zoneinfo import ZoneInfo

def InitializeJobWithGoodValues():
    job = jobs.BackupJob("test-job-001")
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

    def test_invalid_job_id_none(self):
        job = InitializeJobWithGoodValues()
        job.job_id = None
        with self.assertRaises(ValueError) as context:
            job.validate()
    
    def test_invalid_job_id_empty(self):
        job = InitializeJobWithGoodValues()
        job.job_id = "   "
        with self.assertRaises(ValueError) as context:
            job.validate()
    
    def test_invalid_job_id_not_string(self):
        job = InitializeJobWithGoodValues()
        job.job_id = 12345  # Not a string
        with self.assertRaises(ValueError) as context:
            job.validate()

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
    
    def test_invalid_compression_flag(self):
        job = InitializeJobWithGoodValues()
        job.compression = "not_a_boolean"
        with self.assertRaises(ValueError) as context:
            job.validate()
    
    def test_invalid_backup_type(self):
        job = InitializeJobWithGoodValues()
        job.BackupType = "invalid_backup_type"
        with self.assertRaises(ValueError) as context:
            job.validate()
    
    def test_null_backup_type(self):
        job = InitializeJobWithGoodValues()
        job.BackupType = jobs.BackupType.NULL
        with self.assertRaises(ValueError) as context:
            job.validate()

    def test_invalid_destination_url(self):
        job = InitializeJobWithGoodValues()
        job.destination_url = 12345  # Not a string
        with self.assertRaises(ValueError) as context:
            job.validate()

    def test_invalid_max_file_retention_size_type(self):
        job = InitializeJobWithGoodValues()
        job.max_file_retention_size = "not_an_integer"
        with self.assertRaises(ValueError) as context:
            job.validate()
    
    def test_invalid_max_file_retention_size_in_range(self):
        job = InitializeJobWithGoodValues()
        job.max_file_retention_size = -100  # Negative size
        with self.assertRaises(ValueError) as context:
            job.validate()
    
    def test_invalid_retention_policy(self):
        job = InitializeJobWithGoodValues()
        job.retention_policy = "invalid_policy"
        with self.assertRaises(ValueError) as context:
            job.validate()

    def test_invalid_recurrence_policy(self):
        job = InitializeJobWithGoodValues()
        job.schedule_recurrence_policy = "invalid_recurrence"
        with self.assertRaises(ValueError) as context:
            job.validate()
    
    def test_invalid_pre_script_path(self):
        job = InitializeJobWithGoodValues()
        job.script_pre_path = "not_a_path_object"
        with self.assertRaises(ValueError) as context:
            job.validate()
    
    def test_nonexistent_pre_script_path(self):
        job = InitializeJobWithGoodValues()
        job.script_pre_path = Path("/path/that/does/not/exist")
        with self.assertRaises(ValueError) as context:
            job.validate()

    def test_valid_pre_script_path_none(self):
        job = InitializeJobWithGoodValues()
        job.script_pre_path = None  # No script, should be valid
        try:
            job.validate()  # Should not raise
        except ValueError:
            self.fail("validate() raised ValueError unexpectedly!")

    def test_valid_pre_script_path(self):
        job = InitializeJobWithGoodValues()
        job.script_pre_path = Path(".")  # Current directory should exist
        try:
            job.validate()  # Should not raise
        except ValueError:
            self.fail("validate() raised ValueError unexpectedly!")
    
    def test_invalid_post_script_path(self):
        job = InitializeJobWithGoodValues()
        job.script_post_path = "not_a_path_object"
        with self.assertRaises(ValueError) as context:
            job.validate()
    
    def test_nonexistent_post_script_path(self):
        job = InitializeJobWithGoodValues()
        job.script_post_path = Path("/path/that/does/not/exist")
        with self.assertRaises(ValueError) as context:
            job.validate()
    
    def test_valid_post_script_path_none(self):
        job = InitializeJobWithGoodValues()
        job.script_post_path = None  # No script, should be valid
        try:
            job.validate()  # Should not raise
        except ValueError:
            self.fail("validate() raised ValueError unexpectedly!")
    
    def test_valid_post_script_path(self):
        job = InitializeJobWithGoodValues()
        job.script_post_path = Path(".")  # Current directory should exist
        try:
            job.validate()  # Should not raise
        except ValueError:
            self.fail("validate() raised ValueError unexpectedly!")
    
    def test_invalid_schedule_time_type(self):
        job = InitializeJobWithGoodValues()
        job.schedule_time = "not_a_time_object"
        with self.assertRaises(ValueError) as context:
            job.validate()
    
    def test_invalid_schedule_time_tzinfo(self):
        job = InitializeJobWithGoodValues()
        job.schedule_time = time(2, 0)  # No tzinfo
        with self.assertRaises(ValueError) as context:
            job.validate()
    
    def test_valid_weekly_recurrence_configuration(self):
        job = InitializeJobWithGoodValues()
        job.schedule_recurrence_policy = jobs.JobRecurrence.WEEKLY
        job.schedule_days = [jobs.JobScheduleDays.MONDAY, jobs.JobScheduleDays.WEDNESDAY]
        try:
            job.validate()  # Should not raise
        except ValueError:
            self.fail("validate() raised ValueError unexpectedly!")
    
    def test_invalid_weekly_recurrence_configuration(self):
        job = InitializeJobWithGoodValues()
        job.schedule_recurrence_policy = jobs.JobRecurrence.WEEKLY
        job.schedule_days = "not_a_list"
        with self.assertRaises(ValueError) as context:
            job.validate()
    
    def test_invalid_weekly_recurrence_configuration_invalid_day(self):
        job = InitializeJobWithGoodValues()
        job.schedule_recurrence_policy = jobs.JobRecurrence.WEEKLY
        job.schedule_days = [jobs.JobScheduleDays.MONDAY, "invalid_day"]
        with self.assertRaises(ValueError) as context:
            job.validate()
    
    def test_valid_monthly_recurrence_configuration(self):
        job = InitializeJobWithGoodValues()
        job.schedule_recurrence_policy = jobs.JobRecurrence.MONTHLY
        job.schedule_day_of_month = 15
        try:
            job.validate()  # Should not raise
        except ValueError:
            self.fail("validate() raised ValueError unexpectedly!")
    
    def test_invalid_monthly_recurrence_configuration_invalid_day_high(self):
        job = InitializeJobWithGoodValues()
        job.schedule_recurrence_policy = jobs.JobRecurrence.MONTHLY
        job.schedule_day_of_month = 32  # Invalid day
        with self.assertRaises(ValueError) as context:
            job.validate()
    
    def test_invalid_monthly_recurrence_configuration_invalid_day_low(self):
        job = InitializeJobWithGoodValues()
        job.schedule_recurrence_policy = jobs.JobRecurrence.MONTHLY
        job.schedule_day_of_month = 0  # Invalid day
        with self.assertRaises(ValueError) as context:
            job.validate()
    
    def test_valid_daily_recurrence_configuration(self):
        job = InitializeJobWithGoodValues()
        job.schedule_recurrence_policy = jobs.JobRecurrence.DAILY
        job.schedule_time = time(3, 0, tzinfo=ZoneInfo("America/Los_Angeles"))
        try:
            job.validate()  # Should not raise
        except ValueError:
            self.fail("validate() raised ValueError unexpectedly!")


if __name__ == '__main__':
    unittest.main()