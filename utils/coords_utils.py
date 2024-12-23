import os
import cv2
import yaml
import random
from config import COORDS_YML, logger, resize_values
from typing import Tuple, Union, Dict, Any


class CoordsUtils:
    def __init__(self):
        self.logger = logger
        self.coords_data = self.load_coordinates(COORDS_YML)

    # COORDS

    @staticmethod
    def load_coordinates(file_path: str) -> Dict[str, Any]:
        """
        Load coordinates data from a YAML file.

        Args:
            file_path (str): Path to the YAML file containing coordinates data.

        Returns:
            Dict[str, Any]: A dictionary containing the coordinates data loaded from the YAML file.
        """
        with open(file_path, "r") as file:
            data = yaml.safe_load(file)
            return data

    def get_rand_box_coords(self, name: str) -> Union[Tuple[int, int], None]:
        """
        Get random coordinates within a specified bounding box defined in the coordinates data.

        Args:
            name (str): The name of the bounding box entry to retrieve coordinates for.

        Returns:
            Union[Tuple[int, int], None]: A tuple of (x, y) representing random coordinates within the bounding box if found;
            otherwise, None if no matching bounding box is found.
        """
        coords = next(
            (
                item
                for item in self.coords_data["coordinates"]["box_coords"]
                if item["name"] == name
            ),
            None,
        )

        if coords:
            resized_coords = self.resize_ranges(coords["x1"], coords["x2"], coords["y1"], coords["y2"], resize_values)
            # Generate random coordinates within the bounding box
            rand_coords = (
                random.randint(resized_coords[0], resized_coords[1]),
                random.randint(resized_coords[2], resized_coords[3]),
            )
            self.logger.debug(f"Random coordinates: {rand_coords} for box {name}")
            return rand_coords
        else:
            self.logger.error(f"No coordinates found for box {name}")
            return None

    def get_color_coords(
        self, name: str
    ) -> Union[Tuple[Tuple[int, int], Tuple[int, int, int, int]], None]:
        """
        Retrieve the color coordinates and RGBA color value by name.

        Args:
            name (str): The name of the color coordinate entry.

        Returns:
            Union[Tuple[Tuple[int, int], Tuple[int, int, int, int]], None]:
            - A tuple containing two tuples:
                - The first tuple contains the x and y coordinates.
                - The second tuple contains the RGBA color value.
            - None if no entry is found with the specified name.
        """
        coords = next(
            (
                item
                for item in self.coords_data["coordinates"]["color_coords"]
                if item["name"] == name
            ),
            None,
        )
        if coords:
            color_coords = (coords["x"], coords["y"])
            color = (
                coords["color"].get("R", 0),  # Default to 0 if key is missing
                coords["color"].get("G", 0),
                coords["color"].get("B", 0),
                coords["color"].get("A", 255),  # Default to 255 if key is missing
            )
            self.logger.debug(f"Color coordinates: {color_coords} for color {name}")
            return color_coords, color
        else:
            self.logger.error(f"No coordinates found for color {name}")
            return None

    def get_coords(self, name: str) -> Union[Tuple[int, int, int, int], None]:
        """
        Get coordinates defined in the coordinates data.

        Args:
            name (str): The name of the swipe entry to retrieve coordinates for.

        Returns:
            Union[Tuple[int, int, int, int], None]: A tuple of (x1, y1, x2, y2) representing swipe coordinates if found;
            otherwise, None if no matching swipe coords are found.
        """
        coords = next(
            (
                item
                for item in self.coords_data["coordinates"]["box_coords"]
                if item["name"] == name
            ),
            None,
        )

        if coords:
            coords_tup = self.resize_ranges(coords["x1"], coords["x2"], coords["y1"], coords["y2"], resize_values)
            self.logger.debug(f"Swipe coordinates: {coords_tup} for box {name}")
            return coords_tup
        else:
            self.logger.error(f"No coordinates found for swipe {name}")
            return None

    def get_swipe_coords(self, name: str) -> Union[Tuple[int, int, int, int], None]:
        """
        Get coordinates defined in the coordinates data.

        Args:
            name (str): The name of the swipe entry to retrieve coordinates for.

        Returns:
            Union[Tuple[int, int, int, int], None]: A tuple of (x1, y1, x2, y2) representing swipe coordinates if found;
            otherwise, None if no matching swipe coords are found.
        """
        coords = next(
            (
                item
                for item in self.coords_data["coordinates"]["swipe_coords"]
                if item["name"] == name
            ),
            None,
        )

        if coords:
            resized_swipe_coords = self.resize_ranges(coords["x1"], coords["y1"], coords["x2"], coords["y2"], resize_values)
            self.logger.debug(f"Swipe coordinates: {resized_swipe_coords} for box {name}")
            return resized_swipe_coords
        else:
            self.logger.error(f"No coordinates found for swipe {name}")
            return None

    def get_crop_coords(
        self, category: str, sub_cat: str
    ) -> Union[Dict[str, Tuple[int, int, int, int]], Tuple[int, int, int, int], None]:
        """
        Retrieve cropping coordinates from a predefined dataset based on the provided category and optional name.

        Parameters:
        ----------
        category : str
            The category of coordinates to retrieve from the dataset.
        name : str, optional
            The specific name of the coordinates within the given category. If not provided,
            all coordinates in the category are returned as a dictionary.

        Returns:
        -------
        Union[Dict[str, Tuple[int, int, int, int]], Tuple[int, int, int, int], None]
            - If `name` is None: returns a dictionary where keys are names and values are tuples of coordinates.
            - If `name` is provided: returns the tuple of coordinates associated with that name.
            - If `name` does not exist within the category: returns `None`.

        Notes:
        ------
        The structure of `COORDS_DATA` is assumed to contain 'coordinates' -> 'crop_coords' -> 'category' -> 'name'.

        Example:
        --------
        get_crop_coords("club_info", "rq")
        # returns (2000, 365, 2180, 405)

        get_crop_coords("event_img")
        # returns {
        #     "race_type": (0, 0, 330, 80),
        #     "conditions": (5, 60, 320, 145),
        #     "event_number": (0, 150, 65, 215),
        #     "road_type": (75, 150, 330, 215)
        # }
        """
        # coords_dict = next(
        #     (
        #         item
        #         for item in self.coords_data["coordinates"]["crop_coords"]
        #         if item["category"] == category
        #     ),
        #     None,
        # )
        coords_dict = self.get_crop_dict(category)
        if coords_dict is None:
            self.logger.error(f"No dict found for category {category}")
            return None
        else:
            for key, value in coords_dict.items():
                if key == "category":
                    continue
                if isinstance(value, dict):
                    for sub_key, sub_values in value.items():
                        if sub_cat in sub_key:
                            self.logger.debug(
                                f"Sub category {sub_key} found in nested-dict {key}"
                            )
                            return sub_values
                if sub_cat in key:
                    self.logger.debug(f"Sub category {key} found in dict {key}")
                    
                    return value
        self.logger.debug(f"No CropCoords found for category {category}-{sub_cat}")
        return None

    def get_crop_dict(self, category: str):
        # """ -> Union[
        # Dict[Any], None]"""
        # """
        """Retrieve cropping coordinates from a predefined dataset based on the provided category and optional name.

        Parameters:
        ----------
        category : str
            The category of coordinates to retrieve from the dataset.
        name : str, optional
            The specific name of the coordinates within the given category. If not provided,
            all coordinates in the category are returned as a dictionary.

        Returns:
        -------
        Union[Dict[str, Tuple[int, int, int, int]], Tuple[int, int, int, int], None]
            - If `name` is None: returns a dictionary where keys are names and values are tuples of coordinates.
            - If `name` is provided: returns the tuple of coordinates associated with that name.
            - If `name` does not exist within the category: returns `None`.

        Notes:
        ------
        The structure of `COORDS_DATA` is assumed to contain 'coordinates' -> 'crop_coords' -> 'category' -> 'name'.

        Example:
        --------
        get_crop_coords("club_info", "rq")
        # returns (2000, 365, 2180, 405)

        get_crop_coords("event_img")
        # returns {
        #     "race_type": (0, 0, 330, 80),
        #     "conditions": (5, 60, 320, 145),
        #     "event_number": (0, 150, 65, 215),
        #     "road_type": (75, 150, 330, 215)
        # }
        """
        dict = next(
            (
                item
                for item in self.coords_data["coordinates"]["crop_coords"]
                if item["category"] == category
            ),
            None,
        )
        if dict is None:
            self.logger.error(f"No dict found for category {category}")
            return None
        else:
            self.logger.debug(f"CropCoordsDict found for category {category}")
            # dict.pop('category')
            return dict

    def coords_str_to_tuple(self, coords_str: str) -> Tuple[int, int, int, int]:
        """Probably useless.

        Args:
            coords_str (str): _description_

        Returns:
            Tuple[int, int, int, int]: _description_
        """
        coords = coords_str[1:-1].split(",")
        coords = [int(coord) for coord in coords]
        print(f"Coords {coords}")
        print(f"Tuple {tuple(coords)}")
        return tuple(coords)

    @staticmethod
    def resize_coordinate(value: int, factor: float) -> int:
        return int(value * factor)

    def resize_coordinates(
        self, x: int, y: int, factor: Tuple[float, float]
    ) -> Tuple[int, int]:
        return self.resize_coordinate(x, factor[0]), self.resize_coordinate(
            y, factor[1]
        )

    def resize_ranges(
        self, x1: int, x2: int, y1: int, y2: int, factor: Tuple[float, float]
    ) -> Tuple[int, int, int, int]:
        return (
            self.resize_coordinate(x1, factor[0]),
            self.resize_coordinate(x2, factor[0]),
            self.resize_coordinate(y1, factor[1]),
            self.resize_coordinate(y2, factor[1]),
        )

