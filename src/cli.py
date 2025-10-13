# src/cli.py

import sys
from typing import List
# Note: Assuming relative imports work correctly based on project structure
try:
    from .parser import parse_command
    from .scheduler import Scheduler
except ImportError:
    # Fallback for direct execution/testing if not run via python -m
    from parser import parse_command
    from scheduler import Scheduler


def main() -> None:
    sched = Scheduler()

    for raw in sys.stdin:
        line = raw.rstrip("\n")

        # Blank line ends session
        if line == "":
            print("Break time!")
            return

        parsed = parse_command(line)
        logs: List[str] = []

        if parsed is None:
            # comment or whitespace line inside session (ignored)
            pass
        else:
            cmd, args = parsed

            # Dispatch with minimal argument plumbing.
            # NOTE: The Scheduler implementation handles printing custom messages
            # like "Sorry, we're at capacity."
            try:
                if cmd == "CREATE":
                    if len(args) != 2:
                        logs.extend([f"time=? event=error reason=bad_args"])
                    else:
                        qid, cap_str = args
                        cap = int(cap_str)
                        logs.extend(sched.create_queue(qid, cap))

                elif cmd == "ENQ":
                    if len(args) != 2:
                        logs.extend([f"time=? event=error reason=bad_args"])
                    else:
                        qid, item = args
                        logs.extend(sched.enqueue(qid, item))

                elif cmd == "SKIP":
                    if len(args) != 1:
                        logs.extend([f"time=? event=error reason=bad_args"])
                    else:
                        (qid,) = args
                        logs.extend(sched.mark_skip(qid))

                elif cmd == "RUN":
                    if not (1 <= len(args) <= 2):
                        logs.extend([f"time=? event=error reason=bad_args"])
                    else:
                        quantum = int(args[0])
                        steps = int(args[1]) if len(args) == 2 else None
                        # Expect Scheduler.run to return *all* logs in order.
                        logs.extend(sched.run(quantum, steps))

                else:
                    logs.extend([f"time=? event=error reason=unknown_command"])

            except ValueError:
                # e.g., non-integer capacity/quantum/steps
                logs.extend([f"time=? event=error reason=bad_args"])

        # Print logs produced by this line
        if logs:
            print("\n".join(logs))


if __name__ == "__main__":
    main()