#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 16:12:43 2019

@author: tommcdonald
"""

import re, itertools
import matplotlib.pyplot as plt
import numpy as np

def zipf_analysis(file):
    # create dict of term counts in file
    word_regex = re.compile(r'[A-Za-z]+')
    counts = {}
    with open(file) as f:
        for line in f:
            for word in word_regex.findall(line.lower()):
                if word not in counts:
                    counts[word] = 0
                counts[word] += 1
    
    # print summary stats from our dictionary
    total_words = sum(counts.values())
    unique_terms = len(counts)
    terms_sorted = sorted(counts, key=lambda v:counts[v], reverse=True)
    print('Total number of words in file:', total_words)
    print('Number of unique terms in file:', unique_terms)
    print('\nTERM OCCURENCES')
    for term in terms_sorted[:20]:
        print(term, '=', counts[term])
        
    # plot sorted frequencies against rank position
    freqs = sorted(list(counts.values()), reverse=True)
    for length in [100, 1000, 'all']:
        if length != 'all':
            plt.plot(freqs[:length])
            plt.xlabel('Term Frequency')
            plt.ylabel('Term Rank')
            plt.title('Zipf\'s Law for Top ' + str(length) + ' Terms')
            plt.show()
        else:
            plt.plot(freqs)
            plt.xlabel('Term Frequency')
            plt.ylabel('Term Rank')
            plt.title('Zipf\'s Law for All Terms')
            plt.show()
    
    # plot cumulative count for first 100 words
    freqs_cum = list(itertools.accumulate(freqs))
    plt.plot(freqs_cum[:100])
    plt.xlabel('Cumulative Term Frequency')
    plt.ylabel('Term Rank')
    plt.title('Zipf\'s Law - Cumulative Count of First 100 Terms')
    plt.show()
    
    # plot log-log graph to display that Zipf's law is a power law
    x = np.log(np.arange(len(freqs)))
    y = np.log(freqs)
    plt.plot(x, y)
    plt.xlabel('log(Term Rank)')
    plt.ylabel('log(Term Frequency)')
    plt.title('Zipf\'s Law: Log-Log Plot')
    plt.show()
    
zipf_analysis('mobydick.txt')
