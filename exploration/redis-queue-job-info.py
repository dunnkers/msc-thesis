import os

import cloudpickle
from redis import Redis
from rq import Queue
from rq.job import Job

redis = Redis(
    host=os.environ.get('REDIS_HOST'),
    port=os.environ.get('REDIS_PORT'),
    password=os.environ.get('REDIS_PASSWORD'),
    ssl=True
)
queue = Queue(connection=redis)

def get_job(job_id):
    job = Job.fetch(job_id, connection=redis)
    data = cloudpickle.loads(job.data)
    _func_name, _instance, _args, _kwargs = cloudpickle.loads(job.data)
    print(job.enqueued_at, _func_name, _args)

def get_last_n_finished_jobs(n):
    registry = queue.finished_job_registry
    job_ids = registry.get_job_ids(start=registry.count - n)
    return job_ids

for job_id in get_last_n_finished_jobs(10):
    job_info = get_job(job_id)
    
