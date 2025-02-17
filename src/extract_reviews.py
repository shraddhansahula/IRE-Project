import json
from nltk import tokenize
from random import shuffle

from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import confusion_matrix
from sklearn.svm import SVC

count_f = 0
count_n = 0
tagged_reviews = []
min_votes = 4
threshold = 10

def create_tfidf_training_data(docs):
    """
    Creates a document corpus list (by stripping out the
    class labels), then applies the TF-IDF transform to this
    list. 

    The function returns both the class label vector (y) and 
    the corpus token/feature matrix (X).
    """
    # Create the training data class labels
    y = [d[0] for d in docs]
    
    # Create the document corpus list
    corpus = [d[1] for d in docs]


    # Create the TF-IDF vectoriser and transform the corpus
    vectorizer = TfidfVectorizer(min_df=1)
    
    X = vectorizer.fit_transform(corpus)
    
    return X, y

def train_svm(X, y):
    """
    Create and train the Support Vector Machine.
    """
    svm = SVC(C=1000000.0, gamma=0.0, kernel='rbf')
    svm.fit(X, y)
    return svm

for line in open('../dataset/yelp_academic_dataset_review.json', 'r'):
	review = json.loads(line)
	if review['votes']['funny'] >= min_votes  and count_f < threshold:
	    count_f += 1
	    tagged_reviews.append((1, review['text']))
	elif review['votes']['funny'] < min_votes and count_n < threshold:
		count_n += 1
		tagged_reviews.append((0, review['text']))
	if count_f == threshold and count_n == threshold:
		break

'''
t_funny = []
for review in funny:
	t_funny.append(tokenize.word_tokenize(review))

t_not_funny = []
for review in not_funny:
	t_not_funny.append(tokenize.word_tokenize(review))
'''

overall_score = 0

# Vectorise and TF-IDF transform the corpus 

for (i, k) in [(5, 0.2), (4, 0.25), (3, 0.33)]:
    
    print str(i)+"-fold:",

    shuffle(tagged_reviews)
    X, y = create_tfidf_training_data(tagged_reviews)
    # Create the training-test split of the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=k, random_state=42)

    # Create and train the Support Vector Machine
    svm = train_svm(X_train, y_train)

    # Make an array of predictions on the test set
    pred = svm.predict(X_test)

    # Output the hit-rate and the confusion matrix for each model
    print round(svm.score(X_test, y_test), 2)
    overall_score += svm.score(X_test, y_test)

print "Overall Accuracy:",
print round(overall_score/3, 2)


