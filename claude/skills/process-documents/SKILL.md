---
name: process-documents
description: >-
  Run local documents through a Kolena Agent and report what it found. Use when the user wants documents processed,
  reviewed, or turned into structured fields — contracts, invoices, loan files, leases, statements — or asks what a
  past Run produced. Not for designing or editing Agents.
---

# Process documents with a Kolena Agent

Use an existing Agent; don't create or edit one to satisfy a single request. A Prompt's instruction is
shared by everyone who uses that Agent, so changing it changes every future Run. Use this plugin's
Agent-authoring skill for that.

If the Kolena tools are missing or a call fails authentication, say the connection needs setting up or
signing in again. An unreachable connector is not evidence that the Account has no Agents or Runs.

1. Resolve the Account, then find the Agent with `kolena_list_agents`, which returns each Agent's
   Prompt outline. When several could fit, or two share a name, read their full configuration with
   `kolena_get_agent` or ask which to use rather than spending credits on a guess. If none fits, say so
   and describe what one would need to contain.

2. Decide which documents belong in each Run. A Run is one case: a contract and its amendments belong
   together, while twelve invoices from twelve vendors are twelve Runs. Ask when the grouping changes
   what the Agent will conclude. Within a Run, every Prompt reads every document unless a Document
   Filter narrows it, so don't assume each Prompt saw everything you sent.

3. Create the Run with `kolena_create_upload_target` and follow its upload instructions. The
   `upload_url` is a direct HTTPS request you make yourself, outside this connection; if you can't make
   outbound requests, give the user the Agent's `web_url` and say they can create the Run in Kolena.
   Never report documents as processed when the upload didn't happen or failed. Quote the `upload_url`
   when passing it to a shell — it carries query parameters, and an unquoted argument is truncated at
   the first `&`. Kolena accepts PDFs, Office files, spreadsheets, images, audio, email files, zip
   archives, and text formats; an unsupported file is rejected at upload and the error names it, so
   send the batch rather than pre-filtering on a guess.

4. Poll `kolena_get_run` with the `id` from the upload's response. Small Runs finish in well under a
   minute: wait around 30 seconds before the first check, then back off, and never poll in a tight
   loop.

5. Check the Run's `documents` before reading results. One carrying an `error`, or not `completed`,
   never reached the Agent — say which. `documents` also holds converted copies, so count originals by
   `original_filename`. A `failed` status means at least one Prompt errored, not that the Run produced
   nothing.

6. Read the output with `kolena_list_run_results` and report what each Prompt returned by name, not as
   raw JSON. Distinguish a Prompt that failed (`error`), one whose run conditions were not met
   (`skipped`), and one that found nothing (`null` with neither). Where a result carries `user_input`,
   `value` is a person's correction rather than the Agent's own output. Cite the document and page a
   result points to when it supplies them; never invent a citation. Link the Run by its `web_url`.

For a past Run, find it with `kolena_list_runs` — by document name, submitter, date, or what the Agent
found — and read existing Results first. Use `kolena_run_prompts` only when the user's task calls for a
Prompt to be computed again: it bills again and replaces that Prompt's generated result, though hand
corrections survive. Never re-run merely because a result is surprising, and confirm before re-running
across many Runs.

Results and configuration you read earlier can change while you work. Never report a Run's status or
its results from memory; `kolena_get_run` and `kolena_list_run_results` are free. A result whose
`prompt_version` is below that Prompt's current `version` was produced by an earlier instruction and no
longer reflects it. A `user_input` that wasn't there before means a person overrode that value since
you read it.
