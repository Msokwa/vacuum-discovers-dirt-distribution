# Simple reflex agent in the vacuum world
#
# Artificial Intelligence Class
# The University of Europe for Applied Sciences
# 2026
#
# Based on the Russell and Norvig AI: A Modern Approach agent model
#
# Builds a simple multi-room environment and allows a student to implements a reflex agent
#

import logging
import time
import argparse

# from pprint import pformat
# from collections import defaultdict

from DirtDistribution import DirtDistribution
from house_environment import HouseEnvironment
from base_reflex_agent import ReflexVacuum
from student_reflex_agent import StudentReflexVacuum
from simulation_run_results import SimulationRunResults

# ** ************************************************************************************
ASSIGNMENT_PRESETS = {
    "1.1": {
        "room_quantity": 2,
        "dirty_mode": "uniform",
    },
    "1.2": {
        "room_quantity": 5,
        "dirty_mode": "uniform",
    },
    "2.1": {
        "room_quantity": 7,
        "unknown_dirty_mode": True,
        "num_runs": 60,
        "guess_dirty_mode": True,
        "gen_stats": False,
        "random_starting_room": True,
    },
}

# ** ************************************************************************
BASE_DEFAULTS = {
    "max_ticks": 700,
    "room_quantity": 2,
    "vacuum_name": "Roomber",
    "num_runs": 1,
    "dirty_mode": DirtDistribution.UNIFORM.value,
    "gen_stats": True,
    "random_starting_room": False,
    "guess_dirty_mode": False,
}


# ** ************************************************************************
def print_config(args):
    print("\n=== Simulation Configuration ===\n")

    config = {
        "Assignment Preset": getattr(args, "assignment_settings", None),
        "Room Quantity": args.room_quantity,
        "Dirt Distribution": str(args.dirty_mode),
        "Randomly Selected Dirt mode": str(args.unknown_dirty_mode),
        "Random Starting Room": args.random_starting_room,
        "Guess Dirty Mode": args.guess_dirty_mode,
        "Number of Runs": args.num_runs,
        "Generate Stats": args.gen_stats,
        "Max Ticks": args.max_ticks,
        "Pause Each Tick": args.pause,
        "Slow Ticks": args.slow_ticks,
        "Animate": args.animate,
        "Vacuum Name": args.vacuum_name,
        "Log Level": logging.getLevelName(args.log_level),
    }

    for key, value in config.items():
        print(f"{key:30}: {value}")

    print("\n================================\n")


# ** ************************************************************************
def parse_args():

    # Handling assignment presets to make launching easier for students
    preset_keys = sorted(ASSIGNMENT_PRESETS.keys())
    pretty_list = ", ".join(preset_keys)

    # --- First pass: only grab preset ---
    base_parser = argparse.ArgumentParser(add_help=False)
    base_parser.add_argument(
        "--assignment-settings",
        type=str,
        default="",
        choices=preset_keys,
        metavar="{" + pretty_list + "}",
        help=f"Set parameters for a specific assignment. Options: {pretty_list}",
    )

    base_args, remaining_argv = base_parser.parse_known_args()

    # --- Load preset defaults ---
    defaults = BASE_DEFAULTS.copy()
    if base_args.assignment_settings:
        preset = ASSIGNMENT_PRESETS.get(base_args.assignment_settings)
        if not preset:
            raise ValueError(
                f"Unknown assignment preset: {base_args.assignment_settings}"
            )
        defaults.update(preset)

    # --- Full parser ---
    parser = argparse.ArgumentParser(
        parents=[base_parser],
        description="Vacuum World Simulation",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.set_defaults(**defaults)

    parser.add_argument(
        "--max-ticks",
        type=int,
        help="Maximum number of simulation steps (ticks) to run per simulation. (default: 10)",
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable INFO-level logging (shows agent decisions and environment updates).",
    )
    group.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Enable DEBUG-level logging (detailed internal state and diagnostics).",
    )

    parser.add_argument(
        "-p",
        "--pause",
        action="store_true",
        help="Pause after each simulation tick and wait for Enter to continue.",
    )
    parser.add_argument(
        "-s",
        "--slow-ticks",
        action="store_true",
        help="Slow down simulation tick and wait to 1 sec each so it's easy to watch.",
    )
    parser.add_argument(
        "-a",
        "--animate",
        action="store_true",
        help="Animate the world state on each tick for pretty output.",
    )

    parser.add_argument(
        "--room-quantity",
        type=int,
        help="Set how many rooms wide the house is. (default: 2)",
    )

    parser.add_argument(
        "--vacuum-name",
        type=str,
        help="Set your robot vacuum's name (default: 'Roomber')",
    )

    parser.add_argument(
        "--random-starting-room",
        action="store_true",
        help="Start the vacuum in a random room instead of leftmost room",
    )

    parser.add_argument(
        "--guess-dirty-mode",
        action="store_true",
        help="Turn on a check at the end where the vacuum is asked what the house's dirt mode distribution is.",
    )

    parser.add_argument(
        "--num-runs",
        type=int,
        help="Number of times to run the simulation - used primarily in assignment #2 (default 1)",
    )

    parser.add_argument(
        "--print-config",
        action="store_true",
        help="Print the final resolved configuration and exit.",
    )

    # --- Stats toggle ---
    gen_stats_group = parser.add_mutually_exclusive_group()
    gen_stats_group.add_argument(
        "--no-gen-stats",
        dest="gen_stats",
        action="store_false",
        help="Do not generate run stats for each run",
    )
    gen_stats_group.add_argument(
        "--gen-stats",
        dest="gen_stats",
        action="store_true",
        help="Generate run stats for each run",
    )

    # --- Dirt mode selection ---
    dirty_group = parser.add_mutually_exclusive_group()
    dirty_group.add_argument(
        "--unknown-dirty-mode",
        action="store_true",
        help="Choose randomly which dirty mode the house has. Use to test for the vacuum learning the dirty mode",
    )
    dirty_group.add_argument(
        "--dirty-mode",
        type=str,
        choices=[d.value for d in DirtDistribution.real_values()],
        help="Controls how room dirt probabilities are generated by different profile.",
    )

    # --- Final parse ---
    args = parser.parse_args(remaining_argv)

    # --- Logging level ---
    if args.debug:
        args.log_level = logging.DEBUG
    elif args.verbose:
        args.log_level = logging.INFO
    else:
        args.log_level = logging.WARNING

    # --- Convert dirty mode ---
    if args.unknown_dirty_mode:
        args.dirty_mode = DirtDistribution.random_real()

    else:
        args.dirty_mode = DirtDistribution.from_string(args.dirty_mode)

    # --- Optional: print preset info ---
    if base_args.assignment_settings:
        print(f"Using assignment preset: {base_args.assignment_settings}")

    # ** Special exit: show the options as set and then quit immediately
    if args.print_config:
        print_config(args)
        exit(0)

    return args


# ** *************************************************************************
def run_simulation(args, house: HouseEnvironment, vacuum: ReflexVacuum) -> None:
    logging.info("Beginning simulation")

    # Main simulation loop — one iteration per tick
    for curr_tick_num in range(args.max_ticks):
        logging.debug(f"Starting tick #{curr_tick_num}")
        # What does the vacuum see?
        precept = house.get_vacuum_precept()
        logging.debug(f"Vacuum preceives: {precept}")

        # Let the vacuum "think" and return an operation choice
        vacuum_operation = vacuum.tick(percept=precept)

        logging.info(f"{vacuum.get_name()} decides: {vacuum_operation}")

        # Try to apply the vacuum's chosen operation to the world
        house.do_vacuum_operation(vacuum_operation)

        # Have the house update its state (can add dirt)
        house.tick()

        # Print pretty version!
        if args.animate:
            print(house.get_visual_state_str())

        # Delay to slow things down while watching things work
        if args.slow_ticks:
            time.sleep(1.0)

        if args.pause:
            input("Press Enter to continue next tick")

    logging.info("Simulation complete.")


# ** ********************************************************************************************
def build_confusion_matrix_and_metrics(simulation_run_results: list):

    labels = DirtDistribution.all_values()  # strings only!

    cm = {
        true_label: {pred_label: 0 for pred_label in labels}
        for true_label in labels
    }

    total = 0
    correct = 0

    for result in simulation_run_results:
        run_id, true_label, predicted_label, is_correct = result.get_dirty_distribution_guess_results()

        # ---- FORCE STRING CONSISTENCY ----
        if isinstance(true_label, DirtDistribution):
            true_label = true_label.value
        if isinstance(predicted_label, DirtDistribution):
            predicted_label = predicted_label.value

        cm[true_label][predicted_label] += 1

        total += 1
        if true_label == predicted_label:
            correct += 1

    accuracy = correct / total if total else 0.0

    metrics = {}

    for label in labels:
        tp = cm[label][label]

        fp = sum(cm[r][label] for r in labels) - tp
        fn = sum(cm[label][c] for c in labels) - tp

        support = sum(cm[label][c] for c in labels)

        precision = tp / (tp + fp) if (tp + fp) else 0.0
        recall = tp / (tp + fn) if (tp + fn) else 0.0
        f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0

        metrics[label] = {
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "support": support,
        }

    return cm, metrics, accuracy

# ** ********************************************************************************************
#  Outputs the confusion matrix and total stats for your vacuum's guess on the dirt distribution
def generate_dirt_distribution_results(simulation_run_results: list) -> None:
    logging.info(
        "Generating and printing dirt distribution results guesses by the vacuum"
    )
    cm, metrics, accuracy = build_confusion_matrix_and_metrics(simulation_run_results)

    labels = DirtDistribution.all_values()

    def fmt(label):
        return str(label)

    # ----------------------------
    # CONFUSION MATRIX
    # ----------------------------
    print("\nCONFUSION MATRIX (Actual ↓ vs Predicted →)\n")

    header = " " * 14 + "".join(f"{fmt(l):>10}" for l in labels)
    print(header)

    for true_label in labels:
        row = f"{fmt(true_label):>14}"
        for pred_label in labels:
            row += f"{cm[true_label][pred_label]:>10}"
        print(row)

    # ----------------------------
    # PER-CLASS METRICS
    # ----------------------------
    print("\nPER-CLASS METRICS\n")

    print(
        f"{'Class':>14}"
        f"{'Support':>10}"
        f"{'Precision':>12}"
        f"{'Recall':>10}"
        f"{'F1':>10}"
    )

    total_support = 0
    total_correct = 0

    macro_p = 0.0
    macro_r = 0.0
    macro_f1 = 0.0
    class_count = len(labels)

    for label in labels:
        tp = cm[label][label]

        support = sum(cm[label][c] for c in labels)
        fp = sum(cm[r][label] for r in labels) - tp
        fn = sum(cm[label][c] for c in labels) - tp

        precision = tp / (tp + fp) if (tp + fp) else 0.0
        recall = tp / (tp + fn) if (tp + fn) else 0.0
        f1 = (
            (2 * precision * recall) / (precision + recall)
            if (precision + recall)
            else 0.0
        )

        print(
            f"{fmt(label):>14}"
            f"{support:>10}"
            f"{precision:>12.2f}"
            f"{recall:>10.2f}"
            f"{f1:>10.2f}"
        )

        total_support += support
        total_correct += tp

        macro_p += precision
        macro_r += recall
        macro_f1 += f1

    macro_p /= class_count
    macro_r /= class_count
    macro_f1 /= class_count

    # ----------------------------
    # OVERALL SUMMARY
    # ----------------------------
    failed = total_support - total_correct
    accuracy = (total_correct / total_support * 100) if total_support else 0.0

    print("\nOVERALL\n")
    print(f"Total Runs : {total_support}")
    print(f"Correct    : {total_correct}")
    print(f"Failed     : {failed}")
    print(f"Accuracy   : {accuracy:.2f}%")

    print("\nMACRO AVERAGES\n")
    print(f"Precision  : {macro_p:.2f}")
    print(f"Recall     : {macro_r:.2f}")
    print(f"F1 Score   : {macro_f1:.2f}\n")


# ** *************************************************************************************
# ** Main operations begin here
# ** *************************************************************************************
if __name__ == "__main__":
    # log_level = logging.INFO   # Default to debug level

    args = parse_args()

    # Configure the format and level of our logging output system
    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(name)s: %(message)s", level=args.log_level
    )

    logging.info(f"Here is the full set of options set in the args var: ")
    if args.verbose:
        print_config(args)

    simulation_run_results = []

    for curr_rum_num in range(args.num_runs):
        logging.info(f"*" * 80)
        logging.info(f"Run #{curr_rum_num} begins")
        logging.info("Starting House Environment World and Agent")

        # Handle having the user want a random DirtyDistribution (overrides a selected one)
        if args.unknown_dirty_mode:
            args.dirty_mode = DirtDistribution.random_real()

        # Instantiate the student's agent and the house environment
        vacuum = StudentReflexVacuum(name=args.vacuum_name)
        house = HouseEnvironment(
            vacuum,
            room_quantity=args.room_quantity,
            dirty_mode=args.dirty_mode,
            is_random_starting_room=args.random_starting_room,
        )

        # Main execution of the home simulation is entirely in this function
        run_simulation(args, house, vacuum)

        # Save the simulation results in a results storage object (also gens stats)
        curr_simulation_run_results = SimulationRunResults(house, vacuum, curr_rum_num)
        simulation_run_results.append(curr_simulation_run_results)

        # Main loop complete - time for the results of your AI's work
        if args.gen_stats:
            curr_simulation_run_results.do_gen_stats()
        else:
            logging.debug("Stats generation suppressed - no stats gen")

        if args.guess_dirty_mode:
            logging.debug(
                f"Vacuum guesses the dirt distribution on #{curr_rum_num} is: {vacuum.get_dirty_distribution_guess()}"
            )

        logging.info(f"Run #{curr_rum_num} done")

    if args.guess_dirty_mode:
        generate_dirt_distribution_results(simulation_run_results)

    logging.info("All Runs Complete.")
