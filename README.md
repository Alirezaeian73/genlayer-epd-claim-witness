# EPD Claim Witness

An experimental, standalone GenLayer Intelligent Contract for checking whether one specific product carbon claim is supported by a public Environmental Product Declaration (EPD).

## The idea

A user records one product claim, such as a declared Global Warming Potential (GWP) value, together with the public EPD that is meant to support it.

The contract is designed to have GenLayer validators independently examine the document and return a bounded, structured assessment. Deterministic contract logic then records the result. The model does not decide whether a product is environmentally good or make a general sustainability judgment.

The proposed result categories are:

- `SUPPORTED`
- `CONTRADICTED`
- `UNCLEAR`
- `SOURCE_UNAVAILABLE`

The assessment is intended to consider the product identity, the reported indicator, life-cycle module, declared unit, and value. The exact rules will be finalized after checking what the GenLayer runtime can reliably retrieve and test.

## Why GenLayer

EPDs are public evidence, but relevant information may appear in tables and descriptive text rather than in a simple, consistent data field. The intended use of GenLayer is to let validators independently interpret that evidence, while contract code applies a narrow comparison rule and records the result.

If the contract can only store an answer supplied by a website or a single AI model, GenLayer would not add meaningful value. The implementation must put the consensus-critical assessment inside the Intelligent Contract.

## Planned first-version boundaries

The first version is intended to:

- assess one claim against one public EPD at a time;
- preserve each assessment as a public record;
- report uncertainty or unavailable evidence rather than silently treating it as a pass;
- avoid product rankings, broad environmental scores, payments, or a frontend application.

This contract will not certify an EPD, verify the scientific accuracy of a life-cycle assessment, prove the real-world footprint of a physical product, or replace professional review. A source URL or content digest can help identify the material examined, but cannot by itself prove that the source is truthful or authoritative.

Do not submit confidential documents or personal information. Contract inputs and stored results may be public.

## Project status

This repository currently contains an initial design only. The contract has not yet been implemented, linted, tested, or deployed. No live GenLayer result is claimed.

The design will be revised if source retrieval, consensus behavior, or testing shows that the proposed scope is not reliable.
