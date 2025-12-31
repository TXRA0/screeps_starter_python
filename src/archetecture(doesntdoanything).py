"""

# Screeps Bot Architecture Notes

This file explains how my Screeps bot is structured, what each folder is responsible for,
and how to expand or modify behavior without breaking everything.

The main goal of this layout is:
- Keep `main.py` extremely readable
- Separate *what creeps do* from *when creeps are spawned*
- Make it easy to add new roles, new spawning logic, or new systems later


## High-Level Idea

There are three big layers to the bot:

1. **Roles** → what a creep does every tick
2. **Managers** → when and how creeps get spawned
3. **Core / Orchestration** → memory, cache, cleanup, and the main loop

Nothing should try to do more than one of these jobs.


--------------------------------------------------
FOLDER BREAKDOWN
--------------------------------------------------


## `main.py`

This is the entry point. It should stay boring.

It:
- Sets up memory and memhack
- Sets up cache
- Catalogues rooms
- Runs creep logic
- Runs spawning logic
- Uses leftover CPU for pixels

If `main.py` ever gets big, something is wrong and logic should be moved out.


--------------------------------------------------


## `core/`

This folder contains low-level engine stuff that almost never changes.

### `memory.py`
Handles:
- Memhack setup
- Global reset tracking
- Making sure Memory objects exist

Nothing in here should depend on roles or spawning.

### `cache.py`
Handles:
- Cache object (lost on global reset)
- Fast-access per-tick data

Cache is for things that are OK to forget sometimes.

### `cleanup.py`
Handles:
- Deleting memory for dead creeps, rooms, and spawns

This keeps Memory clean and prevents bloat.


--------------------------------------------------


## `rooms/`

Room-level logic that applies to owned rooms as a whole.

### `owned_rooms.py`
Handles:
- Detecting which rooms I own
- Initializing per-room cache values
- Tracking work parts and carry parts per room

If I ever add room strategies (like remote mining or defense),
this folder is where that logic should live.


--------------------------------------------------


## `creeps/`

This folder is just a dispatcher.

### `runner.py`
It:
- Loops over all creeps
- Skips spawning creeps
- Calls the correct role logic based on `creep.memory.role`

It should NOT contain actual creep behavior.
All behavior belongs in `roles/`.


--------------------------------------------------


## `roles/`

This folder contains **all creep behavior**.

Each file = one role.

Examples:
- `miner.py`
- `hauler.py`
- `worker.py`

Each role file should:
- Export ONE main function (e.g. `run_miner(creep)`)
- Only care about what that creep does
- Not care about how or why it was spawned

If I want to change how a creep behaves, I only touch this folder.


### Adding a New Role

To add a new role (example: `claimer`):

1. Create `roles/claimer.py`
2. Implement `run_claimer(creep)`
3. Add a new `elif` in `creeps/runner.py`
4. Make sure a manager spawns creeps with `memory.role = 'claimer'`

That’s it. No other files should need changes.


--------------------------------------------------


## `managers/`

Managers decide **when to spawn creeps and how many**.

Each manager:
- Represents ONE role
- Uses existing room state + cache to decide if spawning is needed
- Builds the creep body
- Calls `spawn.spawnCreep(...)`

Managers do NOT:
- Control creep behavior
- Loop over all spawns
- Handle global timing

That’s the spawner’s job.


### Why Managers Exist

Without managers:
- All spawn logic gets jammed into one huge file
- Changing one role risks breaking others

With managers:
- Each role’s spawning logic is isolated
- It’s easy to rebalance one role
- New roles don’t cause chaos


--------------------------------------------------


## `spawning/`

This folder coordinates spawning.

### `spawner.py`
This is the “spawn brain”.

It:
- Runs every 3 ticks
- Counts current work/carry parts
- Loops rooms and spawns
- Calls managers in priority order

Managers return:
- `True` → something spawned, stop and move on
- `False` → nothing spawned, try next manager

The order managers are called defines spawn priority.


### `naming.py`
Handles:
- Unique creep name generation
- Timecode logic

Keeping this separate avoids clutter.


### `counters.py`
Handles:
- Counting active work parts
- Counting active carry parts

This keeps spawning math clean and centralized.


--------------------------------------------------


## `utils/`

Small helper functions that don’t belong anywhere else.

### `body.py`
Contains:
- `body_shorthand`
- Pixel generation logic

If something is generic and reused, it probably belongs here.


--------------------------------------------------
HOW TO EXPAND THE BOT
--------------------------------------------------


## Adding a New Role (Quick Checklist)

Example: adding a `remote_miner`

1. `roles/remote_miner.py`
   - Write creep behavior

2. `managers/remote_miner_manager.py`
   - Write spawning logic

3. Update `creeps/runner.py`
   - Add role dispatch

4. Update `spawning/spawner.py`
   - Call the new manager in the right priority order


## Changing Spawn Balance

Only touch:
- The relevant manager file

Do NOT touch:
- `main.py`
- `runner.py`
- Other managers


## Adding Room-Level Strategy

Put logic in:
- `rooms/`

Examples:
- Remote room tracking
- Defense state
- Expansion planning


--------------------------------------------------
FUTURE IMPROVEMENTS IDEAS
--------------------------------------------------

Some ideas I might add later:

- Per-room config objects
- Priority-based manager system instead of fixed order
- State machines for roles (harvest/build/upgrade states)
- CPU profiling per system
- Combat and defense roles
- Remote mining managers
- Power creep support

The current structure is designed so all of this can be added
without rewriting existing code.


--------------------------------------------------
FINAL NOTE
--------------------------------------------------

If something feels hard to change, that’s a sign it’s in the wrong folder.

Roles = behavior  
Managers = spawning decisions  
Spawner = coordination  
Main = boring glue  

Keep it boring, keep it readable.
"""