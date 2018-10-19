import requests
from sklearn.manifold import TSNE
import pickle
import pandas as pd
import os

data = None

def readColorList():
    color1 = "#3366CC,#DC3912,#FF9900,#109618,#990099,#3B3EAC,#0099C6,#DD4477"
    color2 = "#66AA00,#B82E2E,#316395,#994499,#22AA99,#AAAA11,#6633CC,#E67300"
    color3 = "#8B0707,#329262,#5574A6,#3B3EAC"

    return color1.split(',') + color2.split(',') + color3.split(',')

def get_data():
    base_url = "../SnoozeFiles"

    topic_dist_dir = "topic_distribution_final"

    directory_contents = os.listdir(os.path.join(base_url, topic_dist_dir))

    data_storage = []

    for file_name in directory_contents:
        if not file_name.startswith('part') or not file_name.endswith('.csv'):
            continue
        print(file_name)
        file_url = os.path.join(base_url, topic_dist_dir, file_name)
        print(file_url)
        with open(file_url, 'r') as f:
            for content in f:
                print(content)
                if content != "":
                    content = content.replace('\"','')
                    obj = {'subreddit_name': content.split(',')[0]}
                    maxval = 0
                    topic_assigned = 0
                    num_topics = len(content.split(',')) - 1
                    for i, contentval in enumerate(list(map(float, content.split(',')[1:]))):
                        obj['topic_'+str(i+1)] = contentval
                        if contentval > maxval:
                            maxval = contentval
                            topic_assigned = i+1
                    obj['assignment'] = topic_assigned
                    data_storage.append(obj)

    return pd.DataFrame(data_storage), num_topics

def gen_TSNE_data():
    doc_topic_dist, num_topics = get_data()
    topic_dist = doc_topic_dist.drop(['subreddit_name', 'assignment'], axis=1)

    tsne_model = TSNE(n_components=2, verbose=5, random_state=42, angle=0.9, init='pca', n_iter=600, perplexity=30)
    tsne_results = tsne_model.fit_transform(topic_dist.values)

    data_plot = doc_topic_dist[['subreddit_name', 'assignment']]

    data_plot['x'] = tsne_results[:,0]
    data_plot['y'] = tsne_results[:,1]

    return data_plot.to_dict('records'), num_topics

def get_topic_dictionaries():
    colorList = readColorList()
    data_dicts, num_topics = gen_TSNE_data()

    data = []

    for k in range(num_topics):
        data_obj = {
            'meta_label': "Topic "+str(k+1),
            'color': colorList[k],
            'data': []
        }
        data.append(data_obj)

    for tsne_res in data_dicts:
        add_obj = {
            'x': tsne_res['x'],
            'y': tsne_res['y'],
            'subreddit_name': tsne_res['subreddit_name']
        }

        loc = tsne_res['assignment'] - 1

        data[loc]['data'].append(add_obj)

    return data

if __name__ == '__main__':
    topic_dict = get_topic_dictionaries()

    pickle.dump(topic_dict, open("topic_dict.pkl", "wb"))
