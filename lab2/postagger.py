"""
USE: python <PROGNAME> (options) 
OPTIONS:
    -h : print this help message and exit
    -d FILE : use FILE as data to create a new lexicon file
    -l FILE : create OR read lexicon file FILE
    -t FILE : apply lexicon to test data in FILE
"""
################################################################

import sys, re, getopt
import numpy as np

################################################################
# Command line options handling, and help

opts, args = getopt.getopt(sys.argv[1:],'hd:l:t:')
opts = dict(opts)

def printHelp():
    help = __doc__.replace('<PROGNAME>',sys.argv[0],1)
    print('-' * 60, help, '-' * 60, file=sys.stderr)
    sys.exit()
    
if '-h' in opts:
    printHelp()

if len(args) > 0:
    print("\n** ERROR: no arg files - only options! **", file=sys.stderr)
    printHelp()

if '-l' not in opts:
    print("\n** ERROR: must specify lexicon file name (opt: -l) **", file=sys.stderr)
    printHelp()

################################################################

# 5 - CREATING TERM-POSTAG-COUNT DICTIONARY
    
def create_dict(filename):
    token_dict = {}
    with open(filename) as f:
        for line in f:
            for token in line.split():
                word = token.split('/')[0]
                pos = token.split('/')[1]
                if word not in token_dict:
                    token_dict[word] = {}
                if pos not in token_dict[word]:
                    token_dict[word][pos] = 0
                token_dict[word][pos] += 1
    return token_dict
        
#term_postag_count = create_dict(opts['-l'])

# 6 - PROCESSING TERM-POSTAG-COUNT DICTIONARY #######################

# function for q.6a
def count_pos_tags(print_6a=True):
    term_postag_count = create_dict(opts['-l'])
    all_pos_tags = [list(x.keys()) for x in term_postag_count.values()]
    all_pos_tags_flat = [pos for sub_dict in all_pos_tags for pos in sub_dict]
    pos_tags = {}
    
    for tag in all_pos_tags_flat:
        if tag not in pos_tags:
            pos_tags[tag] = 0
        pos_tags[tag] += 1
    
    most_common_tag, most_common_count = None, None
    num_total_tags = 0
    for key, val in sorted(pos_tags.items(), key=lambda v:v[1], reverse=True):
        if print_6a == True:
            print(key, val)
        num_total_tags += val
        if most_common_tag == None:
            most_common_tag = key
            most_common_count = val
    if print_6a == True:
        print('Naiive accuracy from classifying every word as NNP:',
              round(most_common_count / num_total_tags, 3))
        
#count_pos_tags()

# function for q.6b
def ambiguous(print_6b=True):
    term_postag_count = create_dict(opts['-l'])
    ambiguous_terms = []
    num_tokens = 0
    num_ambig_tokens = 0
    for key in term_postag_count.keys():
        num_tokens += sum(term_postag_count[key].values())
        if len(term_postag_count[key]) > 1:
            ambiguous_terms.append(term_postag_count[key])
            num_ambig_tokens += sum(term_postag_count[key].values())
    frac_ambig_terms = len(ambiguous_terms) / len(term_postag_count)
    frac_unambig_tokens = 1 - (num_ambig_tokens / num_tokens)
    print(round(frac_ambig_terms*100, 3), 
          '% of terms in lexicon are ambiguous')
    print(round(frac_unambig_tokens*100, 3), 
          '% of ALL tokens in the text are unambiguous')
    
#ambiguous()

# 8 & 9 - NAIIVE POS TAGGING ###############################

def naiive_pos(train=opts['-l'], test=None):
    term_postag_count = create_dict(train)
    with open(train) as f:
        correctly_tagged = 0
        total_tagged = 0
        for line in f:
            for token in line.split():
                word = token.split('/')[0]
                pos = token.split('/')[1]
                total_tagged += 1
                pos_pred = max(term_postag_count[word],
                               key=term_postag_count[word].get)
                if pos_pred == pos:
                    correctly_tagged += 1
    acc = correctly_tagged / total_tagged
    print('Accuracy of naiive method on training data =',
          round(acc*100, 3), '%')
    
    if test is not None:
        with open(test) as f:
            correctly_tagged_test = 0
            total_tagged_test = 0
            for line in f:
                for token in line.split():
                    word = token.split('/')[0]
                    pos = token.split('/')[1]
                    total_tagged_test += 1
                    if word in term_postag_count:
                        pos_pred = max(term_postag_count[word],
                                       key=term_postag_count[word].get)
                        if pos_pred == pos:
                            correctly_tagged_test += 1
        acc_test = correctly_tagged_test / total_tagged_test
        print('Accuracy of naiive method on test data =',
              round(acc_test*100, 3), '%')

naiive_pos(train=opts['-l'], test=opts['-t'])
    