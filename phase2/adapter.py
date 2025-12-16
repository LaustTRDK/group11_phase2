"""
Adapter between the Phase 1 GUI and the Phase 2 object-oriented simulation.

This module translates between:
- Phase 1 style dictionaries (used by the GUI), and
- Phase 2 objects (used by the simulation engine).

The adapter owns a single global DeliverySimulation instance.
"""

from __future__ import annotations
from typing import Dict, List, Tuple, Any

# Reuse Phase 1 helpers
from phase1 import io_mod

# Phase 2 core
from .delivery_simulation import DeliverySimulation
from .dispatch_policies import NearestNeighborPolicy
from .driver import Driver
from .request import Request
from .point import Point
from .request_generator import RequestGenerator
from .mutation_rules import MutationRule, DecisionTreeRule, MutationThresholds
from .driver_behaviour import GreedyDistanceBehaviour


# --------------------------------------------------
# Global simulation instance (managed by adapter)
# --------------------------------------------------

_SIM: DeliverySimulation | None = None


# --------------------------------------------------
# Phase 1 required backend functions
# --------------------------------------------------

def load_drivers(path: str) -> List[Dict[str, Any]]:
    """
    Load drivers from file using Phase 1 logic.

    This function is required by the GUI interface.
    """
    return io_mod.load_drivers(path)


def load_requests(path: str) -> List[Dict[str, Any]]:
    """
    Load requests from file using Phase 1 logic.

    This function is required by the GUI interface.
    """
    return io_mod.load_requests(path)


def generate_drivers(n: int, width: int, height: int) -> List[Dict[str, Any]]:
    """
    Generate random drivers using Phase 1 logic.

    This function is required by the GUI interface.
    """
    return io_mod.generate_drivers(n, width, height)


def generate_requests(
    start_t: int,
    out_list: List[Dict[str, Any]],
    req_rate: float,
    width: int,
    height: int,
) -> None:
    """
    Generate requests over time using Phase 1 logic.

    New requests are appended to the given list.
    """
    io_mod.generate_requests(start_t, out_list, req_rate, width, height)


# --------------------------------------------------
# Adapter: dicts -> objects
# --------------------------------------------------

def init_state(
    drivers: List[Dict],
    requests: List[Dict],
    timeout: int,
    req_rate: float,
    width: int,
    height: int,
) -> Dict[str, Any]:
    """
    Create and initialize a Phase 2 simulation.

    Converts Phase 1-style dictionaries into Phase 2 objects
    and stores the simulation globally.
    """
    global _SIM

    # Build Driver objects
    driver_objs: List[Driver] = []
    for d in drivers:
        driver_objs.append(
            Driver(
                did=d["id"],
                position=Point(d["x"], d["y"]),
                speed=d.get("speed", 1.0),
                status="IDLE",
                current_request=None,
                behaviour=GreedyDistanceBehaviour(max_distance=10_000),
            )
        )

    # Build Request objects
    req_objs: List[Request] = []
    for r in requests:
        req_objs.append(
            Request(
                rid=r["id"],                     # GUI id → rid
                pickup=Point(r["px"], r["py"]),
                dropoff=Point(r["dx"], r["dy"]),
                creation_time=r["t"],
            )
        )

    # Create request generator
    generator = RequestGenerator(
        rate=req_rate,
        width=width,
        height=height,
        next_id=len(req_objs) + 1,
        scheduled=req_objs,
    )

    dispatch_policy = NearestNeighborPolicy()
    mutation_rule = DecisionTreeRule(MutationThresholds())

    _SIM = DeliverySimulation(
        drivers=driver_objs,
        dispatch_policy=dispatch_policy,
        request_generator=generator,
        mutation_rule=mutation_rule,
        timeout=timeout,
    )

    return _snapshot()


# --------------------------------------------------
# Adapter: advance simulation
# --------------------------------------------------

def simulate_step(state: Dict) -> Tuple[Dict, Dict]:
    """
    Advance the simulation by one time step.

    Returns the updated state snapshot and a metrics dictionary.
    """
    if _SIM is None:
        raise RuntimeError("Simulation not initialised")

    _SIM.tick()
    snapshot = _snapshot()

    metrics = {
        "served": snapshot["served"],
        "expired": snapshot["expired"],
        "avg_wait": snapshot["avg_wait"],
    }

    return snapshot, metrics


# --------------------------------------------------
# Adapter: objects -> dicts
# --------------------------------------------------

def _snapshot() -> Dict[str, Any]:
    """
    Convert the internal simulation state into GUI format.

    This hides all Phase 2 objects from the GUI.
    """
    assert _SIM is not None
    snap = _SIM.get_snapshot()

    return {
        "t": snap["time"],
        "drivers": snap["drivers"],
        "pending": [
            {
                "id": r.rid,                    # rid → GUI id
                "px": r.pickup.x,
                "py": r.pickup.y,
                "dx": r.dropoff.x,
                "dy": r.dropoff.y,
                "status": r.status.lower(),
                "driver_id": r.assigned_driver_id,  # did, but GUI kalder det driver_id
                "t": r.creation_time,
            }
            for r in _SIM.requests
            if r.is_active()
        ],
        "served": snap["served"],
        "expired": snap["expired"],
        "avg_wait": snap["avg_wait"],
    }