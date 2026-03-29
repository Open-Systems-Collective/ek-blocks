# Open Knowledge Blocks (OKBs)

**Executable, profile-based compliance for trustworthy AI services.**

Open Knowledge Blocks (OKBs) are modular, machine-readable compliance units that encode regulatory obligations as RDF vocabularies and SHACL constraint shapes. Each block captures a specific set of legal requirements so that AI system providers can validate their evidence graphs automatically.

This repository is the community library of published OKB blocks. For the prototype validator, profile engine, and architecture documentation, see the main project:

- **Prototype**: [github.com/AasishKumarSharma/open-knowledge-blocks](https://github.com/AasishKumarSharma/open-knowledge-blocks)

## How Blocks Work

Every OKB follows a three-layer design:

1. **Schema** (`schema.ttl`): an RDF/OWL vocabulary that defines the classes and properties used to describe compliance evidence.
2. **Shapes** (`shapes.ttl`): SHACL constraint shapes that encode the regulatory "must" requirements. When validated against an evidence graph, violations map directly to unmet legal obligations.
3. **Tests** (`tests/`): conformant and non-conformant evidence graphs that serve as executable specifications.

A compliance **profile** composes one or more blocks into a complete validation suite for a given regulation or use case.

## Repository Structure

```
ek-blocks/
  README.md                     # This file
  validate_example.py           # Quick-start validation script
  kb_human_oversight/           # EU AI Act Article 14: Human Oversight
    schema.ttl                  #   RDF/OWL vocabulary
    shapes.ttl                  #   SHACL constraint shapes
    metadata.ttl                #   DCAT-AP metadata
    README.md                   #   Block documentation
    tests/
      conform/
        full_oversight.ttl      #   Passing evidence graph
      violate/
        no_override.ttl         #   Failing evidence graph
```

## Available Blocks

| Block | Regulation | Description |
|-------|-----------|-------------|
| [kb_human_oversight](kb_human_oversight/) | EU AI Act Art. 14 | Human oversight obligations for high-risk AI systems |

## Quick Start: Validate with pyshacl

Install dependencies:

```bash
pip install rdflib pyshacl
```

Run the included validation script:

```bash
python validate_example.py
```

Or validate manually:

```bash
# Validate a conformant evidence graph (should pass)
pyshacl -s kb_human_oversight/shapes.ttl \
        -e kb_human_oversight/schema.ttl \
        -df turtle \
        kb_human_oversight/tests/conform/full_oversight.ttl

# Validate a non-conformant evidence graph (should fail)
pyshacl -s kb_human_oversight/shapes.ttl \
        -e kb_human_oversight/schema.ttl \
        -df turtle \
        kb_human_oversight/tests/violate/no_override.ttl
```

## Contributing

New blocks are welcome. Each block should follow the canonical structure shown above and include both conformant and non-conformant test graphs. See any existing block for a template.

## License

CC-BY 4.0
