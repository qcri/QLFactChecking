import Features

def read_feature_set(set_name, feat_index):
    features_map = {}

    if feat_index == 'CATEGORIES-incl':
        features_map = Features.add_features(features_map, Features.features_CATEGORIES(set_name))
    if feat_index == 'QUALITY-incl':
        features_map = Features.add_features(features_map, Features.features_QUALITY(set_name))
    if feat_index == 'TROLLNESS-incl':
        features_map = Features.add_features(features_map, Features.features_TROLLNESS(set_name))
    if feat_index == 'ACTIVITY-incl':
        features_map = Features.add_features(features_map, Features.features_ACTIVITY(set_name))
    if feat_index == 'CREDIBILITY-incl':
        features_map = Features.add_features(features_map, Features.features_CREDIBILITY(set_name))
    if feat_index == 'SENTIMENT-incl':
        features_map = Features.add_features(features_map, Features.features_SENTIMENT(set_name))
    if feat_index == 'GOOGLE_VEC-incl':
        features_map = Features.add_features(features_map, Features.features_GOOGLE_VEC(set_name))
    if feat_index == 'QL_VEC-incl':
        features_map = Features.add_features(features_map, Features.features_QL_VEC(set_name))
    if feat_index == 'SYNTAX_VEC-incl':
        features_map = Features.add_features(features_map, Features.features_SYNTAX_VEC(set_name))
    if feat_index == 'RANK_SAME_USER-incl':
        features_map = Features.add_features(features_map, Features.features_RANK_SAME_USER(set_name))
    if feat_index == 'VEC_COSINES_THREAD-incl':
        features_map = Features.add_features(features_map, Features.features_VEC_COSINES_THREAD(set_name))
    if feat_index == 'COSINES-incl':
        features_map = Features.add_features(features_map, Features.features_COSINES(set_name))
    if feat_index == 'all':
        features_map = Features.add_features(features_map, Features.features_CATEGORIES(set_name))
        features_map = Features.add_features(features_map, Features.features_QUALITY(set_name))
        features_map = Features.add_features(features_map, Features.features_TROLLNESS(set_name))
        features_map = Features.add_features(features_map, Features.features_ACTIVITY(set_name))
        features_map = Features.add_features(features_map, Features.features_CREDIBILITY(set_name))
        features_map = Features.add_features(features_map, Features.features_SENTIMENT(set_name))
        features_map = Features.add_features(features_map, Features.features_GOOGLE_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_QL_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_SYNTAX_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_RANK_SAME_USER(set_name))
        features_map = Features.add_features(features_map, Features.features_VEC_COSINES_THREAD(set_name))
        features_map = Features.add_features(features_map, Features.features_COSINES(set_name))
    if feat_index == 'CATEGORIES-excl':
        #features_map = Features.add_features(features_map, Features.features_CATEGORIES(set_name))
        features_map = Features.add_features(features_map, Features.features_QUALITY(set_name))
        features_map = Features.add_features(features_map, Features.features_TROLLNESS(set_name))
        features_map = Features.add_features(features_map, Features.features_ACTIVITY(set_name))
        features_map = Features.add_features(features_map, Features.features_CREDIBILITY(set_name))
        features_map = Features.add_features(features_map, Features.features_SENTIMENT(set_name))
        features_map = Features.add_features(features_map, Features.features_GOOGLE_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_QL_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_SYNTAX_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_RANK_SAME_USER(set_name))
        features_map = Features.add_features(features_map, Features.features_VEC_COSINES_THREAD(set_name))
        features_map = Features.add_features(features_map, Features.features_COSINES(set_name))
    if feat_index == 'QUALITY-excl':
        features_map = Features.add_features(features_map, Features.features_CATEGORIES(set_name))
        #features_map = Features.add_features(features_map, Features.features_QUALITY(set_name))
        features_map = Features.add_features(features_map, Features.features_TROLLNESS(set_name))
        features_map = Features.add_features(features_map, Features.features_ACTIVITY(set_name))
        features_map = Features.add_features(features_map, Features.features_CREDIBILITY(set_name))
        features_map = Features.add_features(features_map, Features.features_SENTIMENT(set_name))
        features_map = Features.add_features(features_map, Features.features_GOOGLE_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_QL_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_SYNTAX_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_RANK_SAME_USER(set_name))
        features_map = Features.add_features(features_map, Features.features_VEC_COSINES_THREAD(set_name))
        features_map = Features.add_features(features_map, Features.features_COSINES(set_name))
    if feat_index == 'TROLLNESS-excl':
        features_map = Features.add_features(features_map, Features.features_CATEGORIES(set_name))
        features_map = Features.add_features(features_map, Features.features_QUALITY(set_name))
        #features_map = Features.add_features(features_map, Features.features_TROLLNESS(set_name))
        features_map = Features.add_features(features_map, Features.features_ACTIVITY(set_name))
        features_map = Features.add_features(features_map, Features.features_CREDIBILITY(set_name))
        features_map = Features.add_features(features_map, Features.features_SENTIMENT(set_name))
        features_map = Features.add_features(features_map, Features.features_GOOGLE_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_QL_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_SYNTAX_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_RANK_SAME_USER(set_name))
        features_map = Features.add_features(features_map, Features.features_VEC_COSINES_THREAD(set_name))
        features_map = Features.add_features(features_map, Features.features_COSINES(set_name))
    if feat_index == 'ACTIVITY-excl':
        features_map = Features.add_features(features_map, Features.features_CATEGORIES(set_name))
        features_map = Features.add_features(features_map, Features.features_QUALITY(set_name))
        features_map = Features.add_features(features_map, Features.features_TROLLNESS(set_name))
        #features_map = Features.add_features(features_map, Features.features_ACTIVITY(set_name))
        features_map = Features.add_features(features_map, Features.features_CREDIBILITY(set_name))
        features_map = Features.add_features(features_map, Features.features_SENTIMENT(set_name))
        features_map = Features.add_features(features_map, Features.features_GOOGLE_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_QL_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_SYNTAX_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_RANK_SAME_USER(set_name))
        features_map = Features.add_features(features_map, Features.features_VEC_COSINES_THREAD(set_name))
        features_map = Features.add_features(features_map, Features.features_COSINES(set_name))
    if feat_index == 'CREDIBILITY-excl':
        features_map = Features.add_features(features_map, Features.features_CATEGORIES(set_name))
        features_map = Features.add_features(features_map, Features.features_QUALITY(set_name))
        features_map = Features.add_features(features_map, Features.features_TROLLNESS(set_name))
        features_map = Features.add_features(features_map, Features.features_ACTIVITY(set_name))
        #features_map = Features.add_features(features_map, Features.features_CREDIBILITY(set_name))
        features_map = Features.add_features(features_map, Features.features_SENTIMENT(set_name))
        features_map = Features.add_features(features_map, Features.features_GOOGLE_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_QL_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_SYNTAX_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_RANK_SAME_USER(set_name))
        features_map = Features.add_features(features_map, Features.features_VEC_COSINES_THREAD(set_name))
        features_map = Features.add_features(features_map, Features.features_COSINES(set_name))
    if feat_index == 'SENTIMENT-excl':
        features_map = Features.add_features(features_map, Features.features_CATEGORIES(set_name))
        features_map = Features.add_features(features_map, Features.features_QUALITY(set_name))
        features_map = Features.add_features(features_map, Features.features_TROLLNESS(set_name))
        features_map = Features.add_features(features_map, Features.features_ACTIVITY(set_name))
        features_map = Features.add_features(features_map, Features.features_CREDIBILITY(set_name))
        #features_map = Features.add_features(features_map, Features.features_SENTIMENT(set_name))
        features_map = Features.add_features(features_map, Features.features_GOOGLE_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_QL_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_SYNTAX_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_RANK_SAME_USER(set_name))
        features_map = Features.add_features(features_map, Features.features_VEC_COSINES_THREAD(set_name))
        features_map = Features.add_features(features_map, Features.features_COSINES(set_name))
    if feat_index == 'GOOGLE_VEC-excl':
        features_map = Features.add_features(features_map, Features.features_CATEGORIES(set_name))
        features_map = Features.add_features(features_map, Features.features_QUALITY(set_name))
        features_map = Features.add_features(features_map, Features.features_TROLLNESS(set_name))
        features_map = Features.add_features(features_map, Features.features_ACTIVITY(set_name))
        features_map = Features.add_features(features_map, Features.features_CREDIBILITY(set_name))
        features_map = Features.add_features(features_map, Features.features_SENTIMENT(set_name))
        #features_map = Features.add_features(features_map, Features.features_GOOGLE_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_QL_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_SYNTAX_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_RANK_SAME_USER(set_name))
        features_map = Features.add_features(features_map, Features.features_VEC_COSINES_THREAD(set_name))
        features_map = Features.add_features(features_map, Features.features_COSINES(set_name))
    if feat_index == 'QL_VEC-excl':
        features_map = Features.add_features(features_map, Features.features_CATEGORIES(set_name))
        features_map = Features.add_features(features_map, Features.features_QUALITY(set_name))
        features_map = Features.add_features(features_map, Features.features_TROLLNESS(set_name))
        features_map = Features.add_features(features_map, Features.features_ACTIVITY(set_name))
        features_map = Features.add_features(features_map, Features.features_CREDIBILITY(set_name))
        features_map = Features.add_features(features_map, Features.features_SENTIMENT(set_name))
        features_map = Features.add_features(features_map, Features.features_GOOGLE_VEC(set_name))
        #features_map = Features.add_features(features_map, Features.features_QL_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_SYNTAX_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_RANK_SAME_USER(set_name))
        features_map = Features.add_features(features_map, Features.features_VEC_COSINES_THREAD(set_name))
        features_map = Features.add_features(features_map, Features.features_COSINES(set_name))
    if feat_index == 'SYNTAX_VEC-excl':
        features_map = Features.add_features(features_map, Features.features_CATEGORIES(set_name))
        features_map = Features.add_features(features_map, Features.features_QUALITY(set_name))
        features_map = Features.add_features(features_map, Features.features_TROLLNESS(set_name))
        features_map = Features.add_features(features_map, Features.features_ACTIVITY(set_name))
        features_map = Features.add_features(features_map, Features.features_CREDIBILITY(set_name))
        features_map = Features.add_features(features_map, Features.features_SENTIMENT(set_name))
        features_map = Features.add_features(features_map, Features.features_GOOGLE_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_QL_VEC(set_name))
        #features_map = Features.add_features(features_map, Features.features_SYNTAX_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_RANK_SAME_USER(set_name))
        features_map = Features.add_features(features_map, Features.features_VEC_COSINES_THREAD(set_name))
        features_map = Features.add_features(features_map, Features.features_COSINES(set_name))
    if feat_index == 'RANK_SAME_USER-excl':
        features_map = Features.add_features(features_map, Features.features_CATEGORIES(set_name))
        features_map = Features.add_features(features_map, Features.features_QUALITY(set_name))
        features_map = Features.add_features(features_map, Features.features_TROLLNESS(set_name))
        features_map = Features.add_features(features_map, Features.features_ACTIVITY(set_name))
        features_map = Features.add_features(features_map, Features.features_CREDIBILITY(set_name))
        features_map = Features.add_features(features_map, Features.features_SENTIMENT(set_name))
        features_map = Features.add_features(features_map, Features.features_GOOGLE_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_QL_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_SYNTAX_VEC(set_name))
        #features_map = Features.add_features(features_map, Features.features_RANK_SAME_USER(set_name))
        features_map = Features.add_features(features_map, Features.features_VEC_COSINES_THREAD(set_name))
        features_map = Features.add_features(features_map, Features.features_COSINES(set_name))
    if feat_index == 'VEC_COSINES_THREAD-excl':
        features_map = Features.add_features(features_map, Features.features_CATEGORIES(set_name))
        features_map = Features.add_features(features_map, Features.features_QUALITY(set_name))
        features_map = Features.add_features(features_map, Features.features_TROLLNESS(set_name))
        features_map = Features.add_features(features_map, Features.features_ACTIVITY(set_name))
        features_map = Features.add_features(features_map, Features.features_CREDIBILITY(set_name))
        features_map = Features.add_features(features_map, Features.features_SENTIMENT(set_name))
        features_map = Features.add_features(features_map, Features.features_GOOGLE_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_QL_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_SYNTAX_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_RANK_SAME_USER(set_name))
        #features_map = Features.add_features(features_map, Features.features_VEC_COSINES_THREAD(set_name))
        features_map = Features.add_features(features_map, Features.features_COSINES(set_name))
    if feat_index == 'COSINES-excl':
        features_map = Features.add_features(features_map, Features.features_CATEGORIES(set_name))
        features_map = Features.add_features(features_map, Features.features_QUALITY(set_name))
        features_map = Features.add_features(features_map, Features.features_TROLLNESS(set_name))
        features_map = Features.add_features(features_map, Features.features_ACTIVITY(set_name))
        features_map = Features.add_features(features_map, Features.features_CREDIBILITY(set_name))
        features_map = Features.add_features(features_map, Features.features_SENTIMENT(set_name))
        features_map = Features.add_features(features_map, Features.features_GOOGLE_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_QL_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_SYNTAX_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_RANK_SAME_USER(set_name))
        features_map = Features.add_features(features_map, Features.features_VEC_COSINES_THREAD(set_name))
        #features_map = Features.add_features(features_map, Features.features_COSINES(set_name))

    return features_map
