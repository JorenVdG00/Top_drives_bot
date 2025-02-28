from utils.coords_utils import CoordsUtils
from .maps import initialize_action_map, initialize_check_map

# Instantiate CoordsUtils
COORDSUTILS = CoordsUtils()

# Instantiate Action Map
ACTION_MAP = initialize_action_map()
CHECK_MAP = initialize_check_map()
