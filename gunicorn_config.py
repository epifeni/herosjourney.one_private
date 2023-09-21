bind = '127.0.0.1:8000'  # The host and port Gunicorn will bind to
workers = 2  # The number of worker processes to spawn
timeout = 120  # The maximum time (in seconds) a worker can be idle before being restarted