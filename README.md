# Azure Delivery Review

A small Python prototype for reviewing declared infrastructure delivery controls. It reads a JSON configuration and reports items that need review, including Terraform validation, plan review, short-lived authentication, access scope, approval, and recovery planning.

## Try it

From this directory, with Python 3:

```bash
python3 review.py example.json
python3 review.py example.json --format json
python3 -m unittest -v test_review.py
```

The example intentionally has missing controls; the review command returns exit code 1 when a control needs review, 0 when all six are declared, and 2 for invalid input.

## What it verifies

The prototype checks only whether each example JSON value is the boolean `true`. A declared control is **not independently verified**: it does not inspect Azure, Terraform, GitHub settings, permissions, or actual deployment evidence. It does not establish compliance or security.

Seven tests cover the review logic and CLI, including default text output, JSON reports, strict boolean handling, success and failure exit codes, and invalid input. A GitHub Actions workflow runs the tests on pushes and pull requests. Real policy integration and Azure deployment are not implemented.

## JSON reports for CI

Use `--format json` for a report containing `schema_version`, `review_type`, `independently_verified`, and a `findings` array. Each finding includes the control name, status, and recommendation. The report explicitly records that declarations are not independently verified.

Text remains the default. Both formats return 0 for all controls declared, 1 for missing controls, and 2 for invalid input. Invalid input produces an error on stderr and no report on stdout. CI callers should capture the exit code before processing the report because missing controls intentionally return 1.

## Engineering choices

- Local JSON input and the Python standard library keep the example easy to run without cloud credentials.
- A nonzero exit code makes missing declarations visible to callers; any future CI integration should distinguish declarations from independently verified controls.
- Example values are fictional. Never commit secrets, customer configurations, or private infrastructure details.

## Next steps

Build evidence-backed checks for selected GitHub or Terraform configuration, document CI results, and review limitations. This AI-assisted personal prototype is a learning and portfolio project.

