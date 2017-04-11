import csv, os, string

PREFIX1 = 'data/features/semeval2016-'
PREFIX2 = '-with-annotations-clear-true-false-only'

def features_CATEGORIES(set_name):
    return read_features(set_name, "text_only.tc.author_comment_categories")

def features_QUALITY(set_name):
    return read_features(set_name, "text_only.tc.past_comments_profile")

def features_TROLLNESS(set_name):
    return read_features(set_name, "text_only.tc.trollness")

def features_ACTIVITY(set_name):
    return read_features(set_name, "text_only.tc.ql_user_features_all_forum_stats")

def features_CREDIBILITY(set_name):
    return read_features(set_name, "credibility")

def features_SENTIMENT(set_name):
    return read_features(set_name, "text_only.tc.SaifMohammad-sentiment")

def features_GOOGLE_VEC(set_name):
    return read_features(set_name, "text_only.tc.word2vec.300d.vectors.all_tokens")

def features_QL_VEC(set_name):
    return read_features(set_name, "text_only.tc.todor-vectors.all_tokens")

def features_SYNTAX_VEC(set_name):
    return read_features(set_name, "text_only.tc.RNN_embeddings.txt")

def features_RANK_SAME_USER(set_name):
    return read_features(set_name, "text_only.tc.rank_and_same_user_features")

def features_VEC_COSINES_THREAD(set_name):
    return read_features(set_name, "text_only.tc.cosines_thread_vs_comment")

def features_COSINES(set_name):
    return read_features(set_name, "text_only.tc.cosines")


#article supports
def features_ARTICLES_SUPPORTS_QUERY_LEVENSHTEIN(set_name):
    return read_features(set_name, "text_only.tc.articles-supports-QUERY-levenshtein")

#article supports
def features_ARTICLES_SUPPORTS_QUERY(set_name):
    return read_features(set_name, "text_only.tc.articles-supports-QUERY")

#article supports
def features_ARTICLES_SUPPORTS_BESTMATCH(set_name):
    return read_features(set_name, "text_only.tc.articles-supports-bestMatch")

#article supports
def features_ARTICLES_SUPPORTS_ENTIREC(set_name):
    return read_features(set_name, "text_only.tc.articles-supports-entireC")

#article supports
def features_ARTICLES_SUPPORTS_BESTMATCH_LEVENSHTEIN(set_name):
    return read_features(set_name, "text_only.tc.articles-supports-bestMatch-levenshtein")

#article supports
def features_ARTICLES_SUPPORTS_ENTIREC_LEVENSHTEIN(set_name):
    return read_features(set_name, "text_only.tc.articles-supports-entireC-levenshtein")

#linguistic Features
def features_LINGF_BIAS_LEX(set_name):
    return read_features(set_name, "text_only.tc.linguisticFeatures-bias-lexicon")

#linguistic Features
def features_LINGF_HEDGES(set_name):
    return read_features(set_name, "text_only.tc.linguisticFeatures-hedges")

#linguistic Features
def features_LINGF_IMPLICATIVES(set_name):
    return read_features(set_name, "text_only.tc.linguisticFeatures-implicatives")

#linguistic Features
def features_LINGF_ASSERTIVES(set_name):
    return read_features(set_name, "text_only.tc.linguisticFeatures-assertives")

#linguistic Features
def features_LINGF_FACTIVES(set_name):
    return read_features(set_name, "text_only.tc.linguisticFeatures-factives")

#linguistic Features
def features_LINGF_REPORT_VERBS(set_name):
    return read_features(set_name, "text_only.tc.linguisticFeatures-report-verbs")

#linguistic Features
def features_LINGF_All_BIAS_LEX(set_name):
    return read_features(set_name, "text_only.tc.linguisticFeatures-all-bias-lexicons")

#linguistic Features
def features_LINGF_STRONGSubj(set_name):
    return read_features(set_name, "text_only.tc.linguisticFeatures-strongSubj")

#linguistic Features
def features_LINGF_WEAKSubj(set_name):
    return read_features(set_name, "text_only.tc.linguisticFeatures-weakSubj")

#linguistic Features
def features_LINGF_NEGATIVES(set_name):
    return read_features(set_name, "text_only.tc.linguisticFeatures-negative-words")

#linguistic Features
def features_LINGF_POSITIVES(set_name):
    return read_features(set_name, "text_only.tc.linguisticFeatures-positive-words")

#linguistic Features
def features_LINGF_MODALS(set_name):
    return read_features(set_name, "text_only.tc.linguisticFeatures-modals")

#linguistic Features
def features_LINGF_NEGATIONS(set_name):
    return read_features(set_name, "text_only.tc.linguisticFeatures-negations")

#linguistic Features
def features_LINGF_All(set_name):
    return read_features(set_name, "text_only.tc.linguisticFeatures-all-linguistic-features")

#linguistic Features
def features_LINGF_EXTENDED_MULTIWORDS(set_name):
    return read_features(set_name, "text_only.tc.linguisticFeatures-multiWords-biases")

#IR features
def features_IR_Bing_snippets(set_name):
    return read_features(set_name, "ir.bing_snippets")

#IR features
def features_IR_Google_snippets(set_name):
    return read_features(set_name, "ir.google_snippets")

#IR features
def features_IR_Bing_webpages(set_name):

    return read_features(set_name, "ir.bing_webpages")

#IR features
def features_IR_Google_webpages(set_name):
    return read_features(set_name, "ir.google_webpages")

#IR features
def features_IR_bing_snippets_qataronly(set_name):
    return read_features(set_name, "ir.bing_snippets_qataronly")

#IR features
def features_IR_google_snippets_qataronly(set_name):
    return read_features(set_name, "ir.google_snippets_qataronly")

#IR features
def features_IR_bing_webpages_qataronly(set_name):

    return read_features(set_name, "ir.bing_webpages_qataronly")

#IR features
def features_IR_google_webpages_qataronly(set_name):
    return read_features(set_name, "ir.google_webpages_qataronly")

#IR features
def features_IR_bing_snippets_qataronly_splited(set_name):
    return read_features(set_name, "ir.bing_snippets_qataronly_splited")

#IR features
def features_IR_google_snippets_qataronly_splited(set_name):
    return read_features(set_name, "ir.google_snippets_qataronly_splited")

#IR features
def features_IR_bing_webpages_qataronly_splited(set_name):
    return read_features(set_name, "ir.bing_webpages_qataronly_splited")

#IR features
def features_IR_google_webpages_qataronly_splited(set_name):
    return read_features(set_name, "ir.google_webpages_qataronly_splited")

#IR features
def features_IR_bing_snippets_qatar_splited_others_bulk(set_name):
    return read_features(set_name, "ir.bing_snippets_qatar_splited_others_bulk")

#IR features
def features_IR_google_snippets_qatar_splited_others_bulk(set_name):
    return read_features(set_name, "ir.google_snippets_qatar_splited_others_bulk")

#IR features
def features_IR_bing_webpages_qatar_splited_others_bulk(set_name):
    return read_features(set_name, "ir.bing_webpages_qatar_splited_others_bulk")

#IR features
def features_IR_google_webpages_qatar_splited_others_bulk(set_name):
    return read_features(set_name, "ir.google_webpages_qatar_splited_others_bulk")

#IR features
def features_IR_bing_snippets_splited(set_name):
    return read_features(set_name, "ir.bing_snippets_splited")

#IR features
def features_IR_google_snippets_splited(set_name):
    return read_features(set_name, "ir.google_snippets_splited")

#IR features
def features_IR_bing_webpages_splited(set_name):
    return read_features(set_name, "ir.bing_webpages_splited")

#IR features
#def features_IR_google_webpages_splited(set_name):
#    return read_features(set_name, "ir.google_webpages_splited")
#IR features
def features_IR_QL_only(set_name):
    return read_features(set_name, "ir.IR_QL_Only_Google_snippets")

def features_IR_QL_only_reputed(set_name):
    return read_features(set_name, "ir.IR_QL_Only_Google_snippets_reputed_only")

def features_IR_QL_split(set_name):
    return read_features(set_name, "ir.IR_QL_Only_Google_snippets_split")

def features_IR_QL_only_withPages_reputed(set_name):
    return read_features(set_name, "ir.IR_QL_Only_Google_all_reputed_only")

def features_IR_QL_withPages_split(set_name):
    return read_features(set_name, "ir.IR_QL_Only_Google_all_split")


def features_IR_External(set_name):
    return read_features(set_name, "ir.IR_External_google_snippets")

def read_features(set_name, suffix):
    path = ''
    file = string.Template("../../../$prefix1$set$prefix2.xml.tab_format.$suffix")
    path = file.substitute(prefix1=PREFIX1, prefix2=PREFIX2, set=set_name, suffix=suffix)
    return read_features_from_file(path)

def read_features_from_file(file_path):
    print('Reading features from file: ', file_path)
    features = {}
    key = ''
    value_array = []
    with open(file_path,encoding="utf8") as csvfile:
        csvreader = csv.reader(csvfile, delimiter='\t')
        for row in csvreader:
            for index,value in enumerate(row):
                if index == 0:
                    if len(key) > 0:
                        features[key] = value_array
                    key = value
                    value_array = []
                else:
                    # in some of the files, the values are separated with space instead of a tab
                    if value.find(' ') > -1: 
                        values = value.split(' ')
                        for val in values:
                            if len(val.strip()) > 0:
                                value_array.append(float(val.strip()))
                    else:
                        value_array.append(float(value))
    if len(key) > 0:
        features[key] = value_array
    return features

def add_features(features_map, new_features_map):
    for key,value in new_features_map.items():
        if not key in features_map.keys():
            features_map[key] = []
        features_map[key].extend(value)
    return features_map

def add_thread_features(features_map, new_features_map):
    for keym,value in new_features_map.items():
        for i in range(1,11):
            # Putting all possible values in the feature map.
            # The non-existing ones will be skipped when the features are run
            key = keym + '_C' + str(i)
            if not key in features_map.keys():
                features_map[key] = []
            features_map[key].extend(value)
    return features_map