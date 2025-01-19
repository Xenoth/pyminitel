import threading, time, redis, pickle, os, datetime

from logging import log, DEBUG

from helldivers_api import WarStatus

war_status = None

class HelldiversRefresher():

    _instance = None
    _lock = threading.Lock() 
    INTERVAL = 600

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
            self.refreshWarStatus()
            time.sleep(HelldiversRefresher.INTERVAL)

    def refreshWarStatus(self):
        log(DEBUG, "Refreshing War Status...")
        self._redis.set('war', pickle.dumps(WarStatus()));
        log(DEBUG, "War Status Updated.")

    def getNextUpdateInSeconds(self) -> int:
        war = pickle.loads(self._redis.get('war'))
        if war is None:
            return None
        return int(HelldiversRefresher.INTERVAL - (datetime.datetime.now() - war.date).total_seconds())
    
    def getWarStatus(self):
        return pickle.loads(self._redis.get('war'))
    

