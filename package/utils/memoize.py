class Memoize:

    def __init__(self, fn):
        self.fn = fn
        self.memo = {}

    def __call__(self, *args):
        if args[0] not in self.memo:
            self.memo[args[0]] = self.fn(None, args[0])
        return self.memo[args[0]]
