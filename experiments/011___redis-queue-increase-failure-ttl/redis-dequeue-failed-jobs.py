#%%
import os

import cloudpickle
from redis import Redis
from rq import Queue
from rq.exceptions import InvalidJobOperation
from rq.job import Job

redis = Redis(
    host=os.environ.get("REDIS_HOST"),
    port=os.environ.get("REDIS_PORT"),
    password=os.environ.get("REDIS_PASSWORD"),
    ssl=True,
)
queue = Queue(connection=redis)

#%%
def dequeue(registry, job_or_id):
    """Dequeues the job with the given job ID."""
    if isinstance(job_or_id, registry.job_class):
        job = job_or_id
    else:
        job = registry.job_class.fetch(job_or_id, connection=registry.connection)

    result = registry.connection.zrem(registry.key, job.id)
    if not result:
        raise InvalidJobOperation

    return job


#%%
registry = queue.failed_job_registry
for job_id in registry.get_job_ids():
    dequeue(registry, job_id)
    print(f"dequeue'd job {job_id}")
