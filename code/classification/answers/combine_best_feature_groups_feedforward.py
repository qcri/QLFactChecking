import RunCV
import csv, operator


################################
# Combine the best features groups.
#
################################

# This is the index of the column of the result we are comparing in the results file.
ACCURACY_INDEX = 5
MAP_INDEX = 9
F1_INDEX = 8

# To change whether runs should be sorted by accuracy or MAP, change the values below:
# RESULT_SCORE_INDEX = MAP_INDEX
# RUN_PREFIX = 'TOP_FFF_MAP_'
# TEMP_RUN_PREFIX = 'TEMP_FFF_MAP_'

RESULT_SCORE_INDEX = ACCURACY_INDEX
RUN_PREFIX = 'TOP_FFF_ACC_'
TEMP_RUN_PREFIX = 'TEMP_FFF_ACC_'

# RESULT_SCORE_INDEX = F1_INDEX
# RUN_PREFIX = 'TOP_FFF_F1_'
# TEMP_RUN_PREFIX = 'TEMP_FFF_F1_'

SET_NAME = 'dev+test'
RESULTS_FILE = "../../../data/results/results-answers-cross-validation-"+SET_NAME+".tsv"

TOP_N_FROM = 2
TOP_N_TO = 40

def main():
    # 1. Read the results file and sort the scores (only the single feature groups: -incl)
    # 2. combine the features from the feature group
    best_results = read_best_system_results()

    max_index = len(best_results)

    # for group_score in best_results:
    #     group = group_score[0]
    #     score = group_score[1]

   
    # current_best = []
    # current_best.append(best_results[0])
    # X = best_results
    # X.remove(best_results[0])
    # groups_names = [best_results[0]]
    # groups_names_str = best_results[0]

    best_system = best_results[0]
    current_best = []
    current_best.append(best_system)
    X = best_results
    # print('X', X)
    X.remove(best_system)
    groups_names = [best_system]
    groups_names_str = best_system

    # for i in range(0, len(X)):
    #     n = i+1
    #     for j in range(0, len(X)):
    #         temp_groups_names = groups_names
    #         temp_groups_names_str = groups_names_str

    #         index_name = temp_system_prefix(i, j)
    #         temp_groups_names.append(X[j][0])
    #         if temp_groups_names_str != '':
    #             temp_groups_names_str += ', '    
    #         temp_groups_names_str += X[j][0]
    #         run_id = index_name + ' ('+temp_groups_names_str + ')'
    #         print('!!! Running...', run_id)
    #         RunCV.run(run_id, temp_groups_names)
    #     best_temp_system = select_best_system(i, j)
    #     current_best.append(best_temp_system)
    #     X.remove(best_temp_system)
    #     index_name = 'FF_'+int(i)
    #     groups_names.append(best_temp_system[0])
    #     if groups_names_str != '':
    #         groups_names_str += ', '    
    #     groups_names_str += best_temp_system[0]
    #     run_id = index_name + ' ('+groups_names_str + ')'
    #     print('!!! Running...', run_id)
    #     RunCV.run(run_id, groups_names)


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
            RunCV.run(run_id, temp_groups_names)
            
        # print('>>>>>>>>>>')
        best_temp_system = select_best_temp_system(i, j)
        current_best.append(best_temp_system)
        X.remove(best_temp_system)
        index_name = RUN_PREFIX+str(i+1)
        groups_names.append(best_temp_system)  
        groups_names_str += best_temp_system
        run_id = index_name + ' ('+groups_names_str + ')'
        print('!!! Running...', run_id)
        RunCV.run(run_id, groups_names)


        # if n >= TOP_N_FROM:
            # run_id = index_name + ' ('+groups_names_str + ')'
            # print('!!! Running...', run_id)
            # RunCV.run(run_id, groups_names)


def temp_system_prefix(i, j=-1, group=''):
    if j >=0:
        return TEMP_RUN_PREFIX + str(i+1) + '_' + str(j) + '__'+group + '___'
    else:
        return TEMP_RUN_PREFIX + str(i+1)



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

def read_best_system_results():
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
    # return sorted_group_scores
    sorted_groups = []             
    for gr in sorted_group_scores:
        sorted_groups.append(gr[0])
    return sorted_groups


# Start here:
main()