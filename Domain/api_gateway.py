from abc import ABC, abstractmethod


class ISwitchBotGateway(ABC):
    @abstractmethod
    def send_toggle_switch(self, device_id):
        pass
