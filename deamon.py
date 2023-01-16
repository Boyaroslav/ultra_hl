class Deamon:
    def __init__(self, name, is_async=None, keys=[]):
        self.name = name
        self.is_async = is_async
        self.keys = keys
    
    def run(self, window ,keys_arr):
        self.name(window, *keys_arr)