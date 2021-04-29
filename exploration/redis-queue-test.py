#%%
import os
import sys
from rq import Queue
from redis import Redis
from redis_queue_module import count_words_at_url

q = Queue(connection=Redis(
    host=os.environ.get('REDIS_HOST'),
    port=os.environ.get('REDIS_PORT'),
    password=os.environ.get('REDIS_PASSWORD'),
    ssl=True
))

result = q.enqueue(count_words_at_url, sys.argv[1])
print('enqued 1 job')
print('jobs:', q.jobs)

#%%
