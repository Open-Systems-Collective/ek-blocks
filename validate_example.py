#!/usr/bin/env python3
"""
Validate the kb_human_oversight OKB test cases against its SHACL shapes.

Requirements:
    pip install rdflib pyshacl
"""

import sys
from pathlib import Path

from rdflib import Graph
from pyshacl import validate

BLOCK_DIR = Path(__file__).resolve().parent / "kb_human_oversight"

SHAPES_FILE = BLOCK_DIR / "shapes.ttl"
SCHEMA_FILE = BLOCK_DIR / "schema.ttl"

TEST_CASES = [
    {
        "label": "conform/full_oversight.ttl  (expect: PASS)",
        "file": BLOCK_DIR / "tests" / "conform" / "full_oversight.ttl",
        "expect_conform": True,
    },
    {
        "label": "violate/no_override.ttl     (expect: FAIL)",
        "file": BLOCK_DIR / "tests" / "violate" / "no_override.ttl",
        "expect_conform": False,
    },
]


def load_graph(path: Path) -> Graph:
    g = Graph()
    g.parse(str(path), format="turtle")
    return g


def main() -> int:
    print("=" * 70)
    print("OKB Validator: kb_human_oversight")
    print("=" * 70)

    shapes_graph = load_graph(SHAPES_FILE)
    ont_graph = load_graph(SCHEMA_FILE)

    all_passed = True

    for case in TEST_CASES:
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

    print("\n" + "=" * 70)
    if all_passed:
        print("All test cases produced expected results.")
        return 0
    else:
        print("Some test cases did not produce expected results.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
