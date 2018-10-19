from sklearn.manifold import TSNE
import pickle
import os
import csv

def get_data():

    data_storage = {'comment_count': [], 'upvote_count': [], 'ratio': []}

    all_dist = {}

    base_url = "../SnoozeFiles"

    topic_dist_dir = "sorted_comment_count"
    directory_contents = os.listdir(os.path.join(base_url, topic_dist_dir))

    for file_name in directory_contents:
        if not file_name.startswith('part') or not file_name.endswith('.csv'):
            continue
        file_url = os.path.join(base_url, topic_dist_dir, file_name)
        contentReader = csv.reader(open(file_url, 'r'))
        for row in contentReader:
            obj = {
                'subreddit': row[0],
                'comment_count': int(row[1])
            }
            all_dist[row[0]] = [int(row[1])]
            data_storage['comment_count'].append(obj)


    topic_dist_dir = "sorted_ups_sum"
    directory_contents = os.listdir(os.path.join(base_url, topic_dist_dir))

    for file_name in directory_contents:
        if not file_name.startswith('part') or not file_name.endswith('.csv'):
            continue
        file_url = os.path.join(base_url, topic_dist_dir, file_name)
        contentReader = csv.reader(open(file_url, 'r'))
        for row in contentReader:
            obj = {
                'subreddit': row[0],
                'upvote_count': int(row[1])
            }
            all_dist[row[0]].append(int(row[1]))
            data_storage['upvote_count'].append(obj)

    topic_dist_dir = "comments_to_ups_ratio_sorted"
    directory_contents = os.listdir(os.path.join(base_url, topic_dist_dir))

    for file_name in directory_contents:
        if not file_name.startswith('part') or not file_name.endswith('.csv'):
            continue
        file_url = os.path.join(base_url, topic_dist_dir, file_name)
        contentReader = csv.reader(open(file_url, 'r'))
        for row in contentReader:
            if float(row[1]) > 0:
                obj = {
                    'subreddit': row[0],
                    'lurker_count': 1/float(row[1])
                }
                all_dist[row[0]].append(1/float(row[1]))
                data_storage['ratio'].append(obj)

    data_storage['ratio'].sort(key=lambda x: x['lurker_count'], reverse=True)

    return data_storage, all_dist

def get_top_subreddits():
    sorted_lists, all_dist = get_data()

    return sorted_lists, all_dist

if __name__ == '__main__':
    subreddit_dists, all_dist = get_top_subreddits()

    comments = subreddit_dists['comment_count']
    upvotes = subreddit_dists['upvote_count']
    ratio = subreddit_dists['ratio']

    pickle.dump(comments, open("comments.pkl", "wb"))
    pickle.dump(upvotes, open("upvotes.pkl", "wb"))
    pickle.dump(ratio, open("ratio.pkl", "wb"))
    pickle.dump(all_dist, open('tri_dim.pkl', "wb"))