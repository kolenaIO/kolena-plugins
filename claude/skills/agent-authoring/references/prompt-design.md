# Prompt design for Kolena Agents

Read this reference when choosing or changing Prompt types, settings, dependencies, or controls, or when diagnosing
an inaccurate Result. Use the live tool schema for exact fields and supported values.

## Choose the output and control shape

- **Text:** prose or a value with a specific shape; put the shape in `format` when possible.
- **Number:** a quantity that should be numeric. `integer`, `minimum`, and `maximum` can catch implausible outputs.
- **True/False:** a yes-or-no question. Set `default_value` only when missing evidence genuinely implies that answer.
- **Classification:** labels from a fixed set. It can select more than one when `allow_multiple` is enabled. Keep labels
  distinguishable, and represent a meaningful "none applies" case if the task needs one.
- **Form:** related named fields filled in together. It can replace several simple one-value Prompts, but a large set of
  difficult fields may be more reliable as separate Prompts.
- **Table:** one row per repeated item. Define what qualifies as a row, including negative or empty values that still
  count. Keep columns the user needs; a wide Table with many rows may take multiple extraction passes.
- **Image:** a cropped image region from a document, when the intended output is the image itself.
- **Document Filter:** selects which Run documents downstream Prompts receive. Filename-only filtering is appropriate
  only when filenames reliably identify the content.
- **Conditional:** produces a value that determines which other Prompts run. Use it for genuinely different branches,
  not for an ordinary value that merely varies between Runs.

## Ground the instruction and connect Prompts

- Inspect representative document contents when available; filenames and one example are not proof of every layout or
  exception. Use the documents' terms, and ask the user about consequential business rules the documents cannot settle.
  Keep one Run's names, dates, and amounts out of reusable instructions unless they are part of a standing rule.
- A downstream Prompt that only assembles upstream Results may use Ignore Run Files. Leave Run documents available
  when it still needs source details.
- Document Filters scope which documents a Prompt receives; multiple filters combine their selections. A Conditional
  gates a Prompt through `run_conditions`; use the values the Conditional can actually produce.
- Inline Citations are available for Text, Form, and Table. Enable them where provenance matters, but never infer a
  citation missing from a Result. For a large Table, citations can increase the work per row.

## Choose processing and cost settings

- Standard processing fits most document-reading tasks. Use Data Analysis for computation over tabular input (a CSV,
  spreadsheet, or upstream tabular Result); without tabular input it can fail or produce unreliable values. Use Enhanced
  Vision for visual details such as stamps or handwriting, and Web Search for facts outside the supplied documents.
- Leave `model_tier` at `default` unless the task plainly needs another tier, the user states a cost or accuracy
  priority, or representative results support a change. Treat `efficient` as a cost/quality experiment, not a silent
  downgrade; `high` is appropriate for harder work when its added cost is justified.
- Output length, the number of Prompts, and how much each Prompt reads can all affect credits. Simple fields grouped in
  one Form may avoid repeated document reads, but do not consolidate difficult fields at the expense of correctness.
  Document Filters can narrow input; a Conditional can skip work altogether. Large Tables may need repeated passes,
  especially as the column count grows. Prefer actual Run usage over a universal cost estimate.
- Editing a Prompt can leave its existing Results and dependent Results out of date. It does not recompute them
  automatically; recomputation consumes credits. Before broad or repeated recomputation, establish its scope with the
  user. Do not treat a saved Result from an older Prompt version as proof of current behavior.

## Diagnose before revising

- For `skipped`, inspect its run conditions and Conditional. For `error`, inspect the failure and processing mode.
  For `null` with neither, check that the relevant document or upstream Result reached the Prompt before rewriting it.
- A plausible but wrong value may come from a missing business rule, the wrong source document, an ambiguous
  instruction, a configuration or dependency error, or model limitations. Compare the actual Result with the source
  and any known-correct answer before choosing a fix. A right value in the wrong shape points toward type or format.
  Missing Table rows may mean the instruction never defined those rows as in scope.
- If `user_input` is present, the effective value includes a person's correction; it is not evidence that the Prompt
  generated that value. Check the Result's `prompt_version` against the current Prompt version before claiming that
  current instructions produced it.
