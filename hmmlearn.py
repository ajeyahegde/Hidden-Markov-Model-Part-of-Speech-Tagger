import sys

input_filename = sys.argv[1]

input_file = open(input_filename, "r", encoding='utf8')

word_dict = dict()

tag_dict = dict()

tag_count_dict = dict()

word_tag_probabilities = dict()

tag_tag_probabilities = dict()

tag_set = set()
i = 0

#Read input and store tag-tag and word-tag tuples to dictionary
for line in input_file:
    words = line.strip().split(" ")
    i += 1
    previous_tag = "<<start>>"
    for w in words:
        word, tag = w.rsplit('/', 1)
        tag_set.add(tag)
        #print(word, tag)
        if (previous_tag, tag) in tag_dict:
            tag_dict[(previous_tag, tag)] += 1
        else:
            tag_dict[(previous_tag, tag)] = 1



        if tag in word_dict:
            if word in word_dict[tag]:
                word_dict[tag][word] += 1
            else:
                word_dict[tag][word] = 1
        else:
            word_dict[tag] = dict()
            word_dict[tag][word] = 1

        if previous_tag in tag_count_dict:
            tag_count_dict[previous_tag] += 1
        else:
            tag_count_dict[previous_tag] = 1

        previous_tag = tag

tag_set.add("<<start>>")
num_tags = len(tag_set)

transission_dict = dict()

open_tags = []

#For loop to segregate open tags
for tag in tag_set:
    if tag in word_dict and len(word_dict[tag]) >= 1000:
        open_tags.append(tag)

#For loop to calculate transission probabilities
for tag1 in tag_set:
    for tag2 in tag_set:
        count = 0
        if(tag1, tag2) in tag_dict:
            count = tag_dict[(tag1, tag2)]
        prob = (count + 1)/(tag_count_dict[tag1]+num_tags)
        transission_dict[(tag1, tag2)] = prob

#For loop to calculate emission probabilities
for tag in word_dict:
    words = word_dict[tag]
    total = sum(words.values())
    for word in words:
        prob = words[word] / total
        word_tag_probabilities[(tag, word)] = prob

#Write to output file
output_file = open("hmmmodel.txt", "w", encoding='utf-8')
output_file.write("Tag-Tag Probabilities:\n")
output_file.write(str(len(transission_dict))+"\n")
for tag_tuple in transission_dict:
    first_tag = tag_tuple[0]
    second_tag = tag_tuple[1]
    prob = transission_dict[tag_tuple]
    output_file.write(first_tag+"\t"+second_tag+"\t"+str(prob)+"\n")


output_file.write("Tag-Word Probabilities:\n")
output_file.write(str(len(word_tag_probabilities))+"\n")
for tag_tuple in word_tag_probabilities:
    first_tag = tag_tuple[0]
    second_tag = tag_tuple[1]
    prob = word_tag_probabilities[tag_tuple]
    output_file.write(first_tag+"\t"+second_tag+"\t"+str(prob)+"\n")

output_file.write(str(len(open_tags))+"\n")
for tag in open_tags:
    output_file.write(tag+"\n")
output_file.close()