# Prompt design for Kolena Agents

Read this reference when writing a Prompt's instruction, when choosing or changing Prompt types, settings,
dependencies, or controls, or when diagnosing an inaccurate Result. Use the live tool schema for exact fields and
supported values.

## Choose the output and control shape

- **Text:** prose or a value with a specific shape; put the shape in `format` when possible.
- **Number:** a quantity that should be numeric. `integer`, `minimum`, and `maximum` can catch implausible outputs.
- **True/False:** a yes-or-no question. Set `default_value` only when missing evidence genuinely implies that answer.
- **Classification:** labels from a fixed set. It can select more than one when `allow_multiple` is enabled. Keep labels
  distinguishable, and represent a meaningful "none applies" case if the task needs one.
- **Form:** related named fields filled in together. It can replace several simple one-value Prompts, but a large set of
  difficult fields may be more reliable as separate Prompts.
- **Table:** one row per repeated item. Define what qualifies as a row, including negative or empty values that still
  count. Keep columns the user needs; a wide Table with many rows may take multiple passes.
- **Document Filter:** selects which Run documents downstream Prompts receive. Filename-only filtering is appropriate
  only when filenames reliably identify the content.
- **Conditional:** produces a value that determines which other Prompts run. Use it for genuinely different branches,
  not for an ordinary value that merely varies between Runs. Give it a closed set of outcomes, with a catch-all (for
  example, "Other") when the listed ones aren't exhaustive. When outcomes can occur together (for example, a call
  transcript that covers both sales and support), use one Yes/No Conditional per aspect, because a Prompt can be tied
  to only one outcome of a Conditional. Tie every Prompt in a branch to the outcome, not only the first: a Prompt that
  depends on a skipped Prompt gets no value. Once a Prompt is tied to an outcome, its instruction doesn't repeat the
  check.

Before settling a field's type, check two things the samples may hide. First, whether it can occur more than once in
a case (for example, a second borrower, a second appraisal, or one value per unit): a field built to hold one value
leaves nowhere for the second, and a rule such as "use the lower of the two" can't then be written; a Table, or a
Form field per occurrence, can hold them. Second, whether a rule needs more than two cases: a True/False that collapses
"yes", "no", and "an accepted equivalent" loses the difference, while a Classification keeps it.

## Ground the instruction and connect Prompts

- Inspect representative document contents when available; filenames and one example are not proof of every layout or
  exception. Use the documents' terms, and ask the user about consequential business rules the documents cannot settle.
  Keep one Run's names, dates, and amounts out of reusable instructions unless they are part of a standing rule.
- When a field can appear under several names, list them so the Prompt matches on meaning rather than one word. For
  example, an invoice's supplier may appear as the Vendor, Seller, or Remit-to party. Read the documents for the names
  they actually use. For an existing Agent, its past Runs may contain good sample documents. Without any, ask the user
  what their documents call it, and treat names you add from general knowledge as assumptions to confirm. When a field
  comes back "Not stated", check the source document before changing the Prompt: the value may truly be absent, or it
  may appear under a name the Prompt didn't know.
- When a Prompt is framed around one kind of document, say what to do with the others; otherwise it reports nothing
  even when equivalent information is there. For example, a Prompt written for itemized invoices should say what to
  capture from an invoice that shows only totals.
- When a Table must always include certain rows, tell the Prompt to mark a row "Not stated" when the documents don't
  address it, rather than filling it with a loosely related passage and a misleading citation.
- Check spreadsheets for layouts that silently corrupt numbers, and tell the Prompt how to handle any you find. For
  example: subtotal rows that double-count when a column is summed, a totals row partway down with more data below it,
  an outdated copy of a sheet beside the current one, dates stored as text, identifiers turned into scientific notation
  or stripped of leading zeros, totals typed in rather than calculated, or data from an earlier case left in a
  template.
- When a Prompt applies rules from a policy or guide, copy the rules it needs into the instruction rather than telling
  it to look them up in an attached document, and keep their exceptions and qualifiers ("except when", "where
  available"); those are the first thing lost when a rule is summarized. Prompt Documents remain right for material a
  Prompt looks values up in (for example, a rate card).
- Keep a large lookup table out of the instruction. Attach it as a CSV Prompt Document and look values up with Data
  Analysis. Format the lookup keys the same way on both sides and keep them as text, so a key such as "00123" still
  matches. Criteria that change from one use of the Agent to the next (for example, this quarter's thresholds) also
  belong in a Prompt Document rather than the instruction, so the Agent can be reused by replacing the file.
- Don't describe a setting in the instruction; turn the setting on. For example, "cite the page" is the Inline
  Citations setting, not a sentence. Don't open an instruction with a heading that repeats the Prompt's name; start
  with what to do.
- A downstream Prompt that only assembles upstream Results may use Ignore Run Files. Leave Run documents available
  when it still needs source details.
- For an Agent that checks, reconciles, or decides rather than only extracting, let a few extraction Prompts read the
  documents and have the Prompts that check or decide work from their Results with Ignore Run Files on. A reading
  error is then fixed in one place, a later Prompt can't pull a different value from the documents, and each Run
  usually reads less. Once other Prompts depend on an extracted field's name, keep the name stable.
- Document Filters scope which documents a Prompt receives. A Conditional gates a Prompt through `run_conditions`; use
  the values the Conditional can actually produce.
- Inline Citations are available for Text, Form, and Table. Enable them where provenance matters, but never infer a
  citation missing from a Result. For a large Table, citations can increase the work per row.

## Make decisions repeatable

Identical documents should get the same answer on every Run. Variation usually comes from a place where the
instruction still leaves the model to choose.

- Give each rule that decides an answer its own numbered line or row. A rule buried mid-paragraph tends to hold on
  clean documents and drop on messy ones.
- Use the same exact labels for a status in every Prompt that produces or reads it. For example, a later Prompt
  matching on "Fail" misses an earlier Prompt's "Hard fail".
- When an overall outcome follows from other Results (for example, how many checks failed), state the mapping
  explicitly rather than leaving it to judgment, and state which failures decide the outcome on their own.
- Write rules that must never bend as plain if-then statements, with no room for a softer answer.
- When a decision is arithmetic or a fixed rule (for example, a tolerance check, which of two values wins, or whether
  a total matches its rows), compute it with Data Analysis over upstream Table Results rather than describing it in
  prose. A rule that keeps giving different answers on identical documents is usually a decision the model is still
  making; move it into the calculation.

## Choose processing and cost settings

- Standard processing fits most document-reading tasks. Use Data Analysis for computation over tabular input (a CSV,
  spreadsheet, or upstream tabular Result); without tabular input it can fail or produce unreliable values. Use Enhanced
  Vision for visual details such as stamps or handwriting, and Web Search for facts outside the supplied documents.
- Beyond the `model_tier` guidance in the tool description, representative Results can also justify a change. Treat
  `efficient` as an experiment to check against them, and `high` as worth its cost only for genuinely harder work.
- Output length, the number of Prompts, and how much each Prompt reads can all affect credits. Simple fields grouped in
  one Form may avoid repeated document reads, but do not consolidate difficult fields at the expense of correctness.
  Document Filters can narrow input; a Conditional can skip work altogether. Large Tables may need repeated passes,
  especially as the column count grows. Prefer actual Run usage over a universal cost estimate.

## Diagnose before revising

- For `skipped`, inspect its run conditions and Conditional. For `error`, inspect the failure and processing mode.
  For `null` with neither, or an answer the instruction uses for a missing value (for example, "Not stated"), check
  that the relevant document or upstream Result reached the Prompt before rewriting it.
- A plausible but wrong value may come from a missing business rule, the wrong source document, an ambiguous
  instruction, a configuration or dependency error, or model limitations. Compare the actual Result with the source
  and any known-correct answer before choosing a fix. A right value in the wrong shape points toward type or format.
  Missing Table rows may mean the instruction never defined those rows as in scope.
- If `user_input` is present, the effective value includes a person's correction; it is not evidence that the Prompt
  generated that value.
