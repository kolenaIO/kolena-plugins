# Kolena Agents

Run documents through your [Kolena](https://www.kolena.com) Agents from a conversation with Claude,
follow a Run until it finishes, and read what the Agent found.

A Kolena Agent is a reusable document-processing workflow: each of its Prompts reads the documents you
send and produces one typed result, so a batch of contracts, invoices, or loan files comes back as
structured fields rather than prose.

## Use it

Ask Claude to send local documents to one of your Agents. Claude names the files, uploads them, waits
for processing, and reports the result of each Prompt with a link to the Run in Kolena. You can also
ask it to find past Runs by document name, by who submitted them, or by what the Agent found, and to
re-run individual Prompts after you reword them.

Creating a Run and re-running Prompts consume Kolena credits.

## Requirements

A Kolena account with the MCP server enabled for your Organization, on a plan that includes it. The
first time you use the connector, Claude opens a browser window to sign in to Kolena. The assistant
acts with your own permissions and can only see and change what you can.

## Data

The plugin sends the documents you choose, and the prompts you type about them, to your Kolena
Organization through `agents-api.kolena.com`. It stores nothing itself. Documents and results are
retained by Kolena under your Organization's own data retention policy.
