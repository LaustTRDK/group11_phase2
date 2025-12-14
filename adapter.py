"""
Adapter between the Phase 1 GUI and the Phase 2 object-oriented simulation.

- Reuse phase1.io_mod for loading and generating data
- Keep this file small, readable, and exam-friendly
- Do NOT reimplement CSV or random generation logic
"""

from __future__ import annotations
from typing import Dict, List, Tuple, Any

# --- reuse Phase 1 helpers ---
from phase1 import io_mod

# --- Phase 2 core ---
from .DeliverySimulation import DeliverySimulation
from .DispatchPolicy import NearestNeighborPolicy
from .driver import Driver
from .request import Request
from .point import Point
from .request_generator import RequestGenerator
from .mutation_rules import MutationRule
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
    Load drivers from a file using Phase 1 logic.

    Parameters
    ----------
    path : str
        Path to the driver CSV file.

    Returns
    -------
    List[Dict[str, Any]]
        List of driver dictionaries (Phase 1 format).

    >>> isinstance(load_drivers, object)
    True
    """
    return io_mod.load_drivers(path)


def load_requests(path: str) -> List[Dict[str, Any]]:
    """
    Load requests from a file using Phase 1 logic.

    >>> isinstance(load_requests, object)
    True
    """
    return io_mod.load_requests(path)


def generate_drivers(n: int, width: int, height: int) -> List[Dict[str, Any]]:
    """
    Generate random drivers using Phase 1 logic.

    >>> isinstance(generate_drivers, object)
    True
    """
    return io_mod.generate_drivers(n, width, height)


def generate_requests(start_t: int,
                      out_list: List[Dict[str, Any]],
                      req_rate: float,
                      width: int,
                      height: int) -> None:
    """
    Generate requests over time using Phase 1 logic.

    >>> isinstance(generate_requests, object)
    True
    """
    io_mod.generate_requests(start_t, out_list, req_rate, width, height)


# --------------------------------------------------
# Adapter: dicts -> objects
# --------------------------------------------------

def init_state(drivers: List[Dict],
               requests: List[Dict],
               timeout: int,
               req_rate: float,
               width: int,
               height: int) -> Dict[str, Any]:
    """
    Initialize the Phase 2 simulation from Phase 1-style dictionaries.

    This function:
    - Converts driver dicts into Driver objects
    - Converts request dicts into Request objects
    - Creates policies and generators
    - Creates and stores a global DeliverySimulation

    Returns
    -------
    Dict[str, Any]
        Initial GUI-compatible snapshot of the simulation.

    >>> isinstance(init_state, object)
    True
    """
    global _SIM

    # 1) Build Driver objects
    driver_objs: List[Driver] = []
    for d in drivers:
        driver_objs.append(
            Driver(
                id=d["id"],
                position=Point(d["x"], d["y"]),
                speed=d.get("speed", 1.0),
                behaviour=GreedyDistanceBehaviour(max_distance=10_000),
            )
        )

    # 2) Build Request objects (scheduled)
    req_objs: List[Request] = []
    for r in requests:
        req_objs.append(
            Request(
                id=r["id"],
                pickup=Point(r["px"], r["py"]),
                dropoff=Point(r["dx"], r["dy"]),
                creation_time=r["t"],
            )
        )

    # 3) Generator + policies (simple defaults)
    generator = RequestGenerator(
        rate=req_rate,
        width=width,
        height=height,
        next_id=len(req_objs) + 1,
        scheduled=req_objs,
    )

    dispatch_policy = NearestNeighborPolicy()
    mutation_rule = MutationRule()

    # 4) Create simulation
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
    Advance the simulation by exactly one time step (tick).

    Returns
    -------
    Tuple[Dict, Dict]
        - Snapshot (GUI format)
        - Metrics dictionary

    Raises
    ------
    RuntimeError
        If the simulation has not been initialized.

    >>> isinstance(simulate_step, object)
    True
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
# Adapter: objects -> dicts (GUI format)
# --------------------------------------------------

def _snapshot() -> Dict[str, Any]:
    """
    Convert the internal DeliverySimulation state into
    a Phase 1 / GUI-compatible dictionary.

    This function hides all Phase 2 objects from the GUI.

    Returns
    -------
    Dict[str, Any]
        Snapshot dictionary in GUI format.

    >>> isinstance(_snapshot, object)
    True
    """
    assert _SIM is not None
    snap = _SIM.get_snapshot()

    return {
        "t": snap["time"],
        "drivers": snap["drivers"],
        "pending": [
            {
                "id": r.id,
                "px": r.pickup.x,
                "py": r.pickup.y,
                "dx": r.dropoff.x,
                "dy": r.dropoff.y,
                "status": r.status.lower(),
                "driver_id": r.assigned_driver_id,
                "t": r.creation_time,
            }
            for r in _SIM.requests
            if r.is_active()
        ],
        "served": snap["served"],
        "expired": snap["expired"],
        "avg_wait": snap["avg_wait"],
    }
