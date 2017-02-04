import RunCV, comment_utils
from comment import Comment
import csv, operator, string, os
import numpy as np


################################
# Combine the best features groups.
#
################################

# This is the index of the column of the result we are comparing in the results file.
ACCURACY_INDEX = 5
MAP_INDEX = 9

# Value above which the postiive or negative label is 
# CLASSIFICATION_THRESHOLD = 0.55

# To change whether runs should be sorted by accuracy or MAP, change the values below:
# RESULT_SCORE_INDEX = MAP_INDEX
# RUN_PREFIX = 'MAP_TOP_'

RESULT_SCORE_INDEX = ACCURACY_INDEX
RUN_PREFIX = 'TOP_'

SET_NAME = 'dev+test'
TEST_SET_NAME = 'dev+test'
RESULTS_FILE = "../../../data/results/results-answers-cross-validation-"+SET_NAME+".tsv"

PREDICTIONS_PATH = string.Template("../../../data/predictions/predicted-labels-$set-$run_id-.tsv")
SCORE_PREDICTIONS_PATH = string.Template("../../../data/predictions/predicted-labels-$set-$run_id-map.tsv")


TOP_N_FROM = 2
TOP_N_TO = 20

def main(prefix):
    # 1. Read the results file and sort the scores (only the single feature groups: -incl)
    # 2. combine the features from the feature group
    best_results = read_best_results(SET_NAME) # read the best resutls from the train set name

    runs_limit = min(TOP_N_TO, len(best_results))

    # for group_score in best_results:
    #     group = group_score[0]
    #     score = group_score[1]

    groups_names = []
    groups_names_str = ''
    for i in range(0, runs_limit):
        n = i+1
        index_name = prefix+str(n)
        groups_names.append(best_results[i][0])
        if groups_names_str != '':
            groups_names_str += ', '    
        groups_names_str += best_results[i][0]

        if n >= TOP_N_FROM:
            run_id = index_name + ' ('+groups_names_str + ')'
            print('!!! Running...', run_id)
            #RunCV.run(run_id, groups_names)

            # clear the predictions file to overwrite it with the latest result
            if os.path.exists(RunCV.score_predictions_path(run_id)):
                os.remove(RunCV.score_predictions_path(run_id))
            if os.path.exists(RunCV.ranking_predictions_path(run_id)):
                os.remove(RunCV.ranking_predictions_path(run_id))
            if os.path.exists(RunCV.predictions_path(run_id)):
                os.remove(RunCV.predictions_path(run_id))

            combine_system_predictions(groups_names, run_id, SET_NAME)
            # combine_system_predictions(groups_names, run_id, TEST_SET_NAME)

    # combine_system_predictions(['IRF_Bing_webpage_qataronly_splitted-incl', 'LINGF_All-incl'], 'TOP_IRF_LINGF', SET_NAME)


def combine_system_predictions(groups, run_id, set_name):
    print('combining:', groups)
    gold_labels_file = 'asdf'    
    comments = {}
    num_systems = len(groups)
    counter = 0
    for group in groups:
        counter += 1
        prediction_labels_file = RunCV.predictions_path(group, set_name)
        score_prediction_labels_file = RunCV.score_predictions_path(group, set_name)
        ranking_prediction_labels_file = RunCV.ranking_predictions_path(group, set_name)

        # write the scores to a file:
        ranking_predictions_map = comment_utils.convert_scores_to_ranking_file_and_return_ranking_map(score_prediction_labels_file, ranking_prediction_labels_file)


        predictions_map = comment_utils.read_comment_labels_from_tsv(prediction_labels_file)
        # score_predictions_map = comment_utils.read_comment_scores_from_tsv(ranking_prediction_labels_file)
        # ranking_predictions_map = comment_utils.read_comment_scores_from_tsv(ranking_prediction_labels_file)

        # 1. Sum the predictions of all the used systems
        for comment_id, label in predictions_map.items():
            if comment_id in comments.keys():
                comment = comments[comment_id]                
                # comment.label += int(label)
                comment.label.append(label)
                # comment.predicted_score += score_predictions_map[comment_id]*(1/counter)
                comment.predicted_score += ranking_predictions_map[comment_id]               
                
                # if comment.comment_id.startswith('Q380_R23'):
                #     print('updating:', comment.comment_id, comment.label, label, comment.predicted_score)    
                #     print(comment.predicted_label)
                #print('updating:', comment.comment_id, comment.predicted_label, comment.predicted_score)
            else:
                comment = Comment('', comment_id, '', '', '', '', '', '')
                comment.label = int(label)
                comment.label = []
                comment.label.append(label)
                # comment.predicted_score = score_predictions_map[comment_id]
                comment.predicted_score = ranking_predictions_map[comment_id]
                comments[comment_id] = comment
                # if comment.comment_id.startswith('Q380_R23'):
                #     print('adding:', comment.comment_id, comment.predicted_label, comment.predicted_score)

        # 2. Calculate the classification label for each comment
        for comment in comments.values():
            # print(comment.comment_id, comment.predicted_label, comment.predicted_label/num_systems)
            # if comment.label/num_systems >= threshold:
            #     comment.predicted_label = 1
            # else:
            #     comment.predicted_label = 0

            # if the systems num is an odd number - get the majority vote
            # otherwise - if the 1s and 0s are equal count, see what the highest rated systems give as a result
            sum_all_labels = 0
            strongest_system_label = comment.label[0]
            for label in comment.label:
                sum_all_labels += label

            if num_systems * 2 == 1:
                if sum_all_labels*2 >= num_systems:
                    comment.predicted_label = 1
                else:
                    comment.predicted_label = 0 
            else:
                if sum_all_labels*2 == num_systems:
                    comment.predicted_label = strongest_system_label
                elif sum_all_labels*2 > num_systems:
                    comment.predicted_label = 1
                else:
                    comment.predicted_label = 0

            # print('using:', comment.comment_id, comment.predicted_label, comment.predicted_score)

    # 3. Write the predicitons file
    RunCV.write_predictions_to_file(comments.values(), RunCV.predictions_path(run_id, set_name))
    RunCV.write_score_predictions_to_file(comments.values(), RunCV.ranking_predictions_path(run_id, set_name))

    # 4. Evaluate the results
    RunCV.evaluate_test_sets(RESULTS_FILE, run_id, 'na', 'na', set_name)



def read_best_results(set_name):
    group_scores = {}
    with open(RESULTS_FILE,encoding="utf8") as csvfile:
        csvreader = csv.reader(csvfile, delimiter='\t')
        for row in csvreader:
            group = row[0]
            score = row[RESULT_SCORE_INDEX]
            set_name_in_results = row[4]
            if (group.endswith('-incl') and set_name_in_results == set_name):
                group_scores[group] = score
                

    print('BEFORE SORT:', group_scores)
    sorted_group_scores = sorted(group_scores.items(), key=operator.itemgetter(1), reverse=True)

    print('AFTER SORT:', sorted_group_scores)                
    return sorted_group_scores


# start here:

main(RUN_PREFIX)

# rng = np.arange(0,1,0.05)
# for val in rng: #[0.4, 0.5, 0.6]:
#     prefix = str(val) + '_M_TOP_'
#     print(val, prefix)
#     main(val, prefix)