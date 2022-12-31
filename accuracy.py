
input_file1 = open(r"hmmoutput.txt", "r", encoding='utf8')
input_file2 = open(r"ja_gsd_dev_tagged.txt", "r", encoding='utf8')

count = 0
total = 0
error = 0
for line1 in input_file1:
    line2 = input_file2.readline()
    words1 = line1.strip().split(" ")
    words2 = line2.strip().split(" ")
    for i in range(len(words1)):
        word1, tag1 = words1[i].rsplit('/', 1)
        word2, tag2 = words2[i].rsplit('/', 1)
        if tag1 == tag2:
            count += 1
        else:
            if(tag2=="S" or tag2=="V" or tag2== "A" or tag2=="SP" or tag2=="N"):
                error += 1
        total += 1

accuracy = count/total
print(count)
print(total)
print(error)
print("Accuracy:", accuracy)