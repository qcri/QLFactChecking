import sys
sys.path.insert(0, '../../data/features/')

import csv, os
import string
import time
from sklearn.preprocessing import Normalizer
from sklearn.svm import *
from sklearn.naive_bayes import *
from sklearn.linear_model import *
from sklearn.grid_search import *
from sklearn.preprocessing import *
from sklearn.pipeline import *
from sklearn.feature_selection import *
from comment import Comment
import comment_utils
import Features
import FeatureSets

timestamp = time.strftime('%d-%m-%Y %H.%M.%S')

SET_NAME = 'dev+test'
DATA_PATH = "../../../data/input/input-"+SET_NAME+".xml"
PREDICTIONS_PATH = string.Template("../../../data/predictions/predicted-labels-$set-$run_id-$time.tsv")
RESULTS_FILE = "../../../data/results/results-answers-cross-validation-"+SET_NAME+".tsv"
CROSS_VALIDATION = True

def predictions_path(run_id):
    return PREDICTIONS_PATH.substitute(set=SET_NAME, run_id=run_id, time=timestamp)

def run(run_id, feat_index=''):
    print('--RUN_ID: ', run_id)
   
    splits = 5
    set_parts = comment_utils.split_set_in_parts(DATA_PATH, splits)

    full_set = []
    for i in range(0,splits):
        full_set.extend(set_parts[i])

    for i in range(0,splits):
        print('running experiments for split', i)
        train_set = list(full_set)
        test_set = set_parts[i]
        for c in test_set:
            train_set.remove(c)
        params = run_experiment(train_set, test_set, run_id, feat_index)

    evaluate_test_sets(RESULTS_FILE, run_id, params)

def run_experiment(train_data, dev_data, run_id, feat_index=''):
    # Read the features
    train_features, train_labels = read_features(train_data, SET_NAME, feat_index)
    dev_features, dev_labels = read_features(dev_data, SET_NAME, feat_index)

    # Scale the features
    min_max_scaler = MinMaxScaler()
    train_features = min_max_scaler.fit_transform(train_features)
    dev_features = min_max_scaler.transform(dev_features)

    # Disable building a model with scikit learn, we will use other tools instead
    # Build model from the train data
    model, best_params = build_model(train_features, train_labels)


    # Predict the dev and train data
    dev_predicted = model.predict(dev_features)

    print(dev_predicted)

    for (i,comment) in enumerate(dev_data):
        comment.predicted_label = dev_predicted[i]

    # Write the predicted labels to file
    write_predictions_to_file(dev_data, predictions_path(run_id))

    # evaluate and save the result
    return best_params

def write_predictions_to_file(data, file):
    for comment in data:
        write_to_csv_file([comment.comment_id, comment.predicted_label], file)

def evaluate_test_sets(results_file, run_id, best_params):
    # write header:
    if not os.path.exists(results_file):
        write_to_csv_file(['RUN-ID', 'Time', 'Params\tOptimized for', 'SET', 'Accuracy', 'Precision', 'Recall', 'F1', 'Predictions', '', ''], results_file)

    result_line = [run_id, timestamp, best_params]

    dev_eval = evaluate(DATA_PATH, predictions_path(run_id), results_file, run_id, SET_NAME, best_params)

    result_line.extend(dev_eval)

    write_to_csv_file(result_line, results_file)

def evaluate(gold_labels_file, prediction_file, results_file, run_id, set_name, best_params):
    gold_labels = comment_utils.read_comment_labels_from_xml(gold_labels_file)
    predicted_labels = comment_utils.read_comment_labels_from_tsv(prediction_file)

    true_positives = 0
    false_positives = 0
    true_negatives = 0
    false_negatives = 0

    print('evaluate...')

    for comment_id, predicted_label in predicted_labels.items():
        gold_label = gold_labels[comment_id]
        if gold_label == 1 and predicted_label == 1:
            true_positives += 1
        elif gold_label == 1 and predicted_label == 0:
            false_negatives += 1
        elif gold_label == 0 and predicted_label == 0:
            true_negatives += 1
        elif gold_label == 0 and predicted_label == 1:
            false_positives += 1

    confusion_matrix = 'TP=' + str(true_positives) + ', FP=' + str(false_positives) + ', TN=' + str(true_negatives) + ', FN=' + str(false_negatives) 
    confusion_matrix2 = 'PredictedYES='+str((true_positives+false_positives))+', ActualYES='+str((true_positives+false_negatives))
    confusion_matrix3 = 'PredictedNO='+str((true_negatives+false_negatives))+', ActualNO='+str((true_negatives+false_positives))

    print(true_positives, false_positives, true_negatives, false_negatives)

    accuracy = (true_positives + true_negatives)/(true_positives+true_negatives+false_positives+false_negatives)
    if true_positives+false_positives > 0:
        precision = true_positives/(true_positives+false_positives)
    else:
        precision = 'n/a'

    recall = true_positives/(true_positives+false_negatives)

    f1 = 2*true_positives/(2*true_positives + false_negatives + false_positives)

    return [set_name, accuracy, precision, recall, f1, confusion_matrix, confusion_matrix2, confusion_matrix3]

def read_features_from_index(data, set_name, feat_index):
    print('---Reading features from index for ' + set_name, feat_index) 
    X = []
    y = []
    features_map = FeatureSets.read_feature_set(set_name, feat_index)

    for comment in data:
        # Set the features for each
        if comment.comment_id in features_map.keys():
            pair_x = features_map[comment.comment_id]
            X.append(pair_x)
            y.append(comment.label)

    return X, y    


def read_features(data, set_name, feat_index):
    if len(feat_index) > 0:
        return read_features_from_index(data, set_name, feat_index)

    print('Reading features for set: ' + set_name)    
    X = []
    y = []
    features_map = {}

    features_map = Features.add_features(features_map, Features.read_question_word_presence_features(set_name))

    # TODO: Read more features

    for question in data:
        # Set the features for each
        question_x = features_map[question.qid]
        X.append(question_x)
        y.append(question.label)

    return X, y

    
def build_model(X, y, scoring='accuracy', params = None):
    
    print('Building model...')
    # clf = LinearSVC(C=4)
    # clf.fit(X, y)

    # If params are given, use them for the classifier
    # Otherwise - perform grid search to find the best params
    # if params:
    #     clf = SVC(params)
    # else:
    #     param_grid = [
    #         {'C': [1, 2, 4, 8], 'kernel': ['linear']},
    #         {'C': [0.5, 1, 2, 4, 8], 'gamma': [0.3, 0.2, 0.1], 'kernel': ['rbf']},
    #     ]
    #     svr = SVC()
    #     clf = GridSearchCV(svr, param_grid, scoring=scoring)    

    

    clf = SVC(C=2, gamma=0.2)
    clf.fit(X, y)

    if isinstance(clf, GridSearchCV):
        print("best params: ", clf.best_params_)
        print("best score: ", clf.best_score_)
        print("best estimator: ",  clf.best_estimator_)

        return clf, str(clf.best_params_) + '\t' + scoring
    else:
        return clf, str(clf.get_params(False)) + '\t' + scoring

def write_output(pairs, set_name, run_id):
    # output for svmrank
    file = '../output/svmrank/min2/'+run_id+'-'+set_name+'.out'
    result = {}
    for pair in pairs:
        qid_int = qid_to_int(pair.question_id)
        cid_int = cid_to_int(pair.comment_id)
        if not qid_int in result.keys():
            result[qid_int] = {}
        result[qid_int][cid_int] = [pair.question_id, pair.comment_id, pair.probability, pair.predicted_label]

    for qid in sorted(result):
        comments = result[qid]
        for cid in sorted(comments):
            label = 'true' if comments[cid][3] == 1 else 'false'
            arr = [comments[cid][0], comments[cid][1], 0, comments[cid][2], label]
            write_to_csv_file(arr, file)

def qid_to_int(qid):
    part1q = qid[qid.find('Q')+1:qid.find('_R')]
    part2q = qid[qid.find('_R')+2:]
    resq = int(part1q)*10000000 + int(part2q)*1000
    return resq

def cid_to_int(cid):
    part1c = cid[cid.find('Q')+1:cid.find('_R')]
    part2c = cid[cid.find('_R')+2:cid.find('_C')]
    part3c = cid[cid.find('_C')+2:]
    resc = int(part1c)*10000000 + int(part2c)*1000 + int(part3c)
    return resc

def write_to_csv_file(array, file_path):
    with open(file_path, 'a+', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(array)

# Start here
#main()