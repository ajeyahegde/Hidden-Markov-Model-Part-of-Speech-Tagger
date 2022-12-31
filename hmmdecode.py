import sys

import numpy as np
import math

input_file = open(r"hmmmodel.txt", "r", encoding='utf8')

dummy = input_file.readline()
tag_count = int(input_file.readline().strip())
tag_tag_dict = dict()

tags = set()
wordset = set()
open_tags = []

#Read back the probabilities value from hmmmodel.txt file
for i in range(tag_count):
    components = input_file.readline().strip().split("\t")
    tag1 = components[0].strip()
    tag2 = components[1].strip()
    prob = float(components[2].strip())
    tag_tag_dict[(tag1, tag2)] = prob
    tags.add(tag1)
    tags.add(tag2)

dummy = input_file.readline()
word_tag_count = int(input_file.readline().strip())
word_tag_dict = dict()

for i in range(word_tag_count):
    components = input_file.readline().strip().split("\t")
    tag = components[0].strip()
    word = components[1].strip()
    prob = float(components[2].strip())
    word_tag_dict[(tag, word)] = prob
    wordset.add(word)

#Read the open tags from hmmmodel.txt file
open_tag_count = int(input_file.readline().strip())
for i in range(open_tag_count):
    open_tags.append(input_file.readline().strip())


num_tags = len(tags)
num_words = len(wordset)

tag_index_dict = dict()
index_tag_dict = dict()
word_index_dict = dict()

open_tags_index = []
index = 0
if open_tag_count == 0:
    for i in range(num_tags):
        open_tags_index.append(i)

print(open_tags_index)
#Assign index to each tag, later used for Viterbi Algorithm
for tag in tags:
    tag_index_dict[tag] = index
    index_tag_dict[index] = tag
    if tag in open_tags:
        open_tags_index.append(index)
    index += 1

index = 0
#Assign index for each word, used in Viterbi Algorithm
for word in wordset:
    word_index_dict[word] = index
    index += 1

#Tag matrix has tag-tag probabilities
tag_matrix = np.empty(shape=(num_tags, num_tags))
#tag_matrix.fill(0.00000000001)

for tag in tag_tag_dict:
    tag_matrix[tag_index_dict[tag[0]], tag_index_dict[tag[1]]] = tag_tag_dict[tag]


#Word matrix has word-tag probabilities
word_matrix = np.empty(shape=(num_tags, num_words))
#word_matrix.fill(0.00000000001)


for tag in word_tag_dict:
    word_matrix[tag_index_dict[tag[0]], word_index_dict[tag[1]]] = word_tag_dict[tag]


test_filename = sys.argv[1]
test_file = open(test_filename, "r", encoding='utf8')

output_file = open("hmmoutput.txt", "w", encoding='utf-8')

#For loop for POS tagging using Viterbi Algorithm
for line in test_file:
    words = line.strip().split(" ")
    sentence_len = len(words)

    #Initialize DP Array for each sentence
    probs_dp = np.zeros((num_tags, sentence_len))
    paths_dp = np.zeros((num_tags, sentence_len))

    #Initilization stage for starting word
    if words[0] not in wordset:
        for tag in range(num_tags):
            if tag_matrix[tag_index_dict['<<start>>'], tag] == 0:
                probs_dp[tag, 0] = float("-inf")
            else:
                probs_dp[tag, 0] = math.log(tag_matrix[tag_index_dict['<<start>>'], tag])
    else:
        for tag in range(num_tags):
            if tag_matrix[tag_index_dict['<<start>>'], tag] == 0:
                probs_dp[tag, 0] = float("-inf")
            else:
                probs_dp[tag, 0] = math.log(tag_matrix[tag_index_dict['<<start>>'], tag]) + math.log(word_matrix[tag, word_index_dict[words[0]]])

    #Calculation for rest of the sentence
    for i in range(1, sentence_len):
        if words[i] not in wordset:
            for tag1 in open_tags_index:
                max_prob = float("-inf")
                max_path = None
                for tag2 in range(num_tags):
                    prob = probs_dp[tag2, i - 1] + math.log(tag_matrix[tag2, tag1])
                    if prob > max_prob:
                        max_prob = prob
                        max_path = tag2
                probs_dp[tag1, i] = max_prob
                paths_dp[tag1, i] = max_path

        else:
            for tag1 in range(num_tags):
                max_prob = float("-inf")
                max_path = None
                for tag2 in range(num_tags):
                    prob = probs_dp[tag2, i-1] + math.log(tag_matrix[tag2, tag1]) + math.log(word_matrix[tag1, word_index_dict[words[i]]])
                    if prob > max_prob:
                        max_prob = prob
                        max_path = tag2
                probs_dp[tag1, i] = max_prob
                paths_dp[tag1, i] = max_path

    m = sentence_len
    max_prob = float('-inf')
    pred = [None] * sentence_len

    #Backtracking to find the most probable tags
    for tag in range(num_tags):
        if probs_dp[tag, sentence_len - 1] > max_prob:
            max_prob = probs_dp[tag, sentence_len - 1]
            pred[sentence_len-1] = index_tag_dict[tag]

    last_tag = pred[sentence_len-1]

    for i in range(sentence_len-1, -1, -1):
        tag_i = tag_index_dict[pred[i]]
        pred[i-1] = index_tag_dict[paths_dp[tag_i, i]]
    #print(pred)


    for i in range(sentence_len-1):
        output_file.write(words[i]+"/"+str(pred[i])+" ")
    output_file.write(words[sentence_len - 1] + "/" + str(last_tag) + "\n")

