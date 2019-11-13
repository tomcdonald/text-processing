
# COM3110/4155/6155: Text Processing
# Regular Expressions Lab Class

import sys, re

#------------------------------

testRE = re.compile('(logic|sicstus)', re.I)
htmlRE = re.compile('<.*?>', re.I)
pairRE = re.compile(r'<(.*?)>(.*?)</\1>', re.I)
linkRE = re.compile(r'<a(.*?)>(.*?)</a>', re.I)

#------------------------------

with open('RGX_DATA.html') as infs: 
    linenum = 0
    for line in infs:
        linenum += 1
        if line.strip() == '':
            continue
        #print('  ', '-' * 100, '[%d]' % linenum, '\n   TEXT:', line, end='')
    
# =============================================================================
#         m = testRE.search(line)
#         if m:
#             print('** TEST-RE:', m.group(1))
# =============================================================================

# =============================================================================
#         mm = testRE.finditer(line)
#         for m in mm:
#             print('** TEST-RE:', m.group(1))
# =============================================================================

# =============================================================================
# # Q1 - Find HTML Tags
#         mm = htmlRE.findall(line)
#         for m in mm:
#             print('** TAG:', m)
# =============================================================================

# =============================================================================
# # Q2 - Differentiate Open/Close HTML Tags
#         mm = htmlRE.findall(line)
#         for m in mm:
#             if m[1] == '/':
#                 print('** CLOSETAG:', m)
#             else:
#                 print('** OPENTAG:', m)
# =============================================================================

# =============================================================================
# # Q3 - Make Pattern Print Tag & Params
#         mm = htmlRE.findall(line)
#         for m in mm:
#             terms = m.strip('<>/').split()
#             if m[1] == '/':
#                 print('\n** CLOSETAG:', terms[0])
#             else:
#                 print('\n** OPENTAG:', terms[0])
#             if len(terms) > 1:
#                     for param in terms[1:]:
#                         print('    PARAM:', param)
# =============================================================================
                
# =============================================================================
# # Q4 - Use Backreferences to Recognise Paired HTML Tags on Same Line
#         mm = pairRE.findall(line)
#         for m in mm:
#             print('** PAIR [', m[0], ']:', m[1])
# =============================================================================
        
# Q5 - Find Links, Printing the href and Link Text Separately
        mm = linkRE.findall(line)
        for m in mm:
            link = m[0].lower()
            text = m[1]
            print('** LINK:', link[6:])
            print('   TEXT:', text, '\n')
        
# =============================================================================
# # Q6 - Strip HTML from all Lines of Text
#         stripped = htmlRE.sub('', line)
#         print('** STRIPPED:', stripped)
# =============================================================================
                
                