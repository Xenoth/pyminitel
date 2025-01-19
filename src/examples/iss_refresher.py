import threading, time, redis, pickle, os, datetime

from logging import log, DEBUG, ERROR, WARNING

from iss_api import ISS_API

war_status = None

class ISSRefresher():

    _instance = None
    _lock = threading.Lock() 
    INTERVAL = 600

    KEY_PREFIX = "ISS"
    TIME_OF_LIFE = 6000

    def add_item(self, value, ttl):
        key_prefix = ISSRefresher.KEY_PREFIX

        item_number = self._redis.incr(f"{key_prefix}:counter")
        key = f"{key_prefix}:item{item_number}"
        self._redis.set(key, value, ex=ttl)
        print(f"Item added : {key} = {value} (expires is {ttl}s)")

    def get_all_items(self, key_prefix):
        keys = self._redis.keys(f"{key_prefix}:*")
        items = {key.decode('utf-8'): self._redis.get(key) for key in keys}
        return items


    def __new__(cls):
        if cls._instance is None: 
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        redis_host = os.getenv("REDIS_HOST", "localhost")
        redis_port = int(os.getenv("REDIS_PORT", 6379))

        self._redis = redis.StrictRedis(host=redis_host, port=redis_port)

        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)
        
    def start(self):
        if not self._thread.is_alive():
            self._thread.start()

    def stop(self):
        self._stop_event.set()
        self._thread.join()

    def _run(self):
        while not self._stop_event.is_set():

            log(DEBUG, "Request the ISS position...")
            self.add_item(pickle.dumps(self.getISSPosition()), ISSRefresher.TIME_OF_LIFE)
            log(DEBUG, "ISS position saved")

            time.sleep(ISSRefresher.INTERVAL)

    def getISSPosition(self):
        iss_pos = ISS_API.getISS()
        if iss_pos is None:
            log(WARNING, 'Issue on retreiving iss position, 3 retry...')
            for i in range(3):
                iss_pos = ISS_API.getISS()
                if iss_pos is not None:
                    return iss_pos
        
        return iss_pos

    def getISSPositions(self):
        iss_positions = []
        items = self.get_all_items(ISSRefresher.KEY_PREFIX)

        for key, value in items.items():
            try:
                if value:
                    iss_position = pickle.loads(value)
                    if iss_position != None:
                        iss_positions.append(iss_position)
            except (pickle.UnpicklingError, TypeError) as e:
                log(ERROR, f"Failed to unpickle value for key {key}: {e}")
        
        ordered_iss_positions = sorted(
            iss_positions,
            key=lambda x: datetime.datetime.fromtimestamp(x.timestamp),
            reverse=True
        )

        return ordered_iss_positions



