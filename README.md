# Azure Delivery Review
**An AI-assisted Python prototype by Rakesh Gorige · Platform & DevOps Engineering**

A small local CLI for reviewing **declared** infrastructure delivery controls. It reads a JSON configuration and reports items needing review: Terraform validation, plan review, short-lived authentication, access scope, approval, and recovery planning.

[Portfolio](https://github.com/rockygorge/RockyProject) · [GitHub profile](https://github.com/rockygorge)

## Try it

Requires Python 3. From this repository directory:

```bash
python3 review.py example.json
python3 review.py example.json --format json
python3 -m unittest -v test_review.py
```

The example intentionally omits controls. Exit code **0** means all six are declared, **1** indicates missing controls, and **2** indicates invalid input.

## Scope of verification

The tool checks only whether each example JSON field is the boolean `true`. It **does not independently verify** Azure, Terraform, GitHub, permissions, deployment evidence, compliance, or security settings.

Seven tests cover the review logic and CLI, including text and JSON output, strict boolean handling, exit codes, and invalid input. GitHub Actions runs those tests on pushes and pull requests.

## JSON reporting

Use `--format json` to produce a report containing `schema_version`, `review_type`, `independently_verified`, and a `findings` array. Each finding includes control name, status, and recommendation. The report marks the declarations as **not independently verified**.

Text output is the default. Missing controls intentionally return exit code 1, so CI consumers should capture exit codes before parsing reports. Invalid input writes an error to stderr rather than a report to stdout.

## Engineering choices

- Python standard library and local JSON minimize setup and avoid cloud credentials.
- Machine-readable output and stable exit codes support future CI integration.
- Fictional examples avoid storing secrets and customer infrastructure information.

## Next steps

Implement evidence-backed checks for selected GitHub or Terraform settings and document proof, CI behavior, and limitations. This remains a **personal learning and portfolio prototype**, not a production security or compliance system.

**Maintainer: Rakesh Gorige**
