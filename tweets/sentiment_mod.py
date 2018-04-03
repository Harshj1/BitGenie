import nltk
import pandas as pd
import re
import pickle

init_train = []
word_features = []
init_test = []
sentiment_list = []


class Initialize:
    test_tweets_start = []

    def init_test_tweets(self, tweets):
        test_tweets = []
        for (text) in tweets:
            words_filtered = [e.lower() for e in text.split() if len(e) >= 3]
            test_tweets.append((words_filtered))
        # print(test_tweets[1:4])
        return test_tweets

    def init_train_tweets(self, tweets):
        train_tweets = []
        for (text, target) in tweets:
            words_filtered = [e.lower() for e in text.split() if len(e) >= 3]
            if (target == 0):
                target = 'negative'
            # elif (target == 2):
            #     target = 'neutral'
            else:
                target = 'positive'
            train_tweets.append((words_filtered, target))
        return train_tweets
        # print(train_tweets[1:4])

    def get_words(self, tweets):
        all_words = []
        for (words, sentiment) in tweets:
            all_words.extend(words)
        return all_words

    def get_words_features(self, tweets):
        words_list = nltk.FreqDist(self.get_words(tweets))
        words_features = words_list.keys()
        return words_features

    def extract_features(document):
        document_words = set(document)
        # stemmer = nltk.SnowballStemmer("english")
        features = {}
        for word in word_features:
            # word = stemmer.stem(word)
            features['contains(%s)' % word] = (word in document_words)
        return features

    def __init__(self, tweets):  # training
        inittrain = self.init_train_tweets(tweets)
        init_train.extend(inittrain)
        inittest = self.init_test_tweets(self.test_tweets_start)    #UNCOMMENT THIS

        # inittest = [
        #     ['the', 'would', 'safer', 'place', 'thousands', 'guns', 'weren', 'sold', 'every', 'day', 'without',
        #      'background', 'checks'],
        #     ['donald', 'trump', 'takes', 'hard', 'look', 'himself', 'new', 'simpsons', 'sketch'],
        #     ['desperate', 'for', 'victory', 'aussies', 'back', 'cheating', 'suspected', 'ball', 'tampering', 'bancroft',
        #      'caught', 'tape', 'cau']]  # COMMENT THIS
        init_test.extend(inittest)
        # features_train = self.get_words_features(inittrain)
        word_features.extend(self.get_words_features(inittrain))
        # training_set = nltk.classify.apply_features(extract_features(), inittrain)
        # print(training_set[1:4])

        # print(self.extract_features(inittrain))


def main():
    file = r'/home/abha/SE2018/amazon_cells_labelled.txt'
    df1 = pd.read_csv(file, sep='\t',
                      names=["text", "target"])
    # df1 = df[['text', 'target']]


    tweets = df1.values.tolist()

    Initialize(tweets)
    training_set = nltk.classify.apply_features(Initialize.extract_features, init_train)
    # print(training_set[1:4])

    # classifier = nltk.NaiveBayesClassifier.train(training_set)
    #
    # save_classifier = open("naivebayes.pickle", "wb")
    # pickle.dump(classifier, save_classifier)
    # save_classifier.close()

    classifier_pkl_opn = open("naivebayes.pickle", "rb")
    classifier_pkl = pickle.load(classifier_pkl_opn)

    # print(classifier.show_most_informative_features(32))
    # tweet = 'I go to school'
    #print(classifier.classify(Initialize.extract_features(tweet.split())))

    for tweet_split in init_test:
        dist = classifier_pkl.prob_classify(Initialize.extract_features(tweet_split))
        pos = dist.prob("positive")
        neg = dist.prob("negative")


        for label in dist.samples():
             print("%s: %f" % (label, dist.prob(label)))
        # print(pos)
        # sentiment = ''
        if((pos - neg) > 0.35):
             sentiment_list.append("positive")
        elif((neg - pos) > 0.35):
             sentiment_list.append("negative")
        else:
             sentiment_list.append("neutral")
    # print(sentiment_list)
    dictionary = dict(zip(Initialize.test_tweets_start, sentiment_list))
    return dictionary


if __name__ == "__main__": main()