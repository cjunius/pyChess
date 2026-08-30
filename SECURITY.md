# Security Policy

## Supported versions

This project is pre-1.0 and moves fast. Only `main` receives fixes.

| Version | Supported |
|---------|-----------|
| `main`  | ✅        |
| tagged releases | latest only |

## Reporting a vulnerability

Please **do not open a public issue** for security problems.

Report privately via GitHub:
[**Open a security advisory**](https://github.com/cjunius/pyChess/security/advisories/new).

Include a description, reproduction steps, and the affected commit or version.
You can expect an acknowledgement within a few days. There is no bug-bounty
program.

## Scope

This is a chess engine that reads UCI commands on stdin and an optional Polyglot
opening-book file. Relevant concerns include malformed UCI / FEN input,
crafted opening-book files, and the `multiprocessing` shared-memory transposition
table. The bundled `opening_book/bookfish.bin` is third-party data — see
[opening_book/README.md](opening_book/README.md).
