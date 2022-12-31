# Hidden-Markov-Model-Part-of-Speech-Tagger
## Part of Speech Tagger using Hidden Markov Model with Italian and Japanese Language data


**DataSet has following files:**

- Two files (one Italian, one Japanese) with tagged training data in the word/TAG format, with words separated by spaces and each sentence on a new line.

- Two files (one Italian, one Japanese) with untagged development data, with words separated by spaces and each sentence on a new line.

- Two files (one Italian, one Japanese) with tagged development data in the word/TAG format, with words separated by spaces and each sentence on a new line, to serve as an answer key for evaluation.

**Project is divided into two phases:**

- hmmlearn.py will learn a Hidden-Markov model from the training data.
- hmmdecode.py will use the model to tag new data.


**To learn Hidden Markov model, run below command:**

```
python hmmlearn.py /path/to/input
```
**To use the model on test data, run below command:**

```
python hmmdecode.py /path/to/input
```
The command-line argument is a single file containing the test data; the program will read the parameters of a hidden Markov model from the file hmmmodel.txt, tag each word in the test data, and write the results to a text file called hmmoutput.txt in the same format as the training data.

Calculate accuracy of the model using below code.

```
python accuracy.py
```
