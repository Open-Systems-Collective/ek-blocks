# kb_human_oversight v1.0.0

Open Knowledge Block encoding human oversight obligations for high-risk AI systems under **EU AI Act Article 14**.

## Regulatory Source

EU Artificial Intelligence Act (Regulation (EU) 2024/1689), Article 14: Human Oversight.

## Obligations Encoded

This block encodes the following requirements from Article 14:

1. **Art. 14(1)**: High-risk AI systems shall be designed and developed so that they can be effectively overseen by natural persons.
2. **Art. 14(4)(a)**: Human operators must be provided with a description of the system's capabilities and limitations.
3. **Art. 14(4)(b)**: Human operators must be able to correctly interpret the system's output.
4. **Art. 14(4)(d)**: Human operators must be able to override or reverse AI decisions.
5. **Art. 14(4)(e)**: Human operators must be able to intervene or interrupt the system.

## Block Contents

| File | Purpose |
|------|---------|
| `schema.ttl` | RDF/OWL vocabulary: classes and properties for oversight evidence |
| `shapes.ttl` | SHACL constraint shapes: machine-checkable compliance rules |
| `metadata.ttl` | DCAT-AP dataset metadata |
| `tests/conform/full_oversight.ttl` | Evidence graph that passes all shapes |
| `tests/violate/no_override.ttl` | Evidence graph that fails: missing override capability |

## Profiles That Include This Block

This block is intended for inclusion in any compliance profile targeting high-risk AI systems under the EU AI Act. See the [Open Knowledge Blocks prototype](https://github.com/AasishKumarSharma/open-knowledge-blocks) for the profile composition mechanism.

## How to Validate

Using [pyshacl](https://github.com/RDFLib/pySHACL):

```bash
# Should pass (exit code 0)
pyshacl -s shapes.ttl -e schema.ttl -df turtle tests/conform/full_oversight.ttl

# Should fail (exit code 1) with one violation on OverrideRequiredShape
pyshacl -s shapes.ttl -e schema.ttl -df turtle tests/violate/no_override.ttl
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

ex:myDecision a ex:Decision ;
    ex:hasOversightRecord ex:rec1 ;
    ex:hasOverrideCapability ex:cap1 ;
    ex:hasSystemDescription ex:desc1 .

ex:rec1 a ex:HumanOversightRecord ;
    ex:oversightTimestamp "2026-01-01T00:00:00Z"^^xsd:dateTime ;
    ex:reviewerID "reviewer-001" ;
    ex:oversightOutcome "approved" .

ex:cap1 a ex:OverrideCapability ;
    ex:overrideMechanism "Manual override available" ;
    ex:overrideAvailable true .

ex:desc1 a ex:AISystemDescription ;
    ex:capabilityDescription "System capabilities documented" ;
    ex:limitationDescription "System limitations documented" .
```

## License

CC-BY 4.0
