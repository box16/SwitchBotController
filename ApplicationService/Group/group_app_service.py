from Domain.Group.group_repository import IGroupRepository
from Domain.api_gateway import ISwitchBotGateway


class GroupAppService:
    def __init__(self, db: IGroupRepository, api_gateway: ISwitchBotGateway):
        pass
