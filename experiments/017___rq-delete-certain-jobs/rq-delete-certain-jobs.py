#%%
import os

import cloudpickle
from redis import Redis
from rq import Queue, Retry
from rq.exceptions import InvalidJobOperation
from rq.job import Job

redis = Redis(
    host=os.environ.get("REDIS_HOST"),
    port=os.environ.get("REDIS_PORT"),
    password=os.environ.get("REDIS_PASSWORD"),
    ssl=True,
)


def get_job(registry, job_or_id):
    if isinstance(job_or_id, registry.job_class):
        job = job_or_id
    else:
        job = registry.job_class.fetch(job_or_id, connection=registry.connection)

    return job


queue = Queue(name="fix-fitting-time", connection=redis)
job_ids = queue.failed_job_registry.get_job_ids()
for job_id in job_ids:
    job = get_job(queue, job_id)
    job.delete()
    print(f"{job_id}")

    # job.delete()
    # print(f"✓ dequeue'd job: {job.description} ({job_id})")

    # with queue.connection.pipeline() as pipeline:
    #     job.started_at = None
    #     job.ended_at = None
    #     job.retry = Retry(max=3, interval=60)
    #     job.save()
    #     job = queue.enqueue_job(job, pipeline=pipeline)
    #     pipeline.execute()
