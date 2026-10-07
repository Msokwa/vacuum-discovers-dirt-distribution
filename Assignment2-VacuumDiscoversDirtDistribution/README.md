# Vacuum World AI Simulation

This project is a simplified Vacuum World environment based on:

Russell & Norvig — Artificial Intelligence: A Modern Approach

Students implement a reflex-based agent that operates in a multi-room environment and attempts to clean dirt using only local percepts.

The agent does not perform planning, search, or lookahead.

---

# Goal

Design an agent that:
- Observes the current percept
- Chooses an action based only on that percept
- Cleans the environment efficiently over time

This is a purely reactive (reflex) agent model.

---

# Student Work Area

You only modify:

```
student_reflex_agent.py
```

Implement your logic inside:

```python
def run_AI(self, percept: VacuumPercept) -> VacuumOperation:
```

This method is called once per simulation tick.

After the Assignment 1 phase 1 (1.1), you can also add state as object member variables in your vacuum object.
For example: self.count_moves_left = 0

---

# Percepts (Agent Inputs)

At each tick, the agent receives:

```python
percept.get_room_name()
percept.get_room_number()
percept.get_is_dirty()
percept.get_room_quantity()
```

No other environmental information is available.

State may optionally be stored inside the agent instance.

---

# Actions (Agent Outputs)

The agent must return one of:

```python
VacuumOperation.NOOP
VacuumOperation.SUCK
VacuumOperation.MOVE_LEFT
VacuumOperation.MOVE_RIGHT
```

---

# Running the Simulation

Basic execution:

```bash
python reflex_vacuum_simulation.py
```

---

# Assignment Presets

The simulation supports predefined configurations via:

```
--assignment-settings <preset>
```

Example:

```bash
python reflex_vacuum_simulation.py --assignment-settings 2.1
```

Presets configure environment settings such as:
- room quantity
- dirt distribution behavior
- number of runs
- evaluation settings

### Override behavior

Any CLI argument can override preset values:

```bash
python reflex_vacuum_simulation.py --assignment-settings 2.1 --room-quantity 10
```

CLI flags always take priority over presets.

---

# Command Line Options

## Execution Control

```
-p    Pause after each tick
-s    Slow execution (1 second per tick)
-a    Animate environment output
```

Example:

```bash
python reflex_vacuum_simulation.py -p -a
```

---

## Debugging

```
-v    INFO-level logging
-d    DEBUG-level logging
```

Example:

```bash
python reflex_vacuum_simulation.py -d
```

---

## Environment Configuration

```
--max-ticks N        Maximum simulation steps
--room-quantity N    Number of rooms
--vacuum-name NAME   Name of the agent
--num-runs N         Number of simulation runs
```

Example:

```bash
python reflex_vacuum_simulation.py --room-quantity 5 --max-ticks 50
```

---

## Configuration Output

```
--print-config
```

Prints the resolved configuration (including presets and overrides) and exits.

Example:

```bash
python reflex_vacuum_simulation.py --assignment-settings 2.1 --print-config
```

---

# Testing Guidance

During development, you are encouraged to:
- Modify CLI parameters freely
- Test different room sizes and run counts
- Experiment with agent strategies
- Use `--print-config` to verify configuration

Use:

```
-h
```

to view all available options.

---

# Rules

- Do not modify simulation or framework files
- Only modify student_reflex_agent.py
- No external processes or threading
- Helper methods are allowed inside the agent class
- Internal state may be stored in __init__

---

# Evaluation

At the end of each run, the system reports:
- Total energy usage
- Number of actions taken
- Efficiency of cleaning
- Room-level statistics

The objective is to minimize unnecessary actions while cleaning effectively.

---

# Concept Reference

Based on:

Russell & Norvig — Artificial Intelligence: A Modern Approach

Focus:
- Reflex agents
- Percept-to-action mapping
- No planning or search

---

# Good luck

Start simple. Validate correctness first. Optimize behavior incrementally.
