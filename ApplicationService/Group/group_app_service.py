from Domain.Group.group_repository import IGroupRepository
from Domain.api_gateway import ISwitchBotGateway
from utility.exception import DeviceNotFound
from typing import List, Tuple
from ApplicationService.Group.dto_group import Group as DGroup
from Domain.Group.group import Group


class GroupAppService:
    def __init__(self, db: IGroupRepository, api_gateway: ISwitchBotGateway):
        self.db = db
        self.api_gateway = api_gateway

    def create_group(self, device_id_list: List[str], name: str):
        try:
            self.db.add(device_id_list, name)
        except DeviceNotFound as e:
            raise e

    def get_all(self) -> Tuple[DGroup]:
        groups: Tuple[Group] = self.db.get_all()
        return tuple(DGroup(g.id, g.name) for g in groups)
