import logging
import random

# ** Project's local classes and types
from DirtDistribution import DirtDistribution
from house_room import HouseRoom
from base_reflex_agent import VacuumOperation, VacuumPercept, ReflexVacuum

# ** Visual output elements for pretty looking stuff
ROBOT_TILE = "🤖"
DIRT_TILE = "🍂"
EMPTY_TILE = "⬛"


# ** *************************************************************************
class HouseEnvironment:
    """The global environment holding rooms and the vacuum.

    Manages the full simulation state: room layout, vacuum position, and the
    application of agent actions to the world each tick.
    """

    def __init__(
        self,
        vacuum: ReflexVacuum,
        room_quantity: int = 2,
        dirty_mode: DirtDistribution = DirtDistribution.UNIFORM,
        is_random_starting_room: bool = False,
    ):

        self.log = logging.getLogger(self.__class__.__name__)
        self.vacuum = vacuum
        self.room_count = room_quantity
        self.dirty_mode = dirty_mode
        self.is_random_starting_room = is_random_starting_room

        self.ticks_count = 0

        # Determine starting location for the vacuum
        self.vacuum_location_index = self.gen_starting_vacuum_room()

        # Build the rooms as a list of HouseRoom objects
        self.rooms = []
        self.rooms = self.gen_rooms()

    def gen_rooms(self):
        rooms = []

        dirty_odds_set = self.dirty_mode.generate_distribution_odds(self.room_count)
        self.log.debug(f"Room odds set {self.dirty_mode} generated: {dirty_odds_set}")

        # Create rooms, naming them sequentially: RoomA, RoomB, RoomC, ...
        for room_number in range(self.room_count):
            room_name = f"Room{chr(ord('A') + room_number)}"
            room_dirty_odds = dirty_odds_set[room_number]
            rooms.append(HouseRoom(room_name, room_number, dirty_odds=room_dirty_odds))
        return rooms

    def gen_starting_vacuum_room(self):
        starting_room = 0
        if self.is_random_starting_room:
            starting_room = random.randrange(0, self.room_count)
            logging.debug(
                f"Starting vacuum in a random starting room of: {starting_room}"
            )
        else:
            logging.debug(f"Starting vacuum in default leftmost room (index = 0)")
        return starting_room

    def tick(self):
        """Advance all rooms by one time step, allowing each to accumulate dirty-ticks
        and potentially become dirty again."""
        self.ticks_count += 1
        for room in self.rooms:
            room.tick()

    def get_vacuum_precept(self) -> VacuumPercept:
        """Return the agent's current percept — what it sees in the room it occupies."""
        return self.rooms[self.vacuum_location_index].preceive_room(
            room_quantity=self.room_count
        )

    def do_vacuum_operation(self, vacuum_operation: VacuumOperation):
        """Apply the agent's chosen action to the environment.

        Supports four operations: NOOP (do nothing), SUCK (clean current room),
        MOVE_LEFT, and MOVE_RIGHT. Movement fails silently at the boundary walls.
        """
        if vacuum_operation == VacuumOperation.NOOP:
            # Vacuum does nothing, so do nothing
            pass
        elif vacuum_operation == VacuumOperation.SUCK:
            self.log.info(
                f"Vacuum cleans in room {self.rooms[self.vacuum_location_index].get_name()}"
            )
            self.rooms[self.vacuum_location_index].vacuum_up()
        elif vacuum_operation == VacuumOperation.MOVE_LEFT:
            if self.vacuum_location_index > 0:
                self.log.info(f"Vacuum moves left succssfully")
                self.vacuum_location_index -= 1
            else:
                self.log.info(f"Vacuum FAILS to move left")
        elif vacuum_operation == VacuumOperation.MOVE_RIGHT:
            if self.vacuum_location_index < self.room_count - 1:
                self.log.info(f"Vacuum moves right succssfully")
                self.vacuum_location_index += 1
            else:
                self.log.info(f"Vacuum FAILS to move right")
        else:
            raise Exception("Unknown VacuumOperation tried in HouseEnvironment")

    def get_visual_state_str(self) -> str:
        """Build a multi-line ASCII/emoji grid showing room labels, vacuum position,
        and dirt status for the current tick."""
        ret = f"Home current state on tick {self.ticks_count}: \n"
        ret += "Rooms | "
        # Build letter row
        for room_number in range(len(self.rooms)):
            out = f"{(chr(ord('A') + room_number)):<2}"
            ret += out + " | "
        ret += "\n"

        # Robot vacuum row
        ret += "Robot | "
        for room_number in range(len(self.rooms)):
            if room_number == self.vacuum_location_index:
                ret += ROBOT_TILE + " | "
            else:
                ret += EMPTY_TILE + " | "
        ret += "\n"

        # Dirty rooms row
        ret += "Dirt  | "
        for room_number in range(len(self.rooms)):
            if self.rooms[room_number].get_is_dirty():
                ret += DIRT_TILE + " | "
            else:
                ret += EMPTY_TILE + " | "
        ret += "\n"

        return ret

    def generate_statistics(self):
        """Aggregate per-room statistics and compute house-wide totals, including
        overall dirty tick counts, vacuum efficiency, and average dirt rate."""
        self.log.debug("Calculating environment statistics")
        stats = {"room_stats": [], "global_counts": {}}

        for room in self.rooms:
            stats["room_stats"].append(room.generate_statistics())

        global_dirty_ticks_count = 0
        global_proper_vacuums_count = 0
        global_unecessary_vaccums_count = 0
        global_dirty_odds = 0.0
        global_total_ticks_count = 0

        for room in self.rooms:
            global_dirty_ticks_count += room.get_total_ticks_dirty()
            global_proper_vacuums_count += room.get_proper_vacuums_count()
            global_unecessary_vaccums_count += room.get_unecessary_vacuums_count()
            global_dirty_odds += room.get_dirty_odds()
            global_total_ticks_count += room.get_ticks_count()

        stats["global_counts"]["global_total_ticks"] = global_total_ticks_count
        stats["global_counts"]["global_dirty_ticks_count"] = global_dirty_ticks_count
        stats["global_counts"][
            "global_proper_vacuums_count"
        ] = global_proper_vacuums_count
        stats["global_counts"][
            "global_unecessary_vaccums_count"
        ] = global_unecessary_vaccums_count
        stats["global_counts"]["global_dirty_odds"] = round(
            global_dirty_odds / len(self.rooms), 3
        )

        return stats

    def gen_results_str(self) -> str:
        """Format a human-readable summary of the full simulation run, including
        house-wide dirty stats and a per-room breakdown table."""
        ret = ""
        stats = self.generate_statistics()
        ret += f"House and Environment Information\n"
        ret += f" Total ticks: {self.ticks_count}\n"
        ret += f"{'-' * 70}\n"
        ret += f"House-wide stats | Ave Dirty Rate: {stats['global_counts']['global_dirty_odds']}\n"
        ret += f"                 | total ticks spent dirty: {stats['global_counts']['global_dirty_ticks_count']}\n"
        total_dirty_pct = round(
            (
                100
                * float(stats["global_counts"]["global_dirty_ticks_count"])
                / stats["global_counts"]["global_total_ticks"]
            ),
            3,
        )
        ret += f"                 | total percent spent dirty: {total_dirty_pct}%\n"
        ret += f"{'-' * 70}\n\n"
        ret += f"Per-room summaries:\n"
        ret += (
            f"Room  | Dirty Rate | # Ticks Dirty | Pct Ticks Dirty | Times Vacuumed \n"
        )
        ret += f"{'-' * 70}\n"

        for room in self.rooms:
            ret += room.get_results_str() + "\n"

        return ret

    def get_dirty_distribution(self) -> DirtDistribution:
        return self.dirty_mode
