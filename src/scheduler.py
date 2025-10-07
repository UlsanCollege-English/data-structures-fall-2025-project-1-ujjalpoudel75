"""
Scheduler + QueueRR stubs for the Multi-Queue Round-Robin Café project.

Rules snapshot:
- Interactive program; blank line ends session with "Break time!".
- ENQ auto-generates task IDs as <queue_id>-NNN (1-based, zero-padded).
- Hardcoded menu must include at least these items (case-sensitive, lowercase):
  americano=2, latte=3, cappuccino=3, mocha=4, tea=1, macchiato=2, hot_chocolate=4
- RUN prints the café display AFTER EACH TURN (quantum).
- RUN steps must satisfy 1 ≤ steps ≤ (#queues).
- Disallowed for the core queue: collections.deque, queue.Queue, third-party DS.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional


# Required menu items; you may add more keys for your own tests/experiments.
REQUIRED_MENU: Dict[str, int] = {
    "americano": 2,
    "latte": 3,
    "cappuccino": 3,
    "mocha": 4,
    "tea": 1,
    "macchiato": 2,
    "hot_chocolate": 4,
}


@dataclass
class Task:
    task_id: str
    remaining: int


class QueueRR:
    """
    Implement a FIFO queue from scratch (no deque/Queue for the core).
    A circular buffer or two-stack queue are fine choices.
    """

    def __init__(self, queue_id: str, capacity: int) -> None:
        # TODO: initialize your internal storage, size/capacity tracking, etc.
        raise NotImplementedError

    def enqueue(self, task: Task) -> bool:
        """Return True on success; False if full (no mutation if full)."""
        raise NotImplementedError

    def dequeue(self) -> Optional[Task]:
        """Remove and return the front task; return None if empty."""
        raise NotImplementedError

    def __len__(self) -> int:  # pragma: no cover - trivial when implemented
        raise NotImplementedError


class Scheduler:
    """
    Orchestrates multiple QueueRR instances in creation order.
    Maintains:
      - current time (minutes)
      - per-queue auto-incrementing counters for task ids
      - per-queue pending SKIP flags
      - RR pointer for the next queue to visit
    """

    def __init__(self) -> None:
        # TODO: initialize time, queues (ordered), id_counters, skip flags, rr index.
        raise NotImplementedError

    # ----- Menu / state helpers -----

    def menu(self) -> Dict[str, int]:
        """
        Return the current menu mapping. Start with REQUIRED_MENU exactly.
        You may return a copy to avoid external mutation.
        """
        raise NotImplementedError

    def next_queue(self) -> Optional[str]:
        """
        Return the queue_id that will be visited next (or None if no queues).
        """
        raise NotImplementedError

    # ----- Commands -----

    def create_queue(self, queue_id: str, capacity: int) -> List[str]:
        """
        Log: time=<t> event=create queue=<queue_id>
        Creation order defines RR order.
        """
        raise NotImplementedError

    def enqueue(self, queue_id: str, item_name: str) -> List[str]:
        """
        Behavior:
          - If item_name not in menu: print "Sorry, we don't serve that."
            and log reject with reason=unknown_item.
          - Else construct next task id as <queue_id>-NNN and try to enqueue:
              - On success: log enqueue with remaining=<burst>.
              - On full: print "Sorry, we're at capacity."
                and log reject with reason=full.
        """
        raise NotImplementedError

    def mark_skip(self, queue_id: str) -> List[str]:
        """
        Mark the queue to be skipped on its next visit (does not advance time).
        Log: time=<t> event=skip queue=<queue_id>
        """
        raise NotImplementedError

    def run(self, quantum: int, steps: Optional[int]) -> List[str]:
        """
        Execute up to 'steps' turns (each turn visits one queue) if provided,
        otherwise run until all queues are empty and no pending skips.

        Validate steps: 1 ≤ steps ≤ (#queues); otherwise:
          Log: time=<t> event=error reason=invalid_steps
          and do not perform any turns.

        Each visited queue should produce:
          - a run log:   time=<t> event=run queue=<qid>
          - zero-time transitions for empty/skip visits (no time advance)
          - if work occurs: time increases by min(remaining, quantum)
            and follow with work/finish logs as appropriate.
        """
        raise NotImplementedError

    # ----- Display -----

    def display(self) -> List[str]:
        """
        Return a compact snapshot with the exact lines/format:

          display time=<t> next=<qid_or_none>
          display menu=[name:minutes,...sorted by name...]
          display <qid> [n/cap][ skip] -> [task:rem,task:rem,...]
          ...

        NOTE: The CLI prints this after EACH RUN TURN only.
        """
        raise NotImplementedError
