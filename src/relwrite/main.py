from argparse import ArgumentParser
import json

from .engine import derive


def main(args):
    argparser = ArgumentParser()

    # NOTE: these options are provisional and will change

    argparser.add_argument(
        'grammar_filename', metavar='FILENAME', type=str,
        help='JSON file containing the grammar to use'
    )
    argparser.add_argument(
        "--parse", action="store_true", default=False,
        help="Process rules from right to left"
    )

    argparser.add_argument(
        "--verbose", action="store_true", default=False,
        help="Display some vital statistics while processing"
    )
    argparser.add_argument(
        "--save-snapshots-every", metavar='COUNT', type=int, default=None,
        help="If given, each time this many generations have passed, "
             "save a copy of the working set of utterances to a JSON "
             "file"
    )

    argparser.add_argument(
        "--start", metavar='UTTERANCE', type=str, default=None,
        help="A single utterance to use as "
             "the starting point of the derivation"
    )
    argparser.add_argument(
        "--start-set-file", metavar='FILENAME', type=str, default=None,
        help="Use the set of utterances in this JSON file as "
             "the starting point of the derivation"
    )

    argparser.add_argument(
        "--max-derivations", metavar='COUNT', type=int, default=None,
        help="The maximum number of derivations to produce "
             "(default: no limit)"
    )
    argparser.add_argument(
        "--max-rewrites-per-utterance", metavar='COUNT', type=int, default=None,
        help="If given, limits the number of times a pattern can rewrite "
             "any particular utterance during a single sweep "
             "(default: no limit, unless beam search is applied, in which case 10)"
    )

    argparser.add_argument(
        "--strategy", metavar='STRATEGY', type=str, default=None,
        help="Will apply a particular strategy (`expand` or `contract`) "
             "under beam search"
    )
    argparser.add_argument(
        "--beam-width", metavar='SIZE', type=int, default=10,
        help="When traversing with a strategy, specify the beam width "
             "for the beam search"
    )
    argparser.add_argument(
        "--expand-until", metavar='SIZE', type=int, default=None,
        help="When using the `expand` strategy, specifies that the "
             "resulting derivations must be at least this long"
    )

    options = argparser.parse_args(args)

    with open(options.grammar_filename, 'r') as f:
        grammar = json.loads(f.read())

    rules = [(tuple(lhs), tuple(rhs)) for [lhs, rhs] in grammar]

    if options.parse:
        rules = [(b,a) for (a,b) in rules]

    if options.start:
        working_utterances = [tuple(options.start.split())]
    elif options.start_set_file:
        with open(options.start_set_file, 'r') as f:
            working_utterances = json.loads(f.read())
        working_utterances = [tuple(x) for x in working_utterances]
    else:
        print("No start set given, please supply --start or --start-set-file")
        working_utterances = []

    max_matches = options.max_rewrites_per_utterance
    if options.strategy:
        max_matches = max_matches or 10

    result = derive(
        rules,
        working_utterances,
        max_derivations=options.max_derivations,
        max_matches=max_matches,
        verbose=options.verbose,
        save_snapshots_every=options.save_snapshots_every,
        strategy=options.strategy,
        expand_until=options.expand_until,
        beam_width=options.beam_width,
    )

    with open('out.json', 'w') as f:
        f.write(json.dumps(result, indent=4))


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
