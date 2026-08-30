# Opening book

`bookfish.bin` is an ~18 MB [Polyglot](http://hgm.nubati.net/book_format.html)
opening book (a "bookfish"-style book, i.e. derived from Stockfish analysis).
The engine reads it **read-only** for the opening: if the current position is in
the book it plays a weighted-random book move instead of searching.

## Overriding / disabling

Set `PYCHESS_BOOK` to point at a different `.bin`, or at a path that does not
exist to disable the book entirely (a missing book is not an error - the engine
just searches from move one).

```bash
PYCHESS_BOOK=/path/to/other.bin pychess
```

## Licensing

The book is bundled data, not part of the engine's source, and is provided for
convenience only. Polyglot books generated from engine analysis are widely
distributed as data; if you intend to redistribute this project commercially,
confirm the provenance of this file or swap in a book whose terms you are sure
of.

## Notes for maintainers

An 18 MB binary in git history is a wart. Options if it becomes a problem:
migrate to [Git LFS](https://git-lfs.com/), fetch the book on first run instead
of vendoring it, or make it a documented external download. It is already in
history, so shrinking that needs a coordinated rewrite - not worth doing
casually.
