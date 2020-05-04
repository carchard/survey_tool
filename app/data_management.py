from app import results_fname, json_fname
import csv
import json

def init_results():
    with open(json_fname, 'rb') as f:
        survey_form = json.load(f)

    questions = survey_form.get('questions', [])

    with open(results_fname, 'w') as f:
        w = csv.writer(f)
        w.writerow([q['text'] for q in questions])


def record_form(form, questions, email_list=[]):
    row = {q['text']: form["q{}".format(idx)].data for idx, q in enumerate(questions)}
    with open(results_fname, 'a') as f:
        w = csv.DictWriter(f, fieldnames=[q['text'] for q in questions])
        w.writerow(row)
    

def show_results():
    """
    returns a list that is ordered based on the number of questions. Elements
    of this list wll be dictionaries with the following fields:
        text: the text from the question so it can be written out on results page
        type: the type of the question
        avg: the average value (left as None for text-based answers)
        min: the minimum value that was submitted (left as None for text-based answers)
        max: the maximum value that was submitted (left as None for text-based answers)
        data: a list of all of the answers that were submitted
    """
    with open(json_fname, 'rb') as f:
        survey_form = json.load(f)


    questions = survey_form.get('questions', [])
    title = survey_form.get('title', 'Missing Title')
    fieldnames = [q['text'] for q in questions]
    results = []

    with open(results_fname, 'r') as f:
        r = csv.DictReader(f, fieldnames=fieldnames)
        next(r)
        for row in r:
            results.append(row)

    # parse out by columns instead of rows
    q_types = [q['type'] for q in questions]
    q_dats = [ [row[q['text']] for row in results if row[q['text']] is not ''] for q in questions]

    # check if there are any answers to the first question
    if len(q_dats[0]) == 0:
        return title, []

    output = [] # prepare the output values
    for q, q_dat in zip(questions, q_dats):
        q_processed = {
            "text": q['text'],
            "type": q['type'],
            "avg": None,
            "min": None,
            "max": None,
            "count_yes": 0,
            "count_no": 0,
            "data": q_dat
        }
        if q_types == "short_answer":
            pass # presently there is no additional processing for text answers

        elif q['type'] == '1-5':
            q_dat = [int(dat) for dat in q_dat]
            q_processed['avg'] = sum(q_dat)/float(len(q_dat))
            q_processed['min'] = min(q_dat)
            q_processed['max'] = max(q_dat)
            
        elif q['type'] == '1-11':
            q_dat = [int(dat) for dat in q_dat]
            q_processed['avg'] = sum(q_dat)/float(len(q_dat))
            q_processed['min'] = min(q_dat)
            q_processed['max'] = max(q_dat)

        elif q['type'] == 'long_answer':
            pass # presently there is no additional processing for text answers

        elif q['type'] == 'long_answer_optional':
            pass # presently there is no additional processing for text answers

        elif q['type'] == 'yes_no':
            print(q_dat)
            q_processed['count_yes'] = len([x for x in q_dat if int(x)==2])
            q_processed['count_no'] = len([x for x in q_dat if int(x)==1])
            print(q_processed)
        elif q['type'] == 'disagree_agree': 
            q_dat = [int(dat) for dat in q_dat]
            avg = sum(q_dat)/float(len(q_dat))
            avg_int = int(avg)
            da_dict = {1: 'strongly disagree', 2: 'disagree', 3: 'neutral', 4: 'agree', 5: 'strongly agree'}
            q_processed['avg'] = da_dict[avg_int]
            q_processed['min'] = da_dict[min(q_dat)]
            q_processed['max'] = da_dict[max(q_dat)]          

        else:
            pass # unknown question type

        output.append(q_processed)

    return title, output