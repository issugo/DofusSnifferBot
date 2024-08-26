from HexReader import HexReader
from ankama.types.game.house.HouseInformation import HouseInformation


class MapComplementaryInformationsDataMessage:
    # protocolId is the network packet id of the message
    protocolId = 9792

    # ALL DATA FROM PACKET
    # unsigned int
    subAreaId = 0

    # int
    mapId = 0

    # Vector. < HouseInformations >
    houses = []

    # Vector. < GameRolePlayActorInformations >
    actors = []

    # Vector. < InteractiveElement >
    interactiveElements = []

    # Vector. < StatedElement >
    statedElements = []

    # Vector. < MapObstacle >
    obstacles = []

    # Vector. < FightCommonInformations >
    fights = []

    # boolean
    hasAggressiveMonsters = False

    # FightStartingPositions
    fightStartPositions = {}

    # FuncTree
    _housestree = {}

    # FuncTree
    _actorstree = {}

    # FuncTree
    _interactiveElementstree = {}

    # FuncTree
    _statedElementstree = {}

    # FuncTree
    _obstaclestree = {}

    # FuncTree
    _fightstree = {}

    # FuncTree
    _fightStartPositionstree = {}

    def __init__(self, dataInput):
        """
        dataInput should be binary data
        the init should construct the data in the same way as the dofus original code
        """
        reader = HexReader(dataInput)
        # lis les maisons dans le message
        _housesLen = reader.read_unsigned_short_big_endian()
        for i in range(0, _housesLen):
            _tempId = reader.read_unsigned_short_big_endian()
            _house = HouseInformation(dataInput, readerCursor=reader.cursor)
            self.houses.append(_house)
        # lis les acteurs dans le message
        _actorsLen = reader.read_unsigned_short_big_endian()
        for i in range(0, _actorsLen):
            _tempId = reader.read_unsigned_short_big_endian()
            # TODO: DESERIALIZE LES ACTEURS
            _actor = ''
            self.actors.append(_actor)
        # lis les interactivesElement dans le message
        _ieLen = reader.read_unsigned_short_big_endian()
        for i in range(0, _ieLen):
            _tempId = reader.read_unsigned_short_big_endian()
            # TODO: DESERIALIZE LES INTERACTIVE ELEMENTS
            _ie = ''
            self.interactiveElements.append(_ie)
        # lis les statedElement dans le message
        _seLen = reader.read_unsigned_short_big_endian()
        for i in range(0, _seLen):
            _tempId = reader.read_unsigned_short_big_endian()
            # TODO: DESERIALIZE LES STATED ELEMENTS
            _se = ''
            self.statedElements.append(_se)
        # lis les mapObstacle dans le message
        _mapObstacleLen = reader.read_unsigned_short_big_endian()
        for i in range(0, _mapObstacleLen):
            _tempId = reader.read_unsigned_short_big_endian()
            # TODO: DESERIALIZE LES MAP OBSTACLE
            _mapObstacle = ''
            self.obstacles.append(_mapObstacle)
        # lis les fights dans le message
        _fightsLen = reader.read_unsigned_short_big_endian()
        for i in range(0, _fightsLen):
            _tempId = reader.read_unsigned_short_big_endian()
            # TODO: DESERIALIZE LES FIGHTS COMMON
            _fights = ''
            self.fights.append(_fights)
        self.hasAggressiveMonsters = reader.read_boolean()
        # TODO DESERIALIZE FIGHT STARTING POSITIONS
        self.fightStartPositions = ''

    @staticmethod
    def deserializeAsMapComplementaryInformationsDataMessage(dataInput):
        """
    dataInput should be bynary data
    """
        return MapComplementaryInformationsDataMessage(dataInput)
