from abc import ABC, abstractmethod


class AbstractMailClient(ABC):
    @abstractmethod
    def __init__(self):
        super().__init__()

    @abstractmethod
    def _build_url(self):
        pass

    @abstractmethod
    def _make_request(self):
        pass

    @abstractmethod
    def send_message(self):
        pass

    @abstractmethod
    def generate_message(self):
        pass

    @abstractmethod
    def generate_event(self):
        pass
