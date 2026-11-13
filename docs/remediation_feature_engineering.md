# Sentinel AI — Remediation Feature Engineering

## Source variable

The source variable is CISA KEV `requiredAction`.

The dataset contains 1,768 records, 46 unique remediation
instruction texts and no missing values.

## Feature extraction methodology

Eight binary indicators were initially extracted using
case-insensitive keyword and regular-expression matching.

The indicators represent textual mentions in CISA instructions.
They do not establish that a remediation action was executed.

## Refined candidate features

1. action_apply_updates
2. action_apply_mitigations
3. action_discontinue_product
4. action_eol_eos
5. action_cisa_directive
6. action_exposure_assessment
7. action_forensic_investigation

All seven features have zero missing values.

## Extraction audit

The forensic/triage indicator was refined to include:
- forensic
- triage
- compromised
- investigation

It identifies 153 records (8.65%).

This feature represents textual references to forensic triage
or potential compromise, not confirmed forensic investigations.

## Redundancy analysis

The following indicators were examined:

- action_apply_mitigations and action_discontinue_product:
  770 records activate both; 7 activate only mitigations;
  27 activate only discontinuation.

- action_exposure_assessment and action_forensic_investigation:
  151 records activate both; 9 activate only exposure assessment;
  2 activate only forensic/triage.

- action_disconnect_product and action_eol_eos:
  All 62 disconnect records also activate EOL/EOS.
  An additional 21 records activate EOL/EOS without disconnect.

Therefore, action_disconnect_product was excluded from
the refined candidate feature set due to redundancy.

The original column remains in the working dataset for traceability.

## Feature coverage

- action_apply_updates: 918 (51.92%)
- action_apply_mitigations: 777 (43.95%)
- action_discontinue_product: 797 (45.08%)
- action_eol_eos: 83 (4.69%)
- action_cisa_directive: 493 (27.88%)
- action_exposure_assessment: 160 (9.05%)
- action_forensic_investigation: 153 (8.65%)

## Limitations

- Keyword extraction can produce false positives and false negatives.
- Multiple indicators can be active for one instruction.
- Correlation does not establish semantic equivalence.
- CISA instructions may describe alternative or conditional actions.
- Textual recommendations do not prove implementation or asset exposure.
- These features are candidates and require model-specific selection.

## Global overlap audit and final candidate selection

A global Spearman correlation audit identified substantial overlap
between several remediation indicators.

### Pairwise overlap findings

- `action_apply_mitigations` and `action_discontinue_product`:
  770 records activated both indicators, 7 only mitigations and
  27 only discontinuation. Both variables are retained.

- `action_exposure_assessment` and `action_forensic_investigation`:
  151 records activated both indicators, 9 only exposure assessment
  and 2 only forensic investigation. A combined indicator was created.

- `action_apply_updates` and `action_apply_mitigations`:
  only 2 records activated both indicators. Both variables are retained
  as distinct remediation strategies.

- `action_apply_updates` and `action_discontinue_product`:
  20 records activated both indicators. Both variables are retained.

- `action_cisa_directive` is a subset of `action_apply_mitigations`
  in this dataset: all 493 records activating the directive indicator
  also activate the mitigation indicator. It is excluded from the
  initial independent model candidate set but preserved for traceability.

### Combined feature

`action_security_assessment` is defined as the logical union of
`action_exposure_assessment` and `action_forensic_investigation`.

It identifies textual mentions of exposure assessment, forensic
investigation or triage. It does not establish that an investigation
was actually performed.

Validation confirmed exact equality with the original logical union.

### Initial remediation model candidates

- `action_apply_updates`
- `action_apply_mitigations`
- `action_discontinue_product`
- `action_eol_eos`
- `action_security_assessment`

The original indicators remain in the master dataset. Candidate selection
is provisional and must be evaluated within model-specific experiments.
