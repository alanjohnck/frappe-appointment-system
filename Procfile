web: bash -c "pip install -r requirements.txt && bench serve --port 8000"
redis_cache: redis-server config/redis_cache.conf
redis_queue: redis-server config/redis_queue.conf
socketio: node apps/frappe/socketio.js
watch: bench watch
schedule: bench schedule
worker: bash -c "bench worker 1>> logs/worker.log 2>> logs/worker.error.log"
