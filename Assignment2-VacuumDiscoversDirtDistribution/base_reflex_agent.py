from enum import Enum, auto
import logging


from DirtDistribution import DirtDistribution


# ** *************************************************************************
class VacuumOperation(Enum):
    """Complete list of actions the Agent may choose from"""

    NOOP = auto()
    MOVE_RIGHT = auto()
    MOVE_LEFT = auto()
    SUCK = auto()


# ** *************************************************************************
class VacuumPercept:
    """One reading of the environment (a preception/precept) by the vacuum"""

    def __init__(
        self, room_name: str, room_number: int, is_dirty: bool, room_quantity: int
    ):
        self.room_name = room_name
        self.room_number = room_number
        self.is_dirty = is_dirty
        self.room_quantity = room_quantity

    def get_room_name(self):
        return self.room_name

    def get_room_number(self):
        return self.room_number

    def get_is_dirty(self):
        return self.is_dirty

    def get_room_quantity(self):
        return self.room_quantity

    def __str__(self):
        return f"[Room = {self.room_name}, In room number = {self.room_number}, Total rooms = {self.room_quantity}, Dirty = {self.is_dirty}]"


# ** *************************************************************************
class ReflexVacuum:
    """The AI Agent operating in the environment"""

    def __init__(self, name="Roomber"):
        self.log = logging.getLogger(self.__class__.__name__)

        self.name = name
        self.move_count = 0
        self.suck_count = 0
        self.noop_count = 0
        self.tick_count = 0

        self.move_energy_cost = 7
        self.suck_energy_cost = 3
        self.noop_energy_cost = 1

        self.operation_choices = []
        self.log.debug(f"Building vacuum to clean the house name: {self.name}")

        self.dirty_distribution_guess = DirtDistribution.UNKNOWN

    def get_energy_spent(self) -> int:
        energy_spent = 0
        energy_spent += self.move_count * self.move_energy_cost
        energy_spent += self.suck_count * self.suck_energy_cost
        energy_spent += self.noop_count * self.noop_energy_cost
        return energy_spent

    def get_name(self):
        return self.name

    def run_AI(self, percept: VacuumPercept) -> VacuumOperation:
        chosen_operation = VacuumOperation.NOOP
        self.log.warning("This is the DUMB agent - it just sits there")
        return chosen_operation

    def tick(self, percept: VacuumPercept) -> VacuumOperation:
        """Called when time moves a single step forward"""
        self.tick_count += 1  # Track how man ticks we've been called for

        # Core AI Agent code call -> Decide what to do
        ai_decision = self.run_AI(percept)

        # Debugging output if you ask for it
        self.log.debug(f"Vacuum decision: {ai_decision}")

        # Save all operations for future analysis
        self.operation_choices.append(ai_decision)

        # Logging what actions the AI Agent chose to do
        if ai_decision == VacuumOperation.SUCK:
            self.suck_count += 1
        elif ai_decision in [VacuumOperation.MOVE_LEFT, VacuumOperation.MOVE_RIGHT]:
            self.move_count += 1
        elif ai_decision == VacuumOperation.NOOP:
            self.noop_count += 1
        return ai_decision

    def __str__(self):
        ret = f"Vacuum {self.name} stats || moves: {self.move_count} | sucks : {self.suck_count} | noops: {self.noop_count}"
        return ret

    def generate_statistics(self) -> dict:
        stats = {
            "name": self.name,
            "move_count": self.move_count,
            "suck_count": self.suck_count,
            "noop_count": self.noop_count,
            "tick_count": self.tick_count,
            "energy_spent": self.get_energy_spent(),
        }
        return stats

    def gen_results_str(self) -> str:
        stats = self.generate_statistics()
        res = ""

        headers = ["Vacuum", "Energy Spent", "NOOPs", "Moves", "Vacuums"]

        row = [
            stats["name"],
            stats["energy_spent"],
            stats["noop_count"],
            stats["move_count"],
            stats["suck_count"],
        ]

        # Convert everything to strings
        row = [str(x) for x in row]

        # Determine column widths
        col_widths = [max(len(headers[i]), len(row[i])) for i in range(len(headers))]

        # Helper to format a row
        def format_row(items):
            return " | ".join(item.ljust(col_widths[i]) for i, item in enumerate(items))

        # Print table
        line = format_row(headers)
        sep = "-+-".join("-" * w for w in col_widths)
        data = format_row(row)

        res += f"{line}\n{sep}\n{data}"

        return res

    def get_dirty_distribution_guess(self) -> DirtDistribution:
        return self.dirty_distribution_guess
