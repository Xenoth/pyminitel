import threading, time, redis, pickle

from helldivers_api import WarStatus

war_status = None

class HelldiversRefresher():

    _instance = None 
    _lock = threading.Lock() 

    def __new__(cls):
        if cls._instance is None: 
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        self._redis = redis.Redis()
        self.interval = 3600

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
            time.sleep(self.interval)

    def refreshWarStatus(self):
        print("Refreshing War Status...")
        self._redis.set('war', pickle.dumps(WarStatus()));
        print("War Status Updated.")

    def getWarStatus(self):
        return self._redis.get('war')
    

