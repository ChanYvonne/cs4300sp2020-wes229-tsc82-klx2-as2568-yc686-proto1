import re
import json
from glob import glob
import os
from io import StringIO
from itertools import groupby
import pickle

import numpy as np
from numpy import linalg as LA

project_name = "Find the Pea to your Podcast"
net_id = "Will Spencer: wes229, Theresa Cho: tsc82, Kathleen Xu: klx2, Yvonne Chan: yc686, Akira Shindo: as2568"

def tokenize(text):
    """Returns a list of words that make up the text.
    
    Note: for simplicity, lowercase everything.
    Requirement: Use Regex to satisfy this function
    
    Params: {text: String}
    Returns: List
    """
    # YOUR CODE HERE
    return re.findall("[A-Za-z]+", text.lower())

def make_word_blob(podcast_dict, review_lst):
    word_blob = []
    word_blob = word_blob + tokenize(podcast_dict["description"])
    # relevant_review_lst = list(filter(lambda x: x["pod_name"] == podcast_dict["name"], review_lst))
    # for each_review in relevant_review_lst:
    #     word_blob = word_blob + tokenize(each_review["rev_text"])
    return word_blob


def jaccard_sim_score(query, podcast_dict, review_lst):
    """Returns an int percentage giving the jaccard similarity of 
    Step 1: Make a word blob of all the reviews and description of the query
    Step 2: Make a word blob of all the reviews and description of the podcast_dict
    Step 3: Do a jaccard sim of the two word blobs
    """
    # YOUR CODE HERE
    word_blob_1 = set(make_word_blob(query, review_lst))
    word_blob_2 = set(make_word_blob(podcast_dict, review_lst))
    score = round(len(word_blob_1 & word_blob_2) * 100/len(word_blob_1 | word_blob_2))
    podcast_dict["similarities"] = [("Duration", "TBD"), ("No. Episodes", "TBD"), ("Genre", "TBD"), ("Description", score)]
    podcast_dict["similarity"] = score
    return score

def get_ranked_podcast(query, podcast_lst, review_lst):
    # query is a dictionary representing the podcast that the user chose
    # podcast_lst is a list of dictionaries, and each dictionary represents a podcast
    # review_lst is a list of dictionaries, and each dictionary represents a review of all podcasts in the database
    # Returns a tuple of (score, podcast_data), so it will be an (int, dict) type
    # description_lst = list(map(lambda x: (x["description"], x), podcast_lst))
    score_lst = list(map(lambda x: (jaccard_sim_score(query, x, review_lst), x), podcast_lst))
    sorted_lst = sorted(score_lst, key=lambda x: x[0], reverse=True)
    ranked_podcast_lst = list(map(lambda x: x[1], sorted_lst))
    return ranked_podcast_lst[:20]

def main():
    print("The following is the score...")
    print(get_ranked_podcast({"name": 'query', "description": "Hello is a test"}, 
        [{"name": 'pod_1', "description": "Hello", "similarities": []}, {"name": 'pod_2', "description": "Hello a test.", "similarities": []}, {"name": 'pod_3', "description": "Hello a", "similarities": []}],
        [{'pod_name': 'query', 'rev_text': "podcast sucks"}, {'pod_name': 'pod_1', 'rev_text': "this podcast sucks"}, {'pod_name': 'pod_2', 'rev_text': "this podcast is great"}]))

# main()
# def get_top_rankings(query, )
