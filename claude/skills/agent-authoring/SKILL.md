---
name: agent-authoring
description: >-
  Use when creating or improving a Kolena Agent by designing or revising its Prompts, settings, dependencies, and
  controls, or diagnosing inaccurate Results. Not for simply processing documents with an existing Agent.
---

# Agent authoring

Build a reusable Agent that produces the user's intended business output, not merely an empty Agent. Own the Prompt
design; ask the user for domain rules, exceptions, and disputed answers rather than asking them to write Prompts.
Use the `process-documents` skill when the task is only to process documents with an existing Agent.

When choosing or changing Prompt types, settings, dependencies, or controls, or diagnosing Results, read
[Prompt design for Kolena Agents](references/prompt-design.md).

## Establish the target and requirements

- Resolve the intended Account and Workspace before writing. If either is ambiguous, ask; do not switch targets to
  work around an error. For an existing Agent, read its current configuration with `kolena_get_agent` and inspect
  relevant Runs and Results when the request concerns its behavior.
- Establish what documents belong in one Run, the desired output, and how people will use it. Distinguish documents
  supplied per Run from standing Prompt Documents. Ask focused questions where missing business rules or required
  inputs would materially change the Agent; do not infer them from one sample or a convenient nearby value.

## Design and change

- Use the smallest Prompt set that meets the requirement. Add Document Filters, Conditionals, dependencies, or
  processing modes when they solve an actual input or output problem; do not optimize credits at the expense of
  untested correctness.
- Create upstream Prompts before dependent ones, using the returned IDs in `<kolena-prompt id="N"/>` tags. Prompt
  order alone does not create dependencies. A newly created Agent without Prompts performs no processing.
- Treat earlier tool results as snapshots. Before editing after a pause, a reported out-of-band change, or a
  conflicting result, re-read the Agent. If an intervening change affects the planned edit, reconcile it with the
  user rather than silently overwriting it. `kolena_update_prompt` replaces any supplied instruction or type-specific
  `config` as a whole; preserve the dependency tags and settings that should remain.
- After related writes, read the Agent back to confirm saved instructions, configurations, and dependencies. If a
  write is not yet reflected, check again before treating it as failed. Do not report a change as verified solely
  because a write call succeeded.

## Verify as the task warrants

- A Prompt edit can make existing Results, including dependent Results, out of date; it does not recompute them.
  When testing is useful and authorized, prefer representative existing Runs and known-correct answers. New Runs and
  re-running Prompts consume credits. Use `process-documents` for test-Run upload and retrieval mechanics when needed.
  Do not assume every authoring task needs a new Run or a fixed iteration loop, and do not start broad or repeated
  billable recomputation without clear user direction.
- Diagnose a Result before revising its Prompt. Distinguish failed, skipped, empty, human-corrected, and plausible
  but wrong values, and check whether a Result came from the current Prompt version. Without known-correct answers
  or accessible Validation results, describe observations rather than claiming measured accuracy.

If Kolena tools are unavailable or authentication fails, say the connection needs setting up or signing in again;
do not infer that an Account has no Agents or Runs. Finish by naming what changed, what was actually checked, and
which business decisions or uncertainties remain. Link the Agent and relevant Runs using returned `web_url` values.
