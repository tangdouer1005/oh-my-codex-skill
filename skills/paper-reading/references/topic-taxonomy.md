# Paper Topic Taxonomy

Use exactly one of the following paths as the primary `Topic` in paper notes.

## Allowed Topic Paths

- `agents/coding`
- `agents/memory`
- `agents/planning`
- `agents/eval`
- `agents/harness`
- `llm/reasoning`
- `llm/retrieval`
- `llm/alignment`
- `llm/training`
- `infra/serving`
- `infra/storage`
- `infra/tooling`
- `domain/database`
- `domain/os`
- `domain/compiler`

## Classification Heuristics

- Choose `agents/harness` when the paper is mainly about scaffolds, context management, orchestration, tool-use loops, or outer-loop optimization around a fixed model.
- Choose `agents/coding` when the paper is mainly about code-generation agents, SWE agents, coding benchmarks, or repository-level software tasks.
- Choose `agents/memory` when the main contribution is memory formation, retrieval from episodic history, long-term memory, or persistent memory for agents.
- Choose `agents/planning` when the core problem is decomposition, search, planning, subgoal generation, or deliberate control.
- Choose `agents/eval` when the paper is mainly about evaluation methodology, benchmarks, reward design, judging, or reliability assessment for agents.
- Choose `llm/reasoning` when the main focus is reasoning quality, theorem solving, chain-of-thought style inference, verifier loops, or problem-solving behavior.
- Choose `llm/retrieval` when the main contribution centers on retrieval-augmented generation, retrieval policy, index design, memory retrieval, or evidence selection for LLMs.
- Choose `llm/alignment` when the main focus is preference optimization, safety, harmlessness, honesty, control, or value alignment.
- Choose `llm/training` when the main contribution is pretraining, finetuning, distillation, RL, data mixture, architecture training tricks, or optimization of model weights.
- Choose `infra/serving` when the paper is mainly about inference systems, latency, throughput, deployment, scheduling, or online serving infrastructure.
- Choose `infra/storage` when the focus is storage engines, memory hierarchies, data layout, caching systems, or persistence infrastructure.
- Choose `infra/tooling` when the work is about developer tools, build systems, observability tools, debugging tools, or engineering platforms.
- Choose `domain/database`, `domain/os`, or `domain/compiler` only when the paper is primarily about that domain itself rather than LLMs or agents applied to it.

## Tie-Break Rule

If a paper fits multiple topics, choose the path that best matches the paper's main claimed contribution, not just its evaluation benchmark.
