---
name: process-documents
description: >-
  Run documents through an existing Kolena Agent and report what it found, or explain what a past Run produced. Use
  when the user wants documents processed, reviewed, or turned into structured fields — contracts, invoices, loan
  files, leases, statements. Not for creating or editing Agents.
---

# Process documents with a Kolena Agent

Use an existing Agent; don't create or edit one to satisfy a single request. A Prompt's instruction is shared by
everyone who uses that Agent, so changing it changes every future Run. Use the `agent-authoring` skill for that.

If the Kolena tools are missing or a call fails authentication, tell the user to connect or sign in to Kolena again.
An unreachable connection is not evidence that the Account has no Agents or Runs.

1. Find the Agent. `kolena_list_agents` returns each Agent's Prompt outline. If none fits, say so and describe what
   one would need to contain. When more than one could fit, including two Agents that share a name, ask which to use
   before uploading anything. Read their configurations with `kolena_get_agent` to tell the user how they differ, not
   to choose for them: the wrong Agent spends credits and can reach a different answer.

2. Decide which documents belong in each Run. A Run is one case: a contract and its amendments belong together, while
   twelve invoices from twelve vendors are twelve Runs. Ask when the grouping changes what the Agent will conclude.
   Document Filters can narrow what a Prompt reads, so don't assume each Prompt saw every document you sent.

3. Create the Run with `kolena_create_upload_target`. The upload is a direct HTTP request outside this connection;
   if you can't send the user's files to `upload_url`, give the user the Agent's `web_url` and say they can create the
   Run in Kolena instead. Quote `upload_url` when passing it to a shell — it carries query parameters, and an unquoted
   argument is cut at the first `&`. Never report documents as processed when the upload didn't happen or failed.

4. Wait for processing. How long a Run takes varies with its size and with demand, from under a minute to much longer,
   so a Run that stays `running` is not by itself a sign of trouble. Wait around 30 seconds before the first
   `kolena_get_run`, then back off rather than polling in a tight loop. If it is still running after several minutes,
   tell the user it's still processing and link the Run, rather than waiting indefinitely.

5. Check the Run's `documents` before reading results. A document with an `error`, or not `completed`, never reached
   the Agent — say which. One uploaded file can appear as several documents, so count uploads by `original_filename`.
   A `failed` Run means at least one Prompt errored, not that the Run produced nothing.

6. Read the output with `kolena_list_run_results` and report what each Prompt returned by name, not as raw JSON.
   Distinguish a Prompt that failed (`error`), one whose run conditions were not met (`skipped`), and one that found
   nothing (`null` with neither). Where a result carries `user_input`, `value` is a person's correction rather than
   the Agent's own output. Cite the document and page a result points to when it supplies them; never invent a
   citation. If the user wants documents like these processed automatically as they arrive, or wants Results as a
   filled-in report, mention that an Integration or an Output Template does that, set up in Kolena.

For a past Run, find it with `kolena_list_runs` — by document name, submitter, date, or what the Agent found — and
read its existing Results first. Use `kolena_run_prompts` only when the user's task calls for a Prompt to be computed
again. Never re-run merely because a result is surprising, and confirm before re-running across many Runs.

Results and configuration you read earlier can change while you work. Never report a Run's status or its results from
memory; `kolena_get_run` and `kolena_list_run_results` don't consume credits. A result whose `prompt_version` is below
the Prompt's current `version` in `kolena_get_agent` was produced by an earlier instruction and no longer reflects it.
A `user_input` that wasn't there before means a person overrode that value since you read it.
