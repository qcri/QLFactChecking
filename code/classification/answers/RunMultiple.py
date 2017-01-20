import RunCV

RUNS = [
    ['CATEGORIES-incl', 'CATEGORIES-incl'],
    ['QUALITY-incl', 'QUALITY-incl'],
    ['TROLLNESS-incl', 'TROLLNESS-incl'],
    ['ACTIVITY-incl', 'ACTIVITY-incl'],
    ['CREDIBILITY-incl', 'CREDIBILITY-incl'],
    ['SENTIMENT-incl', 'SENTIMENT-incl'],
    ['GOOGLE_VEC-incl', 'GOOGLE_VEC-incl'],
    ['QL_VEC-incl', 'QL_VEC-incl'],
    ['SYNTAX_VEC-incl', 'SYNTAX_VEC-incl'],
    ['RANK_SAME_USER-incl', 'RANK_SAME_USER-incl'],
    ['VEC_COSINES_THREAD-incl', 'VEC_COSINES_THREAD-incl'],
    ['COSINES-incl', 'COSINES-incl'],
    ['CATEGORIES-excl', 'CATEGORIES-excl'],
    ['QUALITY-excl', 'QUALITY-excl'],
    ['TROLLNESS-excl', 'TROLLNESS-excl'],
    ['ACTIVITY-excl', 'ACTIVITY-excl'],
    ['CREDIBILITY-excl', 'CREDIBILITY-excl'],
    ['SENTIMENT-excl', 'SENTIMENT-excl'],
    ['GOOGLE_VEC-excl', 'GOOGLE_VEC-excl'],
    ['QL_VEC-excl', 'QL_VEC-excl'],
    ['SYNTAX_VEC-excl', 'SYNTAX_VEC-excl'],
    ['RANK_SAME_USER-excl', 'RANK_SAME_USER-excl'],
    ['VEC_COSINES_THREAD-excl', 'VEC_COSINES_THREAD-excl'],
    ['COSINES-excl', 'COSINES-excl'],
    ['all', 'all'],
]


RUNS_ = [
    ['all-negative', 'COSINES-incl'],
]

def main():
    print('RunMultiple.run_all')
    for run in RUNS:
        run_one(run)

def run_one(run):
    run_id = run[0]
    feats_index = run[1]

    print('Running ', run_id)
    RunCV.run(run_id, feats_index)


# Start here:
main()