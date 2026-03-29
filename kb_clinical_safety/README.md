# kb_clinical_safety v1.0.0

Open Knowledge Block encoding clinical safety obligations for AI-assisted oncology diagnosis and treatment recommendation systems under **EU MDR 2017/745**, **FDA Clinical Decision Support Guidance (2022)**, and **WHO Ethics and Governance of AI for Health (2021)**.

## Clinical Scenario

An AI system analyzes chest CT scans and recommends lung cancer diagnoses. This block ensures that every recommendation carries: (1) clinical evidence citations, (2) confidence/uncertainty scores, (3) training cohort documentation, and (4) a clinician review before the recommendation is acted upon.

## Regulatory Sources

- EU Medical Device Regulation (MDR) 2017/745, Annex XV: Clinical Evaluation requirements
- FDA Guidance on Clinical Decision Support Software (2022), Docket FDA-2022-D-1766
- WHO Ethics and Governance of Artificial Intelligence for Health (2021)

## Obligations Encoded

This block encodes the following requirements:

1. **MDR 2017/745 Annex XV**: Every AI diagnostic recommendation must reference clinical evidence with a source URI and evidence level.
2. **FDA CDS Guidance**: Every AI diagnostic output must include uncertainty or confidence metrics, specifying both the score and the method used.
3. **WHO 2021, Sec.3.4**: Training population demographics must be documented, including cohort size and a description of the population.
4. **MDR 2017/745 Art.14(3)**: Clinical assessment by a qualified professional is required before acting on any AI recommendation.

## Block Contents

| File | Purpose |
|------|---------|
| `schema.ttl` | RDF/OWL vocabulary: classes and properties for clinical safety evidence |
| `shapes.ttl` | SHACL constraint shapes: machine-checkable compliance rules |
| `metadata.ttl` | DCAT-AP dataset metadata |
| `tests/conform/full_clinical.ttl` | Evidence graph that passes all shapes |
| `tests/violate/no_uncertainty.ttl` | Evidence graph that fails: missing uncertainty report |

## Profiles That Include This Block

This block is intended for inclusion in any compliance profile targeting AI-assisted medical device software under EU MDR, FDA oversight, or WHO ethical guidelines. See the [Open Knowledge Blocks prototype](https://github.com/AasishKumarSharma/open-knowledge-blocks) for the profile composition mechanism.

## How to Validate

Using [pyshacl](https://github.com/RDFLib/pySHACL):

```bash
# Should pass (exit code 0)
pyshacl -s shapes.ttl -e schema.ttl -df turtle tests/conform/full_clinical.ttl

# Should fail (exit code 1) with one violation on UncertaintyRequiredShape
pyshacl -s shapes.ttl -e schema.ttl -df turtle tests/violate/no_uncertainty.ttl
```

Or use the included validation script from the repository root:

```bash
python validate_example.py
```

## Minimal Conformant Evidence

The smallest evidence graph that satisfies all shapes:

```turtle
@prefix ex:  <http://example.org/okb#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ex:myDiagnosis a ex:DiagnosticRecommendation ;
    ex:hasClinicalEvidence ex:ev1 ;
    ex:hasUncertaintyReport ex:unc1 ;
    ex:hasPatientCohort ex:coh1 ;
    ex:hasClinicalReview ex:rev1 .

ex:ev1 a ex:ClinicalEvidence ;
    ex:evidenceSource "https://example.org/guideline"^^xsd:anyURI ;
    ex:evidenceLevel "Level I" .

ex:unc1 a ex:UncertaintyReport ;
    ex:confidenceScore "0.90"^^xsd:decimal ;
    ex:uncertaintyMethod "Ensemble Variance" .

ex:coh1 a ex:PatientCohortDescription ;
    ex:cohortSize "10000"^^xsd:integer ;
    ex:cohortDescription "Adult population, age 40-80" .

ex:rev1 a ex:ClinicalReviewRecord ;
    ex:reviewerQualification "Board-certified oncologist" ;
    ex:reviewTimestamp "2026-01-01T00:00:00Z"^^xsd:dateTime ;
    ex:reviewDecision "confirmed" .
```

## License

CC-BY 4.0
