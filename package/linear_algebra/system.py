from .hand import Hand

class System():
    def __init__(self, hand = Hand.right):
        self.hand = hand