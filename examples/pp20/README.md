# PP20 example

The PP20 **intake record** lives at [`projects/pp20/problem.yaml`](../../projects/pp20/problem.yaml).

The PP20 **artefacts have moved** to:

```text
tests/fixtures/pp20/artefacts/
```

They were moved out of `examples/` deliberately. They are hand-written test
data used to exercise the artefact gate — not system output, and not input to
any pipeline. Nothing in this repository generates them. See
[`tests/fixtures/README.md`](../../tests/fixtures/README.md).

To compile the PP20 intake into an artefact plan:

```bash
PYTHONPATH=src python -m throughline.cli plan projects/pp20/problem.yaml --out /tmp/pp20-plan
```
