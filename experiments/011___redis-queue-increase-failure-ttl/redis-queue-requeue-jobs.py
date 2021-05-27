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
def requeue(registry, job_or_id):
    """Requeues the job with the given job ID."""
    if isinstance(job_or_id, registry.job_class):
        job = job_or_id
    else:
        job = registry.job_class.fetch(job_or_id, connection=registry.connection)

    result = registry.connection.zrem(registry.key, job.id)
    if not result:
        raise InvalidJobOperation

    with registry.connection.pipeline() as pipeline:
        queue = Queue(
            job.origin, connection=registry.connection, job_class=registry.job_class
        )
        job.started_at = None
        job.ended_at = None
        job.failure_ttl = 5184000  # 60 days
        job.save()
        job = queue.enqueue_job(job, pipeline=pipeline)
        pipeline.execute()
    return job


#%%
registry = queue.failed_job_registry
for job_id in registry.get_job_ids():
    requeue(registry, job_id)
    print(f"requeue'd job {job_id} with 60 days failure ttl")
