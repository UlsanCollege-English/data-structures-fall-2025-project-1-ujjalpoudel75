# Multi-Queue Round-Robin Café (Interactive CLI)

## Story / Hook

Picture first period at the campus café. There aren’t just one, but several lines—**Mobile**, **WalkIns**, **Faculty**, maybe more. The head barista wants to be **fair**: instead of draining one line before touching the others, they run a **round-robin**—visit Mobile, then WalkIns, then Faculty, then back to Mobile—in the **order the lines were created**. The barista gives each line a fixed **quantum** of attention per visit (e.g., one minute). If a drink finishes within that quantum, great—done. If not, that cup goes back to the **end of the same line** with its **remaining time** written on the sticker until the barista cycles back.

The café has clear policies and a visible status board:

* If **WalkIns** hits its capacity, the newest arrival is politely turned away with: `Sorry, we're at capacity.`
* Managers can issue a **SKIP** to deprioritize a line **one time**, instantly, without advancing the clock.
* Orders are **only** for items on the posted menu; if someone asks for something else, the barista says: `Sorry, we don't serve that.`
* The **wallboard updates after every quantum** to show the time, which line was served, what’s next, and what remains in each line. When all is quiet and the input ends, the barista flips the sign to: `Break time!`

Your program is that café. Each queue is a line of orders; each task is a drink with a burst (minutes needed); the quantum is the barista’s promise of attention per visit; the round-robin is the fairness rule. You’ll type simple commands (`CREATE`, `ENQ`, `RUN`, `SKIP`) **one per line**. The program logs events and, during `RUN`, prints the café display **after each turn**.

---

## Overview

Build an interactive program that simulates a café with multiple order lines (queues) served fairly via **round-robin** with a fixed **quantum** (minutes per turn). You’ll type commands **one per line**. The program processes them immediately. When you hit an **empty line**, the session ends with:

```
Break time!
```

Only `RUN` produces the **café display**, and it does so **after each turn/quantum**.

**Core ideas:** from-scratch queues; preemption & fairness; deterministic I/O; complexity.

---

## How to Run

```bash
python -m cafe_cli
```

Type commands; press **Enter on an empty line** to exit.

---

## Commands (one per line)

* `CREATE <queue_id> <capacity>`
  Create a queue with given capacity (≥ 0). **Creation order** defines round-robin order.

* `ENQ <queue_id> <item_name>`
  Enqueue a new order for `<item_name>`. The **hardcoded menu** maps items → minutes (burst).

  * The system **generates the task id automatically** as `<queue_id>-NNN` (1-based, zero-padded to 3, e.g., `WalkIns-001`).
  * If the queue is full, print the exact message:

    ```
    Sorry, we're at capacity.
    ```

    and emit a `reject` log with `reason=full` (no enqueue).
  * If the item is not on the menu, print:

    ```
    Sorry, we don't serve that.
    ```

    and emit a `reject` log with `reason=unknown_item`.

* `SKIP <queue_id>`
  Mark this queue to be **skipped on its next visit only** (takes **no** time).

* `RUN <quantum> [steps]`
  Execute the scheduler with a quantum (minutes per turn).

  * If `steps` is provided, it must satisfy `1 ≤ steps ≤ (# of queues)`.

    * If outside this range, emit `event=error reason=invalid_steps` and do nothing.
    * Otherwise, perform exactly `steps` **turns** (each turn visits the next queue once).
  * If `steps` is omitted, run until **all queues are empty and no pending skips**.
  * **Display** prints **after each turn** (see “Café display”).

Notes:

* Lines starting with `#` or blank lines are ignored **except** a lone blank line ends the session (prints `Break time!`).
* Invalid commands/args: emit `event=error` (don’t crash).

---

## Round-Robin Rule (Precise)

* Queues rotate in **creation order**: Q₁, Q₂, …, Qk, then back to Q₁.
* A **turn** visits the next queue:

  * If it has a pending **SKIP**, consume it; move on (**no** time advance).
  * If it’s **empty**, move on (**no** time advance).
  * Otherwise, take the **front** task and work for `min(remaining, quantum)` minutes; **advance time** by that amount.

    * If finished, remove it; log `finish`.
    * Else, requeue to the **back** with updated remaining.
* Time only advances when work happens.

---

## Logs (Deterministic)

For each event, print one normalized line:

```
time=<t> event=<EVENT> queue=<qid> [task=<task_id>] [remaining=<r>] [reason=<text>]
```

`event` ∈ `{create, enqueue, reject, run, skip, work, finish, error}`.
Examples:

* Reject (full): `time=7 event=reject queue=WalkIns task=WalkIns-004 reason=full`
* Reject (unknown item): `... reason=unknown_item`
* On each visited queue (even if empty/skip), print `event=run queue=<qid>`.

---

## Café Display (prints **after each RUN turn**)

A compact, line-based snapshot:

```
display time=<t> next=<qid_or_none>
display menu=[americano:2,cappuccino:3,hot_chocolate:4,latte:3,macchiato:2,mocha:4,tea:1]
display <qid> [n/cap][ skip] -> [task:rem,task:rem,...]
display <qid2> [n/cap] -> []
...
```

Rules:

* `menu` items are **sorted by name**, comma-separated; format `name:minutes`.
* For each queue (in **creation order**):

  * `[n/cap]` is current size/capacity.
  * Append ` [ skip]` (note the leading space) only if a skip is pending.
  * `->` shows contents **front→back** as `task_id:remaining` (comma-separated).
* `next` is the queue id the scheduler will visit on the **next** turn (or `none`).
* If there are no queues yet, still print `time`, `next=none`, and `menu`.

---

## Hardcoded Menu (≥ 6 items)

These **must** exist (all lowercase, single tokens):

```
americano=2, latte=3, cappuccino=3, mocha=4, tea=1, macchiato=2, hot_chocolate=4
```

You may add more for your own tests; graders will assume at least the above seven.

---

## Example Session (user input prefixed with `>`)

```
> CREATE Mobile 2
time=0 event=create queue=Mobile

> ENQ Mobile latte
time=0 event=enqueue queue=Mobile task=Mobile-001 remaining=3

> RUN 1 2
time=0 event=run queue=Mobile
time=1 event=work queue=Mobile task=Mobile-001 remaining=2
display time=1 next=Mobile
display menu=[americano:2,cappuccino:3,hot_chocolate:4,latte:3,macchiato:2,mocha:4,tea:1]
display Mobile [1/2] -> [Mobile-001:2]

time=1 event=run queue=Mobile
time=2 event=work queue=Mobile task=Mobile-001 remaining=1
display time=2 next=Mobile
display menu=[americano:2,cappuccino:3,hot_chocolate:4,latte:3,macchiato:2,mocha:4,tea:1]
display Mobile [1/2] -> [Mobile-001:1]

> ENQ Mobile cortado
Sorry, we don't serve that.
time=2 event=reject queue=Mobile task=Mobile-002 reason=unknown_item

> ENQ Mobile latte
time=2 event=enqueue queue=Mobile task=Mobile-002 remaining=3

> ENQ Mobile latte
Sorry, we're at capacity.
time=2 event=reject queue=Mobile task=Mobile-003 reason=full

>
Break time!
```

---

## Constraints

* **Python 3.11+**, standard library only; minimal deps (none required).
* **From-scratch core DS**: implement your own queue (no `collections.deque`/`queue.Queue` for the core).
* Command parsing is case-sensitive; item names must match the menu.
* Deterministic outputs: same inputs → identical logs and display.

---

## Public API (in `/src`)

* `scheduler.py`

  * `class Task(task_id: str, remaining: int)`
  * `class QueueRR`

    * `__init__(self, queue_id: str, capacity: int) -> None`
    * `enqueue(self, task: Task) -> bool`
    * `dequeue(self) -> Task | None`
    * `__len__(self) -> int`
  * `class Scheduler`

    * `create_queue(self, queue_id: str, capacity: int) -> list[str]`
    * `enqueue(self, queue_id: str, item_name: str) -> list[str]`  # auto task_id
    * `mark_skip(self, queue_id: str) -> list[str]`
    * `run(self, quantum: int, steps: int | None) -> list[str]`    # returns logs for all turns
    * `display(self) -> list[str]`                                 # one display block (for current state)
    * `next_queue(self) -> str | None`
    * `menu(self) -> dict[str,int]`
* `parser.py`

  * `parse_command(line: str) -> tuple[str, list[str]] | None`
* `cli.py`

  * Interactive loop: read a line → if empty: print `Break time!` and exit; else dispatch and print **only logs**.
  * For `RUN`, after each turn, print the **display** block.

---

## Complexity Notes (required in `README.md`)

Explain your queue implementation choice (e.g., circular buffer). State and justify:

* `enqueue`, `dequeue`: amortized **O(1)**.
* `run`: **O(#turns + total_minutes_worked)**.
* Space: **O(N)** tasks + metadata.

---

## Testing & Running

* **Run locally:**

  ```bash
  python -m pytest -q
  ```
* Public tests call `Scheduler` directly (no stdin needed).
* Hidden tests include: large sequences, display after each `RUN` turn, steps validation, messages for unknown/full, auto task ids.

---

## Common Pitfalls

* Printing the display after non-`RUN` commands.
* Advancing time on `skip`/empty turns.
* Not enforcing `steps ≤ #queues`.
* Forgetting to zero-pad task ids per queue (`<qid>-001`, `-002`, …).
* Using `deque` for the core queue.

---

## Rubric (100 pts)

* **Correctness (50)**: RR behavior, logs, **display-per-turn**, auto task ids, menu handling, rejects.
* **Complexity notes (15)**: correct, concise, justified.
* **Student tests (15)**: ≥4 targeted, deterministic tests incl. steps validation.
* **Code quality (10)**: structure, type hints on public surfaces, docstrings, PEP 8.
* **Docs & UX (10)**: README completeness; exact messages; clear CLI.

> **Disallowed for core**: `collections.deque`, `queue.Queue`, DS libs for the main queue.

---

## Optional Extensions (Extra Credit up to +10)

Choose up to two:

1. **Menu specials (+5):** `SPECIAL <item> <burst> <start_time> <end_time>` overrides the item’s burst within `[start_time, end_time)`. Reflect in `display menu=[...]`.
2. **Weighted fairness (+5):** `SETWEIGHT <queue_id> <w>` multiplies quantum for that queue (positive int). Show weight in queue display, e.g., `display WalkIns [2/5][ skip] w=2 -> [...]`.

Document policies + edge cases; keep outputs deterministic. Put extra tests in `/tests/extra/`.
