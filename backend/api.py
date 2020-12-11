from backend.db import Database

class Api:
    def __init__(self, today):
        self._today = today
        self._db = Database.getInstance()