import RunCV

RUNS = [
    # ['ARTICLES_SUPPORTS_BESTMATCH-incl', 'ARTICLES_SUPPORTS_BESTMATCH-incl'], #article supports
    # ['ARTICLES_SUPPORTS_ENTIREC-incl', 'ARTICLES_SUPPORTS_ENTIREC-incl'], #article supports
    # ['ARTICLES_SUPPORTS_All-incl', 'ARTICLES_SUPPORTS_All-incl'], #article supports
    ['ARTICLES_SUPPORTS_BESTMATCH_LEVENSHTEIN-incl', 'ARTICLES_SUPPORTS_BESTMATCH_LEVENSHTEIN-incl'], #article supports
    # ['ARTICLES_SUPPORTS_ENTIREC_LEVENSHTEIN-incl', 'ARTICLES_SUPPORTS_ENTIREC_LEVENSHTEIN-incl'], #article supports
    # ['ARTICLES_SUPPORTS_All_LEVENSHTEIN-incl', 'ARTICLES_SUPPORTS_All_LEVENSHTEIN-incl'], #article supports
    # ['LINGF_BIAS_LEX-incl', 'LINGF_BIAS_LEX-incl'], #linguistic Features
    # ['LINGF_HEDGES-incl', 'LINGF_HEDGES-incl'], #linguistic Features
    # ['LINGF_IMPLICATIVES-incl', 'LINGF_IMPLICATIVES-incl'], #linguistic Features
    # ['LINGF_ASSERTIVES-incl', 'LINGF_ASSERTIVES-incl'], #linguistic Features
    # ['LINGF_FACTIVES-incl', 'LINGF_FACTIVES-incl'], #linguistic Features
    # ['LINGF_REPORT_VERBS-incl', 'LINGF_REPORT_VERBS-incl'], #linguistic Features
    # ['LINGF_All_BIAS_LEX-incl', 'LINGF_All_BIAS_LEX-incl'], #linguistic Features
    # ['LINGF_STRONGSubj-incl', 'LINGF_STRONGSubj-incl'], #linguistic Features
    # ['LINGF_WEAKSubj-incl', 'LINGF_WEAKSubj-incl'], #linguistic Features
    # ['LINGF_NEGATIVES-incl', 'LINGF_NEGATIVES-incl'], #linguistic Features
    # ['LINGF_POSITIVES-incl', 'LINGF_POSITIVES-incl'], #linguistic Features
    # ['LINGF_MODALS-incl', 'LINGF_MODALS-incl'], #linguistic Features
    # ['LINGF_NEGATIONS-incl', 'LINGF_NEGATIONS-incl'], #linguistic Features
    ['LINGF_All-incl', 'LINGF_All-incl'], #linguistic Features
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
    # ['CATEGORIES-excl', 'CATEGORIES-excl'],
    # ['QUALITY-excl', 'QUALITY-excl'],
    # ['TROLLNESS-excl', 'TROLLNESS-excl'],
    # ['ACTIVITY-excl', 'ACTIVITY-excl'],
    # ['CREDIBILITY-excl', 'CREDIBILITY-excl'],
    # ['SENTIMENT-excl', 'SENTIMENT-excl'],
    # ['GOOGLE_VEC-excl', 'GOOGLE_VEC-excl'],
    # ['QL_VEC-excl', 'QL_VEC-excl'],
    # ['SYNTAX_VEC-excl', 'SYNTAX_VEC-excl'],
    # ['RANK_SAME_USER-excl', 'RANK_SAME_USER-excl'],
    # ['VEC_COSINES_THREAD-excl', 'VEC_COSINES_THREAD-excl'],
    # ['COSINES-excl', 'COSINES-excl'],
    # ['LINGF_All-excl', 'LINGF_All-excl'], #excluding all linguistic Features
    # ['LINGF_All_BIAS_ADDED_TO_OTHERS', 'LINGF_All_BIAS_ADDED_TO_OTHERS'], #including all linguistic bias Features
    #["IRF_Bing_snippets-incl", "IRF_Bing_snippets-incl"],
    #["IRF_Google_snippets-incl", "IRF_Google_snippets-incl"],
    #["IRF_ALL_snippets-incl", "IRF_ALL_snippets-incl"],
    #["IRF_Bing_snippets_qataronly-incl", "IRF_Bing_snippets_qataronly-incl"],
    #["IRF_Google_snippets_qataronly-incl", "IRF_Google_snippets_qataronly-incl"],
    #["IRF_ALL_snippets_qataronly-incl", "IRF_ALL_snippets_qataronly-incl"],
    #["IRF_Bing_webpage_qataronly-incl", "IRF_Bing_webpage_qataronly-incl"],
    #["IRF_Google_webpage_qataronly-incl", "IRF_Google_webpage_qataronly-incl"],
    #["IRF_ALL_webpages_qataronly-incl", "IRF_ALL_webpages_qataronly-incl"],
    #["IRF_ALL_Google_qataronly-incl", "IRF_ALL_Google_qataronly-incl"],
    #["IRF_ALL_Bing_qataronly-incl", "IRF_ALL_Bing_qataronly-incl"],
    #["IRF_ALL_qataronly-incl", "IRF_ALL_qataronly-incl"],
    #["IRF_Bing_snippets_qataronly_splitted-incl", "IRF_Bing_snippets_qataronly_splitted-incl"],
    #["IRF_Google_snippets_qataronly_splitted-incl", "IRF_Google_snippets_qataronly_splitted-incl"],
    #["IRF_ALL_snippets_qataronly_splitted-incl", "IRF_ALL_snippets_qataronly_splitted-incl"],
    ["IRF_Bing_webpage_qataronly_splitted-incl", "IRF_Bing_webpage_qataronly_splitted-incl"],
    #["IRF_Google_webpage_qataronly_splitted-incl", "IRF_Google_webpage_qataronly_splitted-incl"],
    #["IRF_ALL_webpages_qataronly_splitted-incl", "IRF_ALL_webpages_qataronly_splitted-incl"],
    #["IRF_ALL_Google_qataronly_splitted-incl", "IRF_ALL_Google_qataronly_splitted-incl"],
    #["IRF_ALL_Bing_qataronly_splitted-incl", "IRF_ALL_Bing_qataronly_splitted-incl"],
    #["IRF_ALL_qataronly_splitted-incl", "IRF_ALL_qataronly_splitted-incl"],
    #["IRF_Bing_snippets_qataronly_splitted_others_bulk-incl", "IRF_Bing_snippets_qataronly_splitted_others_bulk-incl"],
    #["IRF_Google_snippets_qataronly_splitted_others_bulk-incl", "IRF_Google_snippets_qataronly_splitted_others_bulk-incl"],
    #["IRF_ALL_snippets_qataronly_splitted_others_bulk-incl", "IRF_ALL_snippets_qataronly_splitted_others_bulk-incl"],
    #["IRF_Bing_webpage_qataronly_splitted_others_bulk-incl", "IRF_Bing_webpage_qataronly_splitted_others_bulk-incl"],
    #["IRF_Google_webpage_qataronly_splitted_others_bulk-incl", "IRF_Google_webpage_qataronly_splitted_others_bulk-incl"],
    #["IRF_ALL_webpages_qataronly_splitted_others_bulk-incl", "IRF_ALL_webpages_qataronly_splitted_others_bulk-incl"],
    #["IRF_ALL_Google_qataronly_splitted_others_bulk-incl", "IRF_ALL_Google_qataronly_splitted_others_bulk-incl"],
    #["IRF_ALL_Bing_qataronly_splitted_others_bulk-incl", "IRF_ALL_Bing_qataronly_splitted_others_bulk-incl"],
    #["IRF_ALL_qataronly_splitted_others_bulk-incl", "IRF_ALL_qataronly_splitted_others_bulk-incl"],
    #["IRF_Bing_snippets_splitted-incl", "IRF_Bing_snippets_splitted-incl"],
    #["IRF_Google_snippets_splitted-incl", "IRF_Google_snippets_splitted-incl"],
    #["IRF_ALL_snippets_splitted-incl", "IRF_ALL_snippets_splitted-incl"],
    #["IRF_Bing_webpage_splitted-incl", "IRF_Bing_webpage_splitted-incl"],
    #["IRF_Google_webpage_splitted-incl", "IRF_Google_webpage_splitted-incl"],
    #["IRF_ALL_webpages_splitted-incl", "IRF_ALL_webpages_splitted-incl"],
    #["IRF_ALL_Google_splitted-incl", "IRF_ALL_Google_splitted-incl"],
    #["IRF_ALL_Bing_splitted-incl", "IRF_ALL_Bing_splitted-incl"],
    #["IRF_ALL_splitted-incl", "IRF_ALL_splitted-incl"]

    #["IRF_ALL_Bing_qataronly-incl", "IRF_ALL_Bing_qataronly-incl"],
    # ["IRF_ALL_webpages_qataronly_splitted-incl", "IRF_ALL_webpages_qataronly_splitted-incl"],
    # ["IRF_Bing_webpage_splitted-incl", "IRF_Bing_webpage_splitted-incl"],
    # ["IRF_ALL_Google_qataronly_splitted_others_bulk-incl", "IRF_ALL_Google_qataronly_splitted_others_bulk-incl"],
    # ["IRF_Google_snippets_qataronly_splitted_others_bulk-incl", "IRF_Google_snippets_qataronly_splitted_others_bulk-incl"],
    # ["IRF_ALL-incl", "IRF_ALL-incl"],

    # ["IRFeatures-excl", "IRFeatures-excl"],
    # ['all', 'all'],
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