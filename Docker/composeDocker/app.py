import time
from flask import Flask
import redis

app=Flask(__name__)
cache=redis.Redis(host='redis',port=6397)


def get_hit_count():
    retries=5
    
    while True:
        try:
            #cache.reset_retry_count()  
            return cache.incr('hits')
        except redis.exceptions.ConnectionErroras as exc:
            if retries==0:
                raise exc
            retries-=1
            time.sleep(0.5)

@app.route('/')
def hello():
    count=get_hit_count()
    return  "Hello Jeevan! I have been Seen {} times.\n".format(count) 
  


