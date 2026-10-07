from enum import Enum, auto
import random


# ** *************************************************************************
class DirtDistribution(Enum):
    UNKNOWN = "unknown"
    UNIFORM = "uniform"
    SKEWED = "skewed"
    RANDOM = "random"

    # Returns list of all possible dirt distribution names as strings ie 'uniform' 'skewed' (not types)
    @classmethod
    def all_values(cls):
        labels = [d.value for d in cls]
        return sorted(labels, key=lambda x: (x == "unknown", x))

    # Returns list of all possible dirt distribution names as strings ie 'uniform' 'skewed' (not types)
    # Leaves out the UNKNOWN class since it's not used in real distributions
    @classmethod
    def real_values(cls):
        return [d for d in cls if d != cls.UNKNOWN]

    # Converts a single DirtDistribution to a string representation
    def __str__(self):
        return f"{self.value}"

    # Factory method returns a DirtDistribution based on a string like 'uniform'
    @classmethod
    def from_string(cls, value: str):
        for d in cls:
            if d.value == value:
                return d
        raise ValueError(f"Invalid DirtDistribution: {value}")

    # Factory method that returns a random DirtDistribution (but not UNKNOWN)
    @classmethod
    def random_real(cls):
        return random.choice([d for d in cls if d != cls.UNKNOWN])

    # API to return a list of floats for dirt falling likelihood in the rooms
    def generate_distribution_odds(self, room_count):
        if self == DirtDistribution.UNIFORM:
            return self._generate_uniform(room_count)

        elif self == DirtDistribution.RANDOM:
            return self._generate_random(room_count)

        elif self == DirtDistribution.SKEWED:
            return self._generate_skewed(room_count)

        else:
            raise ValueError("Unknown distribution - cannot have a set of odds")

    def _generate_uniform(self, room_count) -> list:
        uniform_odds = 0.15
        return [uniform_odds] * room_count

    def _generate_random(self, room_count, p_max=0.20, p_min=0.05) -> list:
        return [round(random.uniform(p_min, p_max), 3) for _ in range(room_count)]

    def _generate_skewed(self, room_count, p_max=0.25, p_min=0.05) -> list:
        """Produce a geometrically decreasing sequence of dirt probabilities across rooms,
        from p_max (first room) down to p_min (last room)."""
        if room_count == 1:
            return [p_max]

        odds = []
        for i in range(room_count):
            t = i / (room_count - 1)
            p = p_max * (p_min / p_max) ** t
            p_rounded = round(p, 3)
            odds.append(p_rounded)

        return odds
