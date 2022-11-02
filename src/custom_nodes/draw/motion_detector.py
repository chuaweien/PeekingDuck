"""
Identify if Tracking Object(s) is/are moving.
"""

from typing import Any, Dict, Tuple
import cv2
from cv2 import FONT_HERSHEY_SIMPLEX
import numpy as np


from peekingduck.pipeline.nodes.abstract_node import AbstractNode
from peekingduck.pipeline.nodes.draw.utils.constants import (
    VERY_THICK,
    THICK,
    CHAMPAGNE,
    TOMATO,
    VIOLET_BLUE,
)
from peekingduck.pipeline.nodes.draw.utils.general import (
    get_image_size,
    project_points_onto_original_image,
)


class Node(AbstractNode):
    """Identify if the Tracking Object is moving.

    Inputs:
        |img_data|

        |bboxes|

        |obj_attrs_data|

    Outputs:
        None.

    Configs:
        None.
    """

    def __init__(self, config: Dict[str, Any] = None, **kwargs: Any) -> None:
        super().__init__(config, node_path=__name__, **kwargs)

        # Stores previous position of each tracking object
        self.tracking = {}

    def run(self, inputs: Dict[str, Any]) -> None:
        """Compares the previous position of each object to the current position. If the position
            has changed, the bounding box will turn `TOMATO` in color. Otherwise, the bounding box
            stays in `CHAMPAGNE` color.

        Args:
            inputs (dict): Dictionary with keys "img", "bboxes", "obj_attrs".

        Returns:
            outputs      : None
        """

        bboxes = inputs["bboxes"]
        ids = inputs["obj_attrs"]["ids"]
        img = inputs["img"]
        img_size = get_image_size(img)

        for i, bbox in enumerate(bboxes):
            if ids[i] not in self.tracking:
                # if tracking object not found in dictionary,
                # add to dictionary with ((0, 0), (0, 0))
                self.tracking[ids[i]] = (
                    np.zeros((1, 2), dtype=int),
                    np.zeros((1, 2), dtype=int),
                )

            top_left, bottom_right = project_points_onto_original_image(bbox, img_size)

            print(ids[i], top_left, bottom_right)

            coord = (top_left, bottom_right)

            # check if current position is different from previous position = movement
            if (top_left != self.tracking[ids[i]][0]).all() and (
                bottom_right != self.tracking[ids[i]][1]
            ).all():
                self.tracking[ids[i]] = coord
                img = self.draw_bbox(img, coord, TOMATO)
                text = "Motion Detected"
            else:  # no movement
                img = self.draw_bbox(img, coord, CHAMPAGNE)
                text = ""

            cv2.putText(
                img,
                f"Status: {text}",
                (10, img_size[1] - 10),
                FONT_HERSHEY_SIMPLEX,
                0.5,
                VIOLET_BLUE,
                THICK,
            )

        return {}

    def draw_bbox(
        self,
        img: np.array,
        coord: Tuple[np.array, np.array],
        color: Tuple(int, int, int),
    ) -> np.array:
        """Draw bbox on the image

        Args:
            img (np.array): image data
            coord (Tuple[np.array, np.array]): coordinates of the bounding box scaled to image size i.e. top_left, bottom_right
            color (Tuple[int, int, int]): color of the bounding box

        Returns:
            outputs (np.array) : image data
        """
        top_left, bottom_right = coord
        return cv2.rectangle(
            img,
            (int(top_left[0]), int(top_left[1])),
            (int(bottom_right[0]), int(bottom_right[1])),
            color,
            VERY_THICK,
        )
