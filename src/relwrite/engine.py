def generate(rules, working_utterances, max_matches=None):
    """Note that an "utterance" can be any mix of terminals and non-terminals.
    The "final utterances" will consist of only one or the other.
    """
    new_working_utterances = set()
    final_utterances = set()
    for utterance in working_utterances:
        num_rewrites_of_this_utterance = 0
        for (pattern, replacement) in rules:
            indices = get_match_indices(utterance, pattern, max_matches=max_matches)
            for index in indices:
                new_utterance = replace_at_index(
                    utterance, pattern, replacement, index
                )
                new_working_utterances.add(new_utterance)
                num_rewrites_of_this_utterance += 1
        if num_rewrites_of_this_utterance == 0:
            final_utterances.add(utterance)

    return new_working_utterances, final_utterances


def get_match_indices(utterance, pattern, max_matches=None):
    length = len(pattern)
    matches = []
    for index, _ in enumerate(utterance):
        if pattern == utterance[index:index + length]:
            matches.append(index)
        if max_matches and len(matches) >= max_matches:
            break
    return matches


def replace_at_index(utterance, pattern, replacement, index):
    length = len(pattern)
    new_utterance = list(utterance)
    new_utterance[index:index + length] = replacement
    return tuple(new_utterance)


def derive(rules, working_utterances, max_derivations=None, max_matches=None, verbose=False, strategy=None, expand_until=None, beam_width=10):
    final_utterances = None
    collected_utterances = []
    num_derivations = 0

    def score_expansion(u):
        return 0 - len(u)

    def score_contraction(u):
        return len(u)

    while working_utterances:

        length = len(working_utterances)
        lengths = [len(u) for u in working_utterances]
        min_length = min(lengths)
        if verbose:
            print('{} working utterances, min length = {}'.format(
                length, min_length
            ))
        if strategy == 'expansion' and min_length >= (expand_until or 0):
            if verbose:
                print('Reached {} threshold'.format(expand_until))
            strategy = 'contraction'

        working_utterances, final_utterances = generate(rules, working_utterances, max_matches=max_matches)

        # beam search: sort by score and trim before continuing
        if strategy:
            scoring_function = score_contraction if strategy == 'contraction' else score_expansion
            working_utterances = sorted(working_utterances, key=scoring_function)[:beam_width]

        for utterance in final_utterances:
            print(' '.join(utterance))
            collected_utterances.append(utterance)
            num_derivations += 1
            if max_derivations and num_derivations >= max_derivations:
                working_utterances = []
                break

    return collected_utterances
