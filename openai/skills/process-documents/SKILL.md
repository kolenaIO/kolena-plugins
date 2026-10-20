---
name: process-documents
description: >-
  Use an existing Kolena Agent to process user-provided documents or inspect a past Run and explain its Results. Use for
  extraction or review with an existing Agent, not for creating or editing one.
---

# Process documents with a Kolena Agent

Choose an Agent whose Prompts produce the user's requested output; do not build or edit a shared Agent merely to
complete one document-processing request.

If Kolena tools are unavailable or authentication fails, tell the user to connect or reconnect Kolena. Do not treat an
unavailable connection as evidence that the Account has no Agents or Runs.

1. Resolve the Account, then find the Agent. If several Accounts are available and the user has not identified one, ask
   rather than guessing. If several Agents could fit, inspect their full Prompt configurations or ask the user to choose
   rather than spending credits on a guess. Keep the selected Account throughout the task unless the user directs a
   change.
2. Decide which documents belong in each Run. A Run normally represents one case: a contract and its amendments belong
   together; unrelated invoices normally need separate Runs. Ask when the grouping changes what the Agent will conclude.
   Prompts can narrow their inputs with Document Filters, so do not assume every Prompt reads every uploaded document.
3. For new Runs, follow `kolena_create_upload_target`'s upload instructions. Its URL requires a direct HTTP upload,
   outside the MCP connection. Use it only if the client can send the user's files to that URL; if not, give the user
   the Agent's `web_url` and explain that they can create the Run in Kolena. Do not claim the files were processed if
   upload was unavailable or failed.
4. After upload, use the returned Run ID to check processing with `kolena_get_run`, waiting between checks rather than
   polling tightly. Inspect document ingestion errors and the Run's final status. A failed Run may still have usable
   Prompt Results.
5. Read Results with `kolena_list_run_results` and explain them by Prompt name. Distinguish a failed Prompt (`error`), a
   Prompt intentionally not run (`skipped`), and an empty result (`null` without either). If `user_input` is present,
   `value` is a person's correction, not the Agent's generated answer. Cite document/page evidence when the result
   actually supplies it; do not invent citations. Link the Run using its canonical `web_url`.

Treat earlier Run and Result responses as snapshots. If processing was still underway, the user reports a correction or
other change made elsewhere, or the task resumes after a pause, refresh the Run and its Results before interpreting or
recomputing them. If they have changed materially, revise the answer or plan rather than repeating an earlier value.

For a past Run, locate it with `kolena_list_runs` and read existing Results first. Recompute with `kolena_run_prompts`
only when the user's task calls for it: it consumes credits and replaces generated Results for the selected Prompts. Ask
before a broad re-run, and never re-run merely because a result is surprising.
