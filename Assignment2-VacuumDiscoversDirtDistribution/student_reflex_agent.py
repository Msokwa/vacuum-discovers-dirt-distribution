#
# Student Agent Class
#
#  This should be the ONLY file you need to edit for this project
#  The function you need to change is run_AI()
#  Every tick of the house simulation, it calls run_AI() on your robot
#  You *can* add more methods, but they must be called from run_AI()
#  NO Threading is needed/allowed - no point here
#  You *can* add class member variables where is says in the __init__ constructor
#
#  The precept you are passed is an object (see base_reflex_agent.py)
#  It is a simple storage object with the current room's status:
#   name, number, is dirty
#  Access the precept's values with:
#   percept.get_room_name()
#   percept.get_room_number()
#   percent.get_is_dirty()
#   percent.get_room_quanity()
#
#  Check out the command line options for pausing/watching output in addition to debugging tools
#

from base_reflex_agent import ReflexVacuum, VacuumOperation, VacuumPercept
from house_environment import DirtDistribution


class StudentReflexVacuum(ReflexVacuum):
    """
    Student Vacuum AI agent implementation goes here.
    """

    def __init__(self, name="StuVac"):
        super().__init__(name=name)  # DO NOT REMOVE THIS

        # Your vacuum's default guess at the dirt distribution is UNKNOWN
        self.dirty_distribution_guess = DirtDistribution.UNKNOWN
        # self.dirty_distribution_guess = DirtDistribution.random_real()  # Pick a random distribution for our guess

        # students can safely add state here
        self.room_data = {}
        self.target_tick_per_room = 95
        self.started_survey = False
        self.survey_complete = False
       
        # self.my_memory = {}

    def run_AI(self, percept: VacuumPercept) -> VacuumOperation:
        room = percept.get_room_number()
        total_rooms = percept.get_room_quantity()
       

        if not self.started_survey:
            if room != 0:
                return VacuumOperation.MOVE_LEFT
            self.started_survey = True

        if room not in self.room_data:
            self.room_data[room] = {
                "observations": 0,
                "dirty": 0
            }

        data = self.room_data[room]
        if data["observations"] < self.target_tick_per_room:
            if percept.get_is_dirty():
                data["dirty"] += 1
                data["observations"] += 1
                return VacuumOperation.SUCK

            data["observations"] += 1
            return VacuumOperation.NOOP

        if room < total_rooms - 1:
            return VacuumOperation.MOVE_RIGHT

        self.survey_complete = True
        self.get_dirty_distribution_guess()

        return VacuumOperation.NOOP

    def get_dirty_distribution_guess(self) -> DirtDistribution:
        rates = []
        for room in sorted(self.room_data):
            data = self.room_data[room]
            if data["observations"]:
                rates.append(data["dirty"] / data["observations"])

        if len(rates) < 3:
            self.dirty_distribution_guess = DirtDistribution.UNKNOWN
            return self.dirty_distribution_guess

        average = sum(rates) / len(rates)
        mean_x = (len(rates) - 1) / 2
        numerator = sum(
            (index - mean_x) * (rate - average)
            for index, rate in enumerate(rates)
        )
        denominator = sum(
            (index - mean_x) ** 2 for index in range(len(rates))
        )
        slope = numerator / denominator if denominator else 0.0
        variance = sum((rate - average) ** 2 for rate in rates) / len(rates)
        standard_deviation = variance ** 0.5

        if slope < -0.018:
            guess = DirtDistribution.SKEWED
        elif standard_deviation < 0.040 and abs(average - 0.15) < 0.06:
            guess = DirtDistribution.UNIFORM
        else:
            guess = DirtDistribution.RANDOM

        self.dirty_distribution_guess = guess
        return self.dirty_distribution_guess
    
