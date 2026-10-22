---
name: agent-authoring
description: >-
  Use when creating or improving a Kolena Agent by designing or revising its Prompts, settings, dependencies, and
  controls, or diagnosing inaccurate Results. Not for simply processing documents with an existing Agent.
---

# Agent authoring

Build a reusable Agent that produces the user's intended business output, not merely an empty Agent. Own the Prompt
design; ask the user for domain rules, exceptions, and disputed answers rather than asking them to write Prompts. If
they want to word instructions themselves, point them to
[Writing Effective Prompts](https://docs.agents.kolena.com/writing-effective-prompts). Use the `process-documents` skill
when the task is only to process documents with an existing Agent.

When choosing or changing Prompt types, settings, dependencies, or controls, or diagnosing Results, read
[Prompt design for Kolena Agents](references/prompt-design.md).

## Establish the target and requirements

- Resolve the intended Workspace before writing. If it is ambiguous, ask; do not switch Workspaces to work around an
  error. For an existing Agent, read its current configuration with `kolena_get_agent` and inspect relevant Runs and
  Results when the request concerns its behavior.
- Establish what documents belong in one Run, the desired output, and how people will use it. Distinguish documents
  supplied per Run from standing Prompt Documents. Ask focused questions where missing business rules or required
  inputs would materially change the Agent; do not infer them from one sample or a convenient nearby value.

## Design and change

- Use the smallest Prompt set that meets the requirement. Add Document Filters, Conditionals, dependencies, or
  processing modes when they solve an actual input or output problem; do not optimize credits at the expense of
  untested correctness.
- Treat earlier tool results as snapshots. Before editing after a pause, a reported out-of-band change, or a conflicting
  result, re-read the Agent. If an intervening change affects the planned edit, reconcile it with the user rather than
  silently overwriting it.
- After related writes, read the Agent back to confirm saved instructions, configurations, and dependencies. If a write
  is not yet reflected, check again before treating it as failed. Do not report a change as verified solely because a
  write call succeeded.

## Verify as the task warrants

- A Prompt edit can make existing Results, including dependent Results, out of date; it does not recompute them.
  When testing is useful and authorized, prefer representative existing Runs and known-correct answers. New Runs and
  re-running Prompts consume credits. Use `process-documents` for test-Run upload and retrieval mechanics when needed.
  Do not assume every authoring task needs a new Run or a fixed iteration loop, and do not start broad or repeated
  billable recomputation without clear user direction.
- Diagnose a Result before revising its Prompt. Distinguish failed, skipped, empty, human-corrected, and plausible but
  wrong values, and check whether its `prompt_version` matches the Prompt's current `version` in `kolena_get_agent`.
  Without a Validation against a Ground Truth, or known-correct answers from the user, describe observations rather
  than claiming measured accuracy.

## Features to set up in Kolena

These tools can't configure the features below yet. When one would serve the user's goal, recommend it, say it is set up
in Kolena, and link the Agent's `web_url` and the feature's guide where one is linked below. Don't leave it out, or
substitute something weaker, without telling the user.

- **[Prompt Documents](https://docs.agents.kolena.com/prompts#attaching-files):** files attached to a Prompt as
  reference material it uses on every Run, such as a rate card, policy, or checklist.
- **Agent Guidelines:** instructions applied across all of an Agent's Prompts. `kolena_get_agent` returns existing ones;
  keep new Prompts consistent with them.
- **[Agent Validation](https://docs.agents.kolena.com/how-to/measuring-accuracy):** scores an Agent's output against a
  Ground Truth, a set of known-correct answers, from the Agent's Validation tab. Runs are matched to the Ground Truth by
  `user_defined_id`, so give test Runs one the user supplies. It may need to be enabled for the user's organization.
- **[Output Templates](https://docs.agents.kolena.com/templated-outputs):** a document or spreadsheet filled with a
  Run's Results. Each Prompt's `template_alias` is its placeholder.
- **[Integrations](https://docs.agents.kolena.com/connections):** bring documents into an Agent automatically, or send
  its Results elsewhere, for recurring work.

If the Kolena tools are missing or a call fails authentication, tell the user to connect or sign in to Kolena again; do
not infer that an Account has no Agents or Runs. Finish by naming what changed, what was actually checked, and which
business decisions or uncertainties remain.
