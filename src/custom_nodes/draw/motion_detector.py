"""
Node template for creating custom nodes.
"""

from typing import Any, Dict
from imutils.video import VideoStream
import datetime
import imutils
import time
import cv2
import numpy as np


from peekingduck.pipeline.nodes.abstract_node import AbstractNode
from peekingduck.pipeline.nodes.draw.utils.bbox import draw_bboxes
from peekingduck.pipeline.nodes.draw.utils.general import (
    get_image_size,
    project_points_onto_original_image
    )


class Node(AbstractNode):
    """This is a template class of how to write a node for PeekingDuck.

    Args:
        config (:obj:`Dict[str, Any]` | :obj:`None`): Node configuration.
    """

    def __init__(self, config: Dict[str, Any] = None, **kwargs: Any) -> None:
        super().__init__(config, node_path=__name__, **kwargs)

        # initialize/load any configs and models here
        # configs can be called by self.<config_name> e.g. self.filepath
        # self.logger.info(f"model loaded with configs: config")
        self.tracking = {}

    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:  # type: ignore
        """This node does ___.

        Args:
            inputs (dict): Dictionary with keys "__", "__".

        Returns:
            outputs (dict): Dictionary with keys "__".
        """


        bboxes = inputs["bboxes"]
        ids = inputs["obj_attrs"]["ids"]
        img = inputs["img"]
        img_size = get_image_size(img)

        for i, bbox in enumerate(bboxes):
            # breakpoint()
            if ids[i] not in self.tracking:
                self.tracking[ids[i]] = []
            
            top_left,  bottom_right = project_points_onto_original_image(bbox, img_size)
            print(ids[i], top_left, bottom_right)
            coord = (top_left, bottom_right)
            try:
                if all(np.array(coord) not in np.array(self.tracking[ids[i]])):
                    self.tracking[ids[i]].append(coord)
                    img = cv2.rectangle(img, (int(top_left[0]), int(top_left[1])), (int(bottom_right[0]), int(bottom_right[1])), (0, 255, 0), 3)
            except TypeError:
                if np.array(coord) not in np.array(self.tracking[ids[i]]):
                    self.tracking[ids[i]].append(coord)
                    img = cv2.rectangle(img, (int(top_left[0]), int(top_left[1])), (int(bottom_right[0]), int(bottom_right[1])), (0, 255, 0), 3)


        return {}
