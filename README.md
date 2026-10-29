# EPD Claim Witness

EPD Claim Witness is an experimental GenLayer Intelligent Contract prototype for checking a narrowly defined claim about a building product against its public Environmental Product Declaration (EPD).

## What it checks

The current prototype accepts an International EPD System registration number, a claimed product name, a declared unit, and a claimed GWP-total value for life-cycle modules A1-A3.

It retrieves the public EPD page and its linked PDF, asks the contract's extraction step to identify relevant facts and supporting quotes, and compares the extracted product, unit, indicator, module, and value with the submitted claim.

The current implementation is intentionally limited to EPD-IES registration numbers and GWP-total for A1-A3. This is the prototype's implemented scope, not a claim that the same method works for every EPD program, indicator, or life-cycle module.

## Why GenLayer

Relevant EPD evidence can appear in document tables and text rather than in a consistent data field. The contract uses GenLayer's non-deterministic web and extraction calls for that evidence, then applies deterministic comparison rules and strict equivalence to the result before recording an assessment.

The consensus-critical assessment is part of the Intelligent Contract. A single website or an off-chain AI response is not treated as the final authority.

## Assessment results

The contract records one of these outcomes:

- `SUPPORTED`: the submitted product, declared unit, indicator, module, and value match the extracted EPD evidence.
- `CONTRADICTED`: the product, unit, indicator, and module match, but the extracted value differs from the claim.
- `UNCLEAR`: the evidence could not be confidently extracted or matched.
- `SOURCE_UNAVAILABLE`: the EPD page or linked PDF could not be retrieved.

`SUPPORTED` means agreement with the retrieved EPD snapshot only. It is not an EPD certification, an independent life-cycle assessment, or proof of the physical product's real-world environmental impact.

## Stored record

Each completed assessment stores its result, submitted claim, source page and PDF URLs, a SHA-256 digest of the rendered document text, extracted source values, and supporting quotes. Assessments are indexed by an incrementing ID and can be read through the contract's view methods.

Inputs and stored results may be public. Do not submit confidential documents or personal information.

## Development setup

The commands below use Python 3.13, which was used for local validation.

From the repository root, create and activate a virtual environment, then install the pinned development dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
