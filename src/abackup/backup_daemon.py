
# There should only ever be **one** Backup Daemon instance running per system.
# This daemon will be responsible for starting/stopping the scheduler, executing the jobs,
# and handling any system-level interactions required for background operation.

# The cli commands should be able to find/reach this daemon instance to run commands.
# To do so, it should use BackupDaemon as an abstraction layer for platform-specific implementations.


class BackupDaemon():
    # Ensure singleton behavior
    # Abstract Base Class
    pass

class Win32BackupDaemon(BackupDaemon):
    pass
    '''
    import win32serviceutil
    import win32service
    import win32event
    '''
    # Check the above imports for Windows service implementation - win32serviceutil.ServiceFramework?

class UnixBackupDaemon(BackupDaemon):
    pass


    '''
    # my_scheduler.service
    [Unit]
    Description=My Python Scheduler Service
    After=network.target

    [Service]
    Type=simple
    User=your_username
    ExecStart=/usr/bin/python3 /path/to/your/script.py
    Restart=always

    [Install]
    WantedBy=multi-user.target
    '''
    # First time setup should include the above service file in /etc/systemd/system/

    '''
    import daemon
    '''
    # Check the above import for Unix daemon implementation - python-daemon or daemon?