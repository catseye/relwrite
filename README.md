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
memory footprint in favour of generality.  There is, however, a feature to improve
the performance in the case of very long derivations.  Specifying a search strategies
enables a **beam search** algorithm which aggressively focuses on derivations with a
desirable character, e.g. a particular minimum length.

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

Generate a really long string from a non-terminal in a grammar:

(TK)

### Notes

`relwrite` uses the term "derivation" as a generic term meaning "parse or generation".

`relwrite` also uses the term "utterance" to mean "any string of terminals and non-terminals".

### TODO

*   specify output filename
*   try heuristic for contraction phase: highest proportion of terminals
