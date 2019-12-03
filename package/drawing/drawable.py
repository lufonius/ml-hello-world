from abc import abstractmethod, ABCMeta
from typing import Union, List


class Drawable:
    @abstractmethod
    def get_y_each(self, x: float) -> List[int]:
        raise NotImplementedError
