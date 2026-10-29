# EPD Claim Witness

EPD Claim Witness is an experimental GenLayer Intelligent Contract for checking a specific building-product GWP claim against the product's public Environmental Product Declaration (EPD).

## What it checks

The current prototype accepts an International EPD System registration number, product name, declared unit, and claimed GWP-total value for life-cycle modules A1-A3.

The contract retrieves the official EPD page, follows its PDF link through a text-extraction service, and extracts the product, unit, indicator, module, value, and supporting quotes. Validators compare the extracted evidence, then deterministic contract logic compares the claim with the EPD result.

The implemented scope is limited to EPD-IES registration numbers and GWP-total for A1-A3.

## Consensus and source handling

The contract uses GenLayer's non-deterministic web and extraction calls. The official EPD page is retrieved directly. The PDF is converted to text through Jina Reader because direct PDF rendering in the GenLayer runtime failed during testing.

Validators use comparative evaluation to check agreement on the source and extracted facts. The contract then applies deterministic checks to the product name, declared unit, indicator, module, and numeric value.

The text-extraction service is a third-party dependency. Each assessment records the official page URL, official PDF URL, text retrieval URL, a digest of the rendered text, and evidence quotes.

## Assessment results

- `SUPPORTED`: the submitted product, unit, indicator, module, and value match the extracted EPD evidence.
- `CONTRADICTED`: the product, unit, indicator, and module match, but the extracted value differs from the claim.
- `UNCLEAR`: evidence could not be confidently extracted or matched.
- `SOURCE_UNAVAILABLE`: the source page or text-conversion path could not be retrieved.

`SUPPORTED` means agreement with one published EPD snapshot. It is not an EPD certification, an independent life-cycle assessment, or proof of the physical product's real-world environmental impact.

## Current live deployment

- Network: GenLayer Studio
- Contract: `0xDd1C070e0c052f2cA275e485e4FE7Ca688DF48CC`
- Deployment transaction: [0x7efc22ddb827d8fa292d576f5c38ed26e1bb4354f60f749e0f7c7b4b22b02eba](https://explorer-studio.genlayer.com/tx/0x7efc22ddb827d8fa292d576f5c38ed26e1bb4354f60f749e0f7c7b4b22b02eba)
- Live assessment transaction: [0x0f42f6cbd1fb6197690a8f06eb31a638ceae882524f56ede1c9bd36a3b511d6d](https://explorer-studio.genlayer.com/tx/0x0f42f6cbd1fb6197690a8f06eb31a638ceae882524f56ede1c9bd36a3b511d6d)
- Live result: `SUPPORTED`
- Assessed claim: `157` for `CLS Rck35 S4 XC2 D25 CEM III 42,5 N-LH/SR CAM`, declared unit `1 m3`
- Extracted EPD value: `1,57 E+02`, GWP-total, module A1-A3

This is one successful live assessment. It does not establish that every EPD PDF or every validator run will be available or agree.

## Development checks

Development dependencies are pinned in `requirements-dev.txt`. From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt

genvm-lint check contracts/epd_claim_witness.py
genvm-lint typecheck contracts/epd_claim_witness.py
pytest -q
```

The local prototype passed lint, typecheck, and eight Direct Mode tests. Those tests mock web retrieval and extraction. They do not replace live network testing.

With the pinned GenLayer test package, the Direct Mode loader required a local GenVM artifact-cache workaround in the development environment. A clean-machine test run has not yet been independently verified.

## Limitations and privacy

The prototype handles one GWP-total claim for modules A1-A3 at a time. Retrieval and extraction can fail or be ambiguous. A text digest helps identify the material processed but does not prove that the source or conversion service is truthful.

Inputs and stored assessment records may be public. Do not submit confidential documents or personal information.
