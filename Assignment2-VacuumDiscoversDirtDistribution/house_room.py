import logging
import random

from base_reflex_agent import VacuumPercept


# ** *************************************************************************
class HouseRoom:
    """Represents a single room in the vacuum world environment.

    Tracks cleanliness state, dirt probability, and statistics such as how often
    the room was dirty or vacuumed (correctly and unnecessarily).
    """

    def __init__(self, room_name, room_number, is_dirty=True, dirty_odds=0.1):
        self.log = logging.getLogger(self.__class__.__name__)

        self.name = room_name
        self.number = room_number
        self.is_dirty = is_dirty
        self.dirty_odds = dirty_odds

        self.total_ticks = 0
        self.current_ticks_dirty = 0
        self.total_ticks_dirty = 0

        self.times_vacuumed_count = 0
        self.times_properly_vacuumed_count = 0
        self.times_unecessary_vacuumed_count = 0

        self.log.debug(f"Building room {self.name}")

    def get_name(self):
        return self.name

    def get_is_dirty(self):
        return self.is_dirty

    def get_total_ticks_dirty(self):
        return self.total_ticks_dirty

    def get_proper_vacuums_count(self):
        return self.times_properly_vacuumed_count

    def get_unecessary_vacuums_count(self):
        return self.times_unecessary_vacuumed_count

    def get_dirty_odds(self):
        return self.dirty_odds

    def get_ticks_count(self):
        return self.total_ticks

    def vacuum_up(self):
        """Clean the room. If dirty, marks it clean and records a proper vacuum;
        otherwise records it as an unnecessary vacuum operation."""
        self.log.debug("Vacuuming room")
        self.times_vacuumed_count += 1
        if self.is_dirty:
            self.times_properly_vacuumed_count += 1
            self.is_dirty = False
            self.current_ticks_dirty = 0
        else:
            self.times_unecessary_vacuumed_count += 1

    def tick(self):
        """Advance the room by one time step. Updates dirty-tick counters and
        randomly re-dirties the room based on its dirty_odds probability."""
        self.log.debug(f"Room {self.name} tick")
        self.total_ticks += 1
        if self.is_dirty:
            self.current_ticks_dirty += 1
            self.total_ticks_dirty += 1
        if random.random() < self.dirty_odds:
            self.log.debug(f"Room {self.name} got dirty again!")
            self.is_dirty = True

    def __str__(self):
        ret = f"Room {self.name}({self.number}) || is dirty: {self.is_dirty} | Ticks dirty: {self.current_ticks_dirty} | Times vacuumed: {self.times_vacuumed_count} | Odds of dirty: {self.dirty_odds}"
        return ret

    def preceive_room(self, room_quantity) -> VacuumPercept:
        """Return a VacuumPercept describing the room's current state, as seen by the agent."""
        return VacuumPercept(
            room_name=self.name,
            room_number=self.number,
            is_dirty=self.is_dirty,
            room_quantity=room_quantity,
        )

    def generate_statistics(self) -> dict:
        """Return a dict of per-room statistics, including dirty time percentage
        and the ratio of proper to unnecessary vacuum operations."""
        stats = {
            "room_name": self.name,
            "room_number": self.number,
            "is_dirty": self.is_dirty,
            "dirty_odds": self.dirty_odds,
            "total_ticks": self.total_ticks,
            "current_ticks_dirty": self.current_ticks_dirty,
            "total_ticks_dirty": self.total_ticks_dirty,
            "times_vacuumed": self.times_properly_vacuumed_count,
            "times_properly_vacuumed": self.times_properly_vacuumed_count,
            "times_unecessary_vacuumed": self.times_unecessary_vacuumed_count,
        }

        if self.total_ticks == 0:
            stats["Ticks_Dirty_Pct"] = 0.0
        else:
            stats["Ticks_Dirty_Pct"] = round(
                float(self.total_ticks_dirty) / self.total_ticks, 3
            )

        if self.times_unecessary_vacuumed_count == 0:
            stats["Proper_To_Unecessary_Ratio"] = float("inf")
        else:
            stats["Proper_To_Unecessary_Ratio"] = (
                round(
                    float(self.times_properly_vacuumed_count)
                    / self.times_unecessary_vacuumed_count
                ),
                3,
            )

        return stats

    def get_results_str(self) -> str:
        """Return a formatted one-line summary of this room's simulation results."""
        ret = ""
        dirty_pct = round(100 * (float(self.total_ticks_dirty) / self.total_ticks), 3)

        ret += f"{self.name} | {self.dirty_odds:>10} | {self.total_ticks_dirty:>13} | {dirty_pct:>14}% | {self.times_vacuumed_count:>12}"

        return ret
