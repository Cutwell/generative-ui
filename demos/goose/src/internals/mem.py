class MemCache():
    def __init__(self):
        self.cache = {}

    def set(self, key, value):
        self.cache[key] = value
        
    def get(self, key):
        if key in self.cache:
            return self.cache[key]
        else:
            return None
        
    def delete(self, key):
        if key in self.cache:
            del self.cache[key]
            return True
        else:
            return False
