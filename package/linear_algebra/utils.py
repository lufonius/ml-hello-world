class Utils:
    @staticmethod
    def within_range(start, end, value) -> bool:
        if start == end:
            raise Exception("dude what are you doing!")

        if start > end:
            return end <= value <= start

        if start < end:
            return start <= value <= end