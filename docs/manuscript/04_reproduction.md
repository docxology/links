# Reproduction and limitations

The experiment is encoded as a native regression test under `tests/unit/test_organizer_manuscript_fixture.py`. Its inputs are in `tests/fixtures/organizer_neutral.json`, whose SHA-256 digest is:

```text
151483fd2f5547b919d8b7bf62f16c0bfd2d3c0183f5860e12186ae40eabfccc
```

Run the test from the repository root using the development environment described in the documentation:

```sh
uv run --locked pytest -q tests/unit/test_organizer_manuscript_fixture.py
```

The tests exercise the production loader, categorizer, and serializer with explicit limits and a temporary output directory. The experiment assumes valid JSON records and a fixed keyword table. External collection, provider execution, and downstream document evaluation fall outside this study.
