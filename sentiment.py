#!/usr/bin/env python
# 
#  classifier.py
#  analyzes the sentiment of strings passed into stdin as json. (array of strings)
#  
#  Created by Philip Thrasher on 2011-02-28.
#  Copyright 2011 pthrash entuhpryzizz. All rights reserved.
# 


import os, sys, nltk.classify.util, json, cPickle, collections

MIN_THRESHOLD = 0.37
MAX_THRESHOLD = 0.63
CLASSIFIER = 'pickles/nbClassifier.pickle'
STOPWORDS = 'pickles/stopwords.pickle'

class Classifier():
    def __init__(self):
        """docstring for __init__"""
        self.classifier = cPickle.load(open(CLASSIFIER))
        #self.stopwords = cPickle.load(open(STOPWORDS))
    
    def _string_to_feature(self, text):
        """docstring for _string_to_feature"""
        words = text.split(" ")
        return dict([(word.lower(), True) for word in words])
    
        
    def _generate_features(self, strings):
        """generates the features for classification."""
        features = []
        for item in strings:
            feature = self._string_to_feature(item)
            if not(MIN_THRESHOLD <= self.classifier.prob_classify(feature).prob('pos') <= MAX_THRESHOLD):
                features.append((feature, item,))
        return features

    def classify(self, strings):
        """docstring for analyze"""
        testsets = collections.defaultdict(set)
        features = self._generate_features(strings)
        for i, feature in enumerate(features):
            observed = self.classifier.classify(feature[0])
            testsets[observed].add(i)
        final = []
        for neg in testsets['neg']:
            final.append(dict(id=neg, content=features[int(neg)][1], classification='neg'))
        for pos in testsets['pos']:
            final.append(dict(id=pos, content=features[int(pos)][1], classification='pos'))
        return sorted(final, key=lambda d: int(d['id']))
        
    
if __name__ == '__main__':
    pass
    