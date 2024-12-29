from Domain.api_gateway import ISwitchBotGateway


class SwitchBotGateway(ISwitchBotGateway):
    def send_toggle_switch(self, device_id):
        pass


class FakeSwitchBotGateway(ISwitchBotGateway):
    def send_toggle_switch(self, device_id):
        pass
