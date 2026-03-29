#!/usr/bin/env python3
"""
Validate OKB test cases against their SHACL shapes.

Covers:
    - kb_human_oversight
    - kb_clinical_safety

Requirements:
    pip install rdflib pyshacl
"""

import sys
from pathlib import Path

from rdflib import Graph
from pyshacl import validate


def load_graph(path: Path) -> Graph:
    g = Graph()
    g.parse(str(path), format="turtle")
    return g


def run_block(block_name: str, block_dir: Path, test_cases: list) -> bool:
    print("=" * 70)
    print(f"OKB Validator: {block_name}")
    print("=" * 70)

    shapes_graph = load_graph(block_dir / "shapes.ttl")
    ont_graph = load_graph(block_dir / "schema.ttl")

    all_passed = True

    for case in test_cases:
        print(f"\nTest: {case['label']}")
        print("-" * 50)

        data_graph = load_graph(case["file"])

        conforms, results_graph, results_text = validate(
            data_graph,
            shacl_graph=shapes_graph,
            ont_graph=ont_graph,
            inference="none",
            abort_on_first=False,
        )

        if conforms == case["expect_conform"]:
            status = "OK"
        else:
            status = "UNEXPECTED"
            all_passed = False

        print(f"  Conforms : {conforms}")
        print(f"  Expected : {case['expect_conform']}")
        print(f"  Status   : {status}")

        if not conforms:
            print(f"  Violations:")
            for line in results_text.strip().splitlines():
                print(f"    {line}")

    return all_passed


def main() -> int:
    root = Path(__file__).resolve().parent

    # ---- kb_human_oversight ------------------------------------------------

    ho_dir = root / "kb_human_oversight"
    ho_cases = [
        {
            "label": "conform/full_oversight.ttl  (expect: PASS)",
            "file": ho_dir / "tests" / "conform" / "full_oversight.ttl",
            "expect_conform": True,
        },
        {
            "label": "violate/no_override.ttl     (expect: FAIL)",
            "file": ho_dir / "tests" / "violate" / "no_override.ttl",
            "expect_conform": False,
        },
    ]

    # ---- kb_clinical_safety ------------------------------------------------

    cs_dir = root / "kb_clinical_safety"
    cs_cases = [
        {
            "label": "conform/full_clinical.ttl   (expect: PASS)",
            "file": cs_dir / "tests" / "conform" / "full_clinical.ttl",
            "expect_conform": True,
        },
        {
            "label": "violate/no_uncertainty.ttl   (expect: FAIL)",
            "file": cs_dir / "tests" / "violate" / "no_uncertainty.ttl",
            "expect_conform": False,
        },
    ]

    all_passed = True
    all_passed = run_block("kb_human_oversight", ho_dir, ho_cases) and all_passed

    print("\n")

    all_passed = run_block("kb_clinical_safety", cs_dir, cs_cases) and all_passed

    print("\n" + "=" * 70)
    if all_passed:
        print("All test cases produced expected results.")
        return 0
    else:
        print("Some test cases did not produce expected results.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
