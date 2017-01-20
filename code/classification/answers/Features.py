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