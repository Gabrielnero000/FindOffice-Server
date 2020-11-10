from backend.db import Database

class Api:
    def __init__(self):
        self._db = Database.getInstance()