`relwrite`
==========

`relwrite` relates strings to string via a grammar in the Chomsky hierarchy.

What does "relate" mean in this context?

*   Given a grammar and a string of terminals, it can _parse_ that string, and
    report if is in the language of the grammar or not.
*   Given a grammar and a nonterminal, it can _generate_ a string of terminals
    from them.

The relational engine in `relwrite` is a very general one, based on string rewriting.
There are therefore no restrictions on the input grammar -- it may be **regular**,
**context-free**, **context-sensitive**, or **unrestricted**.  If the grammar is
ambiguous, then all possible parses (or generations) can be returned.

It should be understood that `relwrite` trades off performance and small
memory footprint in favour of generality, so in general usage, it works
best on small inputs.

There are, however, features intended to improve performance in the case of very
long derivations.  Specifying a search strategy enables a **beam search** algorithm
which aggressively focuses on derivations with a desired propery, e.g. a particular
minimum length.  This does sacrifice completeness however -- only a handful of all
the possible results will be returned.

The grammar must be provided in the form of a JSON file.  There are example
grammar files in the `eg/` directory of this repo.

### Example usage

Generate a string from a non-terminal in a grammar:

```
./bin/relwrite eg/recursive-grammar.json --start "<Sentence>" --max-derivations=1
```

Parse a string w.r.t. a grammar:

```
./bin/relwrite eg/recursive-grammar.json --parse --start "a penguin sees a penguin then sees a dog"
```

Generate a really long string from a non-terminal in a grammar, without running out
of memory and only taking a few hours of processor time:

```
./bin/relwrite eg/recursive-grammar.json --start "<Sentence>" --max-derivations=1 --strategy=expand --expand-until=3000
```

Parse a really long string from a non-terminal in a grammar, without running out
of memory and only taking a few hours of processor time.  This assumes the string
to be parsed is in JSON format in the file `xyz.json`.

```
./bin/relwrite eg/recursive-grammar.json --parse --start-set-file=xyz.json --max-derivations=1 --strategy=contract
```

### Detailed usage

Run `relwrite --help` for a description of all the possible command-line options.  Note that
these are somewhat provisional and subject to change.

### Notes

`relwrite` uses the term "derivation" as a generic term meaning "a parse or a generated utterance".
It also uses the term "utterance" to mean "any string of terminals and non-terminals".

### TODO (immediate)

*   `--output-file` to specify output filename
*   `--goal` to assert that a particular final utterance appears
*   Turn `complete` into a strategy that must be explicitly selected.

### TODO (aspirational)

Analyze the input grammar and classify it in the Chomsky hierarchy.

If the input grammar is context-free, use an algorithm such as Earley or CYK to
efficiently parse or generate it.

Allow strategies to be defined richly, perhaps in JSON files, and let
them configure parameters like beam width, max rewrites per utterance, etc.

For max rewrites per utterance, allow them to be taken from random
points (or at least from a randomly-chosen start point) in the utterace.

Support random search.  For `contract` strategy, it should be sufficient to
identify the subset of the next states that is sufficiently contracting
(this is not a "beam width" so much as a "pre-filter"),
then select a single instance from it at random (beam width of 1).
