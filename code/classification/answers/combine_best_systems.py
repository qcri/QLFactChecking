import RunCV, comment_utils
from comment import Comment
import csv, operator, string, os


################################
# Combine the best features groups.
#
################################

# This is the index of the column of the result we are comparing in the results file.
ACCURACY_INDEX = 5
MAP_INDEX = 9

# Value above which the postiive or negative label is 
CLASSIFICATION_THRESHOLD = 0.5

# To change whether runs should be sorted by accuracy or MAP, change the values below:
RESULT_SCORE_INDEX = ACCURACY_INDEX
RUN_PREFIX = 'TOP_'

SET_NAME = 'dev+test'
RESULTS_FILE = "../../../data/results/results-answers-cross-validation-"+SET_NAME+".tsv"

PREDICTIONS_PATH = string.Template("../../../data/predictions/predicted-labels-$set-$run_id-.tsv")
SCORE_PREDICTIONS_PATH = string.Template("../../../data/predictions/predicted-labels-$set-$run_id-map.tsv")


TOP_N_FROM = 2
TOP_N_TO = 20

def main():
    # 1. Read the results file and sort the scores (only the single feature groups: -incl)
    # 2. combine the features from the feature group
    best_results = read_best_results()

    runs_limit = min(TOP_N_TO, len(best_results))

    # for group_score in best_results:
    #     group = group_score[0]
    #     score = group_score[1]

    groups_names = []
    groups_names_str = ''
    for i in range(0, runs_limit):
        n = i+1
        index_name = RUN_PREFIX+str(n)
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
            if os.path.exists(RunCV.predictions_path(run_id)):
                os.remove(RunCV.predictions_path(run_id))

            combine_system_predictions(groups_names, run_id)

def combine_system_predictions(groups, run_id):
    print('combining:', groups)
    gold_labels_file = 'asdf'    
    comments = {}
    num_systems = len(groups)
    for group in groups:
        prediction_labels_file = RunCV.predictions_path(group)
        score_prediction_labels_file = RunCV.score_predictions_path(group)

        predictions_map = comment_utils.read_comment_labels_from_tsv(prediction_labels_file)
        score_predictions_map = comment_utils.read_comment_scores_from_tsv(score_prediction_labels_file)

        # 1. Sum the predictions of all the used systems
        for comment_id, label in predictions_map.items():
            if comment_id in comments.keys():
                comment = comments[comment_id]
                comment.predicted_label += label
                comment.predicted_score += score_predictions_map[comment_id]
                print('updating:', comment.comment_id, comment.predicted_label, comment.predicted_score)
                comments[comment_id] = comment
            else:
                comment = Comment('', comment_id, '', '', '', '', '', '')
                comment.predicted_label = label
                comment.predicted_score = score_predictions_map[comment_id]
                comments[comment_id] = comment
                print('adding:', comment.comment_id, comment.predicted_label, comment.predicted_score)

        # 2. Calculate the classification label for each comment
        for comment in comments.values():
            if comment.predicted_score/num_systems >= CLASSIFICATION_THRESHOLD:
                comment.predicted_label = 1
            else:
                comment.predicted_label = 0
            # print('using:', comment.comment_id, comment.predicted_label, comment.predicted_score)

    # 3. Write the predicitons file
    RunCV.write_predictions_to_file(comments.values(), RunCV.predictions_path(run_id))
    RunCV.write_score_predictions_to_file(comments.values(), RunCV.score_predictions_path(run_id))

    # 4. Evaluate the results
    RunCV.evaluate_test_sets(RESULTS_FILE, run_id, 'na', 'na')



def read_best_results():
    group_scores = {}
    with open(RESULTS_FILE,encoding="utf8") as csvfile:
        csvreader = csv.reader(csvfile, delimiter='\t')
        for row in csvreader:
            group = row[0]
            score = row[RESULT_SCORE_INDEX]
            if (group.endswith('-incl')):
                group_scores[group] = score
                

    print('BEFORE SORT:', group_scores)
    sorted_group_scores = sorted(group_scores.items(), key=operator.itemgetter(1), reverse=True)

    print('AFTER SORT:', sorted_group_scores)                
    return sorted_group_scores


# start here:
main()