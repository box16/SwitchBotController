from Domain.Group.group_repository import IGroupRepository
from Domain.api_gateway import ISwitchBotGateway
from typing import List


class GroupAppService:
    def __init__(self, db: IGroupRepository, api_gateway: ISwitchBotGateway):
        self.db = db
        self.api_gateway = api_gateway

    def create_group(self, devices: List[str], name: str):
        self.db.add(devices, name)
