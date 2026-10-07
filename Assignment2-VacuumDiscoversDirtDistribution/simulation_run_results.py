import logging
from pprint import pformat

from house_environment import HouseEnvironment
from base_reflex_agent import ReflexVacuum


class SimulationRunResults:
    def __init__(self, house: HouseEnvironment, vacuum: ReflexVacuum, run_number: int):
        self.house = house
        self.vacuum = vacuum
        self.run_number = run_number

    def generate_statistics(
        self, house: HouseEnvironment, vacuum: ReflexVacuum
    ) -> dict:
        """Collect and return combined statistics from both the house environment
        and the vacuum agent."""
        stats = {}
        stats["house"] = house.generate_statistics()
        stats["vacuum"] = vacuum.generate_statistics()

        return stats

    def show_results(self, house: HouseEnvironment, vacuum: ReflexVacuum) -> None:
        """Print the final simulation results for both the house environment
        and the vacuum agent to stdout."""
        vacuum_results_str = vacuum.gen_results_str()
        house_results_str = house.gen_results_str()

        print("-" * 80)
        print(f"{house_results_str}")
        print()
        print("-" * 80)
        print("-" * 80)
        print(vacuum_results_str)
        print("-" * 80)
        print()

    def do_gen_stats(self) -> None:
        logging.info("Generating stats on your AI agent's successes")
        stats = self.generate_statistics(self.house, self.vacuum)
        raw_stats = pformat(stats)
        logging.debug(f"{raw_stats}")

        self.show_results(self.house, self.vacuum)

    def get_dirty_distribution_guess_results(self) -> tuple:
        house_dirty_distribution = self.house.get_dirty_distribution()
        vacuum_dirty_distribution_guess = self.vacuum.get_dirty_distribution_guess()
        is_correct_guess = (
            self.house.get_dirty_distribution()
            == self.vacuum.get_dirty_distribution_guess()
        )
        return (
            self.run_number,
            house_dirty_distribution,
            vacuum_dirty_distribution_guess,
            is_correct_guess,
        )
