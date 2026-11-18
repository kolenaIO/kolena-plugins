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

When writing Prompt instructions, choosing or changing Prompt types, settings, dependencies, or controls, or
diagnosing Results, read [Prompt design for Kolena Agents](references/prompt-design.md).

## Establish the target and requirements

- Resolve the intended Workspace before writing. If it is ambiguous, ask; do not switch Workspaces to work around an
  error. For an existing Agent, read its current configuration with `kolena_get_agent` and inspect relevant Runs and
  Results when the request concerns its behavior.
- Establish what documents belong in one Run, the desired output, and how people will use it. Distinguish documents
  supplied per Run from standing Prompt Documents. Ask focused questions where missing business rules or required
  inputs would materially change the Agent; do not infer them from one sample or a convenient nearby value.
- Understand how the work is done today before designing Prompts: the steps a person follows, the decisions along the
  way, what each step reads and produces, and which steps depend on others. Design the Prompts from that rather than
  one Prompt per step; one Prompt may cover several steps, and one step may need several Prompts.
- Ask for the documents of a few representative cases, each one Run's worth, before writing Prompts, including the
  harder variations (for example, a scanned copy, an amended version, or an unusual layout), and, where they exist,
  the finished outputs people currently produce from them. For an existing Agent, its past Runs may contain good
  sample documents; start there. Expected outputs show what the Agent should produce better than a description does.
  Use them to design the Prompts and to check Results, but don't send them with a Run: an Agent that can read the
  answers will look correct whatever its Prompts do. If the user has no documents yet, you can still build from their
  description, a template, or a sample form, but tell them which instructions rest on assumptions a real document
  should confirm, and suggest testing on real documents before relying on the Agent.
- Identify values the Agent needs that the Run's documents can't supply (for example, an as-of date, a reporting
  period, or an identifier assigned later in the process). Agree with the user where each comes from (a document sent
  with the Run, a Prompt Document, or the Agent Guidelines) rather than leaving a Prompt to work it out; a guessed
  value can be far off and still look plausible. When an identifier doesn't exist yet at the time of the Run, have the
  Prompt report it as missing rather than derive it from something similar.
- Separate checks the documents can prove from checks that depend on systems, schedules, or people. A Prompt should
  report the second kind as needing evidence from outside the documents, not as passed or failed.
- Test each rule against the version of the document that will actually be in the Run. A requirement written for a
  final or executed document will falsely fail a draft or earlier version; restate the rule for the version that
  arrives, or tell the user it can't be checked at this point.
- When sources disagree, raise the difference rather than choosing one silently. For example, the user's description
  of a rule may conflict with their written policy, two documents may give different values, or a rule may be called
  mandatory in one place and optional in another.

## Design and change

- Use the smallest Prompt set that meets the requirement. Add Document Filters, Conditionals, dependencies, or
  processing modes when they solve an actual input or output problem; do not optimize credits at the expense of
  untested correctness. An Agent that checks or decides may still need separate extraction Prompts; the reference
  explains when.
- Put rules that apply to every Prompt in the Agent Guidelines once, with `kolena_update_agent_guidelines`, rather than
  repeating them in each Prompt: for example, quoting exact wording, how to answer when a value is absent, or which
  document controls. Test each sentence: if it applies to every Prompt, it belongs in the Guidelines; if it applies to
  one Prompt, it stays in that Prompt, however long that makes it. The Guidelines reach every Prompt, so nothing
  specific to one Prompt belongs there. The tool replaces the whole text, so carry forward what is already there.
- When a Run can hold several versions of a document (for example, an original with later amendments, or a draft
  alongside a signed copy), set the order that decides which one controls and put it in the Agent Guidelines. A common
  order: the most recent date wins, a signed copy beats a draft, and the document closest to the decision wins;
  otherwise the Prompt flags the conflict rather than choosing. Confirm the order with the user. For large bundles, a
  first Prompt that lists the documents and which one controls each topic can feed the Prompts that extract from them.
- Use the same few answers for missing values across the Agent, defined once in the Agent Guidelines: for example,
  "Not stated" when the documents don't give the value, "Needs Review" when a Prompt can't proceed safely, and
  "Missing" for a value assigned later in the process. A Prompt gives one of these rather than a guess.
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
- Agree on what counts as correct before judging Results: the user's finished outputs for the same documents, a list
  of expected values they supply, or Results from a Run they have reviewed and accept. Don't treat the Agent's own
  output as the answer until the user has confirmed it.
- Diagnose a Result before revising its Prompt. Distinguish failed, skipped, empty, human-corrected, and plausible but
  wrong values, and check whether its `prompt_version` matches the Prompt's current `version` in `kolena_get_agent`.
  Without a Validation against a Ground Truth, or known-correct answers from the user, describe observations rather
  than claiming measured accuracy.
- Test on more than one Run's worth of documents. Prompts revised until they are right on one case can still miss on
  the next, so check changes against cases they weren't tuned on, ideally ones whose documents differ in layout,
  version, or exceptions. If the user has supplied documents for only one Run, ask for more. A new case tells you more
  than re-running one you have already tested.

## Features to set up in Kolena

These tools can't configure the features below yet. When one would serve the user's goal, recommend it, say it is set up
in Kolena, and link the Agent's `web_url` and the feature's guide where one is linked below. Don't leave it out, or
substitute something weaker, without telling the user.

- **[Prompt Documents](https://docs.agents.kolena.com/prompts#attaching-files):** files attached to a Prompt as
  reference material it uses on every Run, such as a rate card, policy, or checklist.
- **[Agent Validation](https://docs.agents.kolena.com/how-to/measuring-accuracy):** scores an Agent's output against a
  Ground Truth, a set of known-correct answers, from the Agent's Validation tab. Runs are matched to the Ground Truth by
  `user_defined_id`, so give test Runs one the user supplies. It may need to be enabled for the user's organization.
- **[Output Templates](https://docs.agents.kolena.com/templated-outputs):** a document or spreadsheet filled with a
  Run's Results. Each Prompt's `template_alias` is its placeholder.
- **[Integrations](https://docs.agents.kolena.com/connections):** bring documents into an Agent automatically, or send
  its Results elsewhere, for recurring work.

If the Kolena tools are missing or a call fails authentication, tell the user to connect or sign in to Kolena again; do
not infer that an Account has no Agents or Runs. Finish by naming what changed, what was actually checked, and which
business decisions or uncertainties remain. List any rule, step, threshold, tolerance, or mapping you added without
the user or their documents stating it, so they can confirm or correct it.
