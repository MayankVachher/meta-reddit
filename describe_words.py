import requests
import pickle
import pandas as pd
import os
import csv

data = None

def readColorList():
    color1 = "#3366CC,#DC3912,#FF9900,#109618,#990099,#3B3EAC,#0099C6,#DD4477"
    color2 = "#66AA00,#B82E2E,#316395,#994499,#22AA99,#AAAA11,#6633CC,#E67300"
    color3 = "#8B0707,#329262,#5574A6,#3B3EAC"

    return color1.split(',') + color2.split(',') + color3.split(',')

def get_data():
    base_url = "../SnoozeFiles"

    topic_dist_dir = "top_words_topic_final"

    directory_contents = os.listdir(os.path.join(base_url, topic_dist_dir))

    data_storage = []

    for file_name in directory_contents:
        if not file_name.startswith('part') or not file_name.endswith('.csv'):
            continue
        print(file_name)
        file_url = os.path.join(base_url, topic_dist_dir, file_name)
        print(file_url)
        contentReader = csv.reader(open(file_url, 'r'))
        for row in contentReader:
            obj = {'topic_num': int(row[0]) + 1}
            obj['dists'] = []
            words = row[1].split(',')
            probs = row[2].split(',')
            probs = list(map(lambda x: '{:.4f}'.format(float(x)), probs))
            for i in range(3):
                obj['dists'].append((words[i], probs[i]))

            data_storage.append(obj)
    return data_storage

def get_topic_dists():
    topic_word_dist = get_data()
    print(topic_word_dist)
    return topic_word_dist

if __name__ == '__main__':
    topic_dict = get_topic_dists()

    pickle.dump(topic_dict, open("top_words_topic.pkl", "wb"))