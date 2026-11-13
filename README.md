# CTF Fixtures

Investigate security concepts with reproducible local exercises.

## Quick start

Use Python 3.10 or newer. The CLI runs locally with the standard library. From the repository root, run:

```sh
python3 main.py example.json
```

The HTTP exercise compares each response’s status and length with a control. The sample identifies label B because its body is 140 bytes versus the 100-byte control.

## Input and output

| Input | Format | Output or purpose |
| --- | --- | --- |
| `http-oracle` | `control` pair and `responses` with `label`, `status`, `size` | Labels that differ from the control |
| `jwt-header` | `token` in three-segment JWT form | Unverified `alg` and `kid` metadata |
| `salted-sha256` | `salt`, `digest`, ordered `candidates` | First matching candidate, or `null` |

Results are JSON on stdout. Redirect to a file when you want to save the review.

## Interpreting results

Response differences can have several causes. JWT header fields are untrusted metadata. The hash exercise uses SHA-256 over UTF-8 `salt + candidate` for teaching; production password storage needs a dedicated password hashing scheme.

## Troubleshooting

- Use the included fixture first to confirm the command and working directory.
- Check the input path and required fields if the CLI exits with status 2.
- Keep real assessment exports and generated reports in your private workspace.

## Verify locally

```sh
python3 -m unittest discover -s tests -v
```
