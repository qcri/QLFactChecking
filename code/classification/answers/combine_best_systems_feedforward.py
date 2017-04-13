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
F1_INDEX = 8

# Value above which the postiive or negative label is 
# CLASSIFICATION_THRESHOLD = 0.55

# To change whether runs should be sorted by accuracy or MAP, change the values below:
RESULT_SCORE_INDEX = MAP_INDEX
RUN_PREFIX = 'TOP_FFS_MAP_'
TEMP_RUN_PREFIX = 'TEMP_FFS_MAP_'

# RESULT_SCORE_INDEX = ACCURACY_INDEX
# RUN_PREFIX = 'TOP_FFS_ACC_'
# TEMP_RUN_PREFIX = 'TEMP_FFS_ACC_'

# RESULT_SCORE_INDEX = F1_INDEX
# RUN_PREFIX = 'TOP_FFS_F1_'
# TEMP_RUN_PREFIX = 'TEMP_FFS_F1_'

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

    best_system = best_results[0]
    current_best = []
    current_best.append(best_system)
    X = best_results
    # print('X', X)
    X.remove(best_system)
    groups_names = [best_system]
    groups_names_str = best_system

    # print('BEST:', best_system)
    # print('X', X)

    for i in range(1, len(X)):
        n = i+1
        for j in range(0, len(X)):
            temp_groups_names = list(groups_names)
            temp_groups_names_str = groups_names_str

            # print('----------', groups_names)
            # print('----------', temp_groups_names)

            index_name = temp_system_prefix(i, j, X[j])
            temp_groups_names.append(X[j])
            if temp_groups_names_str != '':
                temp_groups_names_str += ', '    
            temp_groups_names_str += X[j]
            run_id = index_name + ' ('+temp_groups_names_str + ')'
            print('!!! Running...', run_id)
            #RunCV.run(run_id, temp_groups_names)
            print('1', groups_names)
            combine_system_predictions(temp_groups_names, run_id, SET_NAME, RunCV.DATA_PATH)
            print('2', groups_names)

        # print('>>>>>>>>>>')
        best_temp_system = select_best_temp_system(i, j)
        current_best.append(best_temp_system)
        X.remove(best_temp_system)
        index_name = RUN_PREFIX+str(i)
        groups_names.append(best_temp_system)  
        groups_names_str += best_temp_system
        run_id = index_name + ' ('+groups_names_str + ')'
        print('!!! Running...', run_id)
        #RunCV.run(run_id, groups_names)
        combine_system_predictions(groups_names, run_id, SET_NAME, RunCV.DATA_PATH)

    # groups_names = []
    # groups_names_str = ''
    # for i in range(0, runs_limit):
    #     n = i+1
    #     index_name = prefix+str(n)
    #     groups_names.append(best_results[i][0])
    #     if groups_names_str != '':
    #         groups_names_str += ', '    
    #     groups_names_str += best_results[i][0]

    #     if n >= TOP_N_FROM:
    #         run_id = index_name + ' ('+groups_names_str + ')'
    #         print('!!! Running...', run_id)
    #         #RunCV.run(run_id, groups_names)

    #         # clear the predictions file to overwrite it with the latest result
    #         if os.path.exists(RunCV.score_predictions_path(run_id)):
    #             os.remove(RunCV.score_predictions_path(run_id))
    #         if os.path.exists(RunCV.ranking_predictions_path(run_id)):
    #             os.remove(RunCV.ranking_predictions_path(run_id))
    #         if os.path.exists(RunCV.predictions_path(run_id)):
    #             os.remove(RunCV.predictions_path(run_id))

    #         combine_system_predictions(groups_names, run_id, SET_NAME, RunCV.DATA_PATH)
    #         if RunCV.EVAL_ON_TEST_SET:
    #             # RunCV.evaluate_test_sets(RESULTS_FILE, run_id, 'na', 'na', RunCV.TEST_SET_NAME, RunCV.TEST_DATA_PATH)
    #             combine_system_predictions(groups_names, run_id, RunCV.TEST_SET_NAME, RunCV.TEST_DATA_PATH)

    # combine_system_predictions(['IRF_Bing_webpage_qataronly_splitted-incl', 'LINGF_All-incl'], 'TOP_IRF_LINGF', SET_NAME)



def temp_system_prefix(i, j=-1, group=''):
    if j >=0:
        return TEMP_RUN_PREFIX + str(i) + '_' + str(j) + '__'+group + '___'
    else:
        return TEMP_RUN_PREFIX + str(i)

def select_best_temp_system(i, j):
    print('SELECTING BEST RUN....')
    group_scores = {}
    with open(RESULTS_FILE,encoding="utf8") as csvfile:
        csvreader = csv.reader(csvfile, delimiter='\t')
        for row in csvreader:
            group = row[0]
            score = row[RESULT_SCORE_INDEX]
            if (group.startswith(temp_system_prefix(i, -1))):
                group_scores[group] = score                

    # print('BEFORE SORT:', group_scores)
    sorted_group_scores = sorted(group_scores.items(), key=operator.itemgetter(1), reverse=True)

    # print('AFTER SORT:', sorted_group_scores)      
    # # print(sorted_group_scores)          
    run_name = sorted_group_scores[0][0]
    group_name = run_name[run_name.index('__')+2:run_name.index('___')]
    # # print(group_name)
    return group_name


def combine_system_predictions(groups, run_id, set_name, data_path):
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
                # comment.predicted_score += score_predictions_map[comment_id]
                comment.predicted_score += ranking_predictions_map[comment_id]               
                
                # if comment.comment_id.startswith('Q380_R23'):
                #     print('updating:', comment.comment_id, comment.label, label, comment.predicted_score)    
                #     # # print(comment.predicted_label)
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
            # # # print(comment.comment_id, comment.predicted_label, comment.predicted_label/num_systems)
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

    # 3. Write the predictions file
    RunCV.write_predictions_to_file(comments.values(), RunCV.predictions_path(run_id, set_name))
    RunCV.write_score_predictions_to_file(comments.values(), RunCV.ranking_predictions_path(run_id, set_name))

    # 4. Evaluate the results
    RunCV.evaluate_test_sets(RESULTS_FILE, run_id, 'na', 'na', set_name, data_path)
    



def read_best_results(set_name):
    group_scores = {}
    groups = []
    with open(RESULTS_FILE,encoding="utf8") as csvfile:
        csvreader = csv.reader(csvfile, delimiter='\t')
        for row in csvreader:
            group = row[0]
            score = row[RESULT_SCORE_INDEX]
            set_name_in_results = row[4]
            if (group.endswith('-incl') and set_name_in_results == set_name):
                group_scores[group] = score
                groups.append(group)
                

    print('BEFORE SORT:', group_scores)
    sorted_group_scores = sorted(group_scores.items(), key=operator.itemgetter(1), reverse=True)

    print('AFTER SORT:', sorted_group_scores)

    sorted_groups = []             
    for gr in sorted_group_scores:
        sorted_groups.append(gr[0])
    return sorted_groups
    # return groups


# start here:

main(RUN_PREFIX)

# rng = np.arange(0,1,0.05)
# for val in rng: #[0.4, 0.5, 0.6]:
#     prefix = str(val) + '_M_TOP_'
#     # # print(val, prefix)
#     main(val, prefix)