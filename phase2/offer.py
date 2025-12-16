from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .driver import Driver
    from .request import Request

class Offer:
    def __init__(self, driver, request, estimated_travel_time: float, estimated_reward: float):
        self.driver = driver
        self.request = request
        self.estimated_travel_time = estimated_travel_time
        self.estimated_reward = estimated_reward

