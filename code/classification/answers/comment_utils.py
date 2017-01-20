import xml.etree.ElementTree as ET
import csv, random
from comment import Comment

POSITIVE_LABELS = ['Factual - True']
NEGATIVE_LABELS = ['Factual - False', 'Factual - Partially True', 'Factual - Conditionally True', 'NonFactual', 'Factual - Responder Unsure']

def read_comments(input_xml_file):
    comments = []

    tree = ET.parse(input_xml_file)
    root = tree.getroot()
    for thread in root:
        question_tag = thread[0]
        question_id = question_tag.attrib['RELQ_ID']
        question_subject = question_tag[0].text
        question_text = question_tag[1].text
        question_category = question_tag.attrib['RELQ_CATEGORY']
        question_user = question_tag.attrib['RELQ_USERID']
        question_date = question_tag.attrib['RELQ_DATE']
        question_subject = ignore_non_utf8(question_subject)
        question_text = ignore_non_utf8(question_text)
        question_fact_label = question_tag.attrib['RELQ_FACT_LABEL']

        if question_fact_label == 'Single Question - Factual':
            for index, comment_tag in enumerate(thread):
                if index > 0: # the 0 index was processed above - it is the question
                    comment_id = comment_tag.attrib['RELC_ID']
                    comment_text = comment_tag[0].text
                    comment_user = comment_tag.attrib['RELC_USERID']
                    comment_date = comment_tag.attrib['RELC_DATE']
                    comment_fact_label = comment_tag.attrib['RELC_FACT_LABEL']

                    comment = Comment(question_id, comment_id, question_category, question_subject, question_text, comment_text, comment_user, comment_date)

                    label = get_label(comment_fact_label)
                    if label > -1:
                        comment.label = label
                        comments.append(comment)

    return comments

def read_comment_labels_from_xml(input_xml_file):
    labels = {}
    print('parsing...', input_xml_file)

    tree = ET.parse(input_xml_file)
    root = tree.getroot()
    for thread in root:
        question_tag = thread[0]
        question_fact_label = question_tag.attrib['RELQ_FACT_LABEL']
        if question_fact_label == 'Single Question - Factual':
            for index, comment_tag in enumerate(thread):
                if index > 0: # the 0 index was processed above - it is the question
                    comment_fact_label = comment_tag.attrib['RELC_FACT_LABEL']
                    comment_id = comment_tag.attrib['RELC_ID']
                    label = get_label(comment_fact_label)
                    if label > -1:
                        labels[comment_id] = label
    return labels

# Reads question labels from TSV file in the format: QID\tlabel
def read_comment_labels_from_tsv(input_file):
    comment_labels = {}
    with open(input_file,encoding="utf8") as csvfile:
        csvreader = csv.reader(csvfile, delimiter='\t')
        for row in csvreader:
            for index,value in enumerate(row):
                label = row[1]
                if label == '1':
                    label = 1
                else: 
                    label = 0
                comment_labels[row[0]] = label
                
    return comment_labels

def get_label(original_label):
    if original_label  == 'True':
        return 1
    elif original_label  == 'False':
        return 0
    return -1

def ignore_non_utf8(text):
    if not text:
        text = ''
    return ''.join([i if ord(i) < 128 else ' ' for i in text])


def split_set_in_parts(xml_file, parts_size):
    parts = [[] for _ in range(parts_size)]
    # Init the random seed in order to produce the same split of a set every time
    rand = random.Random(0) 

    tree = ET.parse(xml_file)
    root = tree.getroot()
    for thread in root:
        question_tag = thread[0]
        question_id = question_tag.attrib['RELQ_ID']
        question_subject = question_tag[0].text
        question_text = question_tag[1].text
        question_category = question_tag.attrib['RELQ_CATEGORY']
        question_user = question_tag.attrib['RELQ_USERID']
        question_date = question_tag.attrib['RELQ_DATE']
        question_subject = ignore_non_utf8(question_subject)
        question_text = ignore_non_utf8(question_text)
        question_fact_label = question_tag.attrib['RELQ_FACT_LABEL']

        if question_fact_label == 'Single Question - Factual':
            parts_index = -1
            for index, comment_tag in enumerate(thread):
                if index > 0: # the 0 index was processed above - it is the question
                    comment_id = comment_tag.attrib['RELC_ID']
                    comment_text = comment_tag[0].text
                    comment_user = comment_tag.attrib['RELC_USERID']
                    comment_date = comment_tag.attrib['RELC_DATE']
                    comment_fact_label = comment_tag.attrib['RELC_FACT_LABEL']
                    comment = Comment(question_id, comment_id, question_category, question_subject, question_text, comment_text, comment_user, comment_date)

                    label = get_label(comment_fact_label)
                    if label > -1:
                        # if any of the comments is in the labels, add it to the subset part
                        comment.label = label
                        if parts_index == -1:
                            parts_index = rand.randint(0,parts_size-1)
                        parts[parts_index].append(comment)
    return parts
