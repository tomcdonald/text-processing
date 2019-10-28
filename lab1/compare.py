"""\
------------------------------------------------------------
USE: python <PROGNAME> (options) file1...fileN
OPTIONS:
    -h : print this help message
    -b : use BINARY weights (default: count weighting)
    -s FILE : use stoplist file FILE
    -I PATT : identify input files using pattern PATT, 
              (otherwise uses files listed on command line)
------------------------------------------------------------
"""

import sys, re, getopt, glob, itertools

opts, args = getopt.getopt(sys.argv[1:], 'hs:bI:')
opts = dict(opts)
filenames = args

##############################
# HELP option

if '-h' in opts:
    progname = sys.argv[0]
    progname = progname.split('/')[-1] # strip out extended path
    help = __doc__.replace('<PROGNAME>', progname, 1)
    print(help, file=sys.stderr)
    sys.exit()

##############################
# Identify input files, when "-I" option used

if '-I' in opts:
    filenames = glob.glob(opts['-I'])

print('INPUT-FILES:', ' '.join(filenames))

##############################
# STOPLIST option

stops = set()
if '-s' in opts:
    with open(opts['-s'], 'r') as stop_fs:
        for line in stop_fs :
            stops.add(line.strip())

##############################
# 5/6 - TOKENISATION & COUNTING
            
def count_words(filenames):
    dicts = {}
    for file in filenames:
        words = {}
        with open(file) as f:
            for line in f:
                for word in re.findall(r'[\w]+', line.lower()):
                    if word not in stops:
                        if word not in words:
                            words[word] = 0
                        words[word]+=1
        dicts[file] = words
    return(dicts)
    
# 7 - COMPARISON
# 9 - COMPARE MULTIPLE FILES, PRINT TOP 10 SCORES

def compare_files(filenames):
    dicts = count_words(filenames)
    scores = {}
    for pair in itertools.combinations(filenames, 2):
        dict1, dict2 = dicts[pair[0]], dicts[pair[1]]
        dict1_keys = set(dict1.keys())
        dict2_keys = set(dict2.keys())
        intersect = dict1_keys & dict2_keys
        union = dict1_keys | dict2_keys
        simple_jaccard = round(len(intersect) / len(union), 4)
        
        # 8 - COUNT SENSITIVE JACCARD
        numerator, denominator = 0, 0
        for word in union:
            if word in dict1:
                count1 = dict1[word]
            else:
                count1 = 0
            if word in dict2:
                count2 = dict2[word]
            else:
                count2 = 0
            numerator += min([count1, count2])
            denominator += max([count1, count2])
        cs_jaccard = round(numerator / denominator, 4)
        print_str = pair[0] + ' <> ' + pair[1] + ' = '
        if '-b' in opts:
            scores[print_str] = cs_jaccard
        else:
            scores[print_str] = simple_jaccard
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    for score in sorted_scores[:10]:
        print(score[0], score[1])
        
compare_files(filenames)
