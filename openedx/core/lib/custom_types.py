
class Disposable:
    def __init__(self):
        pass
    def __enter__(self):
        return object()
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
