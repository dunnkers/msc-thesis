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
def get_job(registry, job_or_id):
    """Gets the Job with the given job ID."""
    if isinstance(job_or_id, registry.job_class):
        job = job_or_id
    else:
        job = registry.job_class.fetch(job_or_id, connection=registry.connection)

    return job


def get_job_return(job):
    if job.result and not isinstance(job.result, str):
        result = cloudpickle.loads(job.result)
    else:
        result = job.result

    return result


registry = queue.finished_job_registry
job = get_job(registry, "20d880a4-0046-47ca-b5e8-c6602a99a1fc")
job_return = get_job_return(job)
print(job_return)

# %%
