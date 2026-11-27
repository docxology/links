# Reproducible Organization of Local URL Metadata

This software methods note documents the repository's [local metadata organizer](../../src/data/organize_links.py). It derives its observations from the [synthetic JSON fixture](../../tests/fixtures/organizer_neutral.json) and [native regression tests](../../tests/unit/test_organizer_manuscript_fixture.py).

1. [Abstract](00_abstract.md)
2. [Scope](01_context.md)
3. [Organization and serialization](02_local_contract.md)
4. [Fixture observations](03_fixture.md)
5. [Reproduction and limitations](04_reproduction.md)
6. [References](99_references.md)

The canonical bundle uses [config.yaml](config.yaml), [references.bib](references.bib), and the [LaTeX preamble](preamble.md). Render PDF and HTML with [docxology/template at 87704fe](https://github.com/docxology/template/tree/87704feae0a4490ef7dad9c931d268e8c30273c2). Register a clean checkout as `projects/working/links` in the Template workspace and run the stages from the Template root.

```sh
uv run python scripts/pipeline/stage_03_render.py --project working/links
uv run python scripts/pipeline/stage_04_validate.py --project working/links
```

Render in a disposable checkout. Template writes to project-level `output/`, which also contains retained workflow artifacts in the Links repository.
