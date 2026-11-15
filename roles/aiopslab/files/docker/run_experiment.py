"""Runs one AIOpsLab experiment end-to-end and exits.

AIOpsLab ships no scriptable CLI - cli.py is an interactive REPL. This mirrors the
non-interactive pattern used by AIOpsLab's own example agents under clients/ (see
clients/gpt.py's __main__ block), but for a single problem instead of looping over the
whole registry, and driven by environment variables instead of being hardcoded.
"""

import asyncio
import json
import os
import sys

from dotenv import load_dotenv

from aiopslab.orchestrator import Orchestrator
from clients.registry import AgentRegistry

load_dotenv()


def main() -> int:
    problem_id = os.environ["AIOPSLAB_PROBLEM_ID"]
    agent_name = os.environ.get("AIOPSLAB_AGENT", "gpt")
    max_steps = int(os.environ.get("AIOPSLAB_MAX_STEPS", "30"))

    agent_cls = AgentRegistry().get_agent(agent_name)
    if agent_cls is None:
        print(f"Unknown AIOpsLab agent '{agent_name}'", file=sys.stderr)
        return 1

    agent = agent_cls()
    orchestrator = Orchestrator()
    orchestrator.register_agent(agent, name=agent_name)

    problem_desc, instructions, apis = orchestrator.init_problem(problem_id)
    agent.init_context(problem_desc, instructions, apis)

    result = asyncio.run(orchestrator.start_problem(max_steps=max_steps))
    print(json.dumps(result, default=str, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
