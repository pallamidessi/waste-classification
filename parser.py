import re

pattern_third_level = '(..) (..) (..+)'
pattern_second_level = '(..) (..)'
pattern_first_level = '(..)'

re_third_level = re.compile(pattern_third_level)
re_second_level = re.compile(pattern_second_level)
re_first_level = re.compile(pattern_first_level)

raw_data_path = "EPA_Waste_Classification_2015_Web.txt"

def skip(line):
    if line == "\n":
        return True
    else:
        return False

def parse_order(line):
    m = re_third_level.match(line)
    if m != None:
        return (3, int(m.group(1).lstrip("0")) - 1,\
                   int(m.group(2).lstrip("0")) - 1,\
                   int(m.group(3).lstrip("0").rstrip('*')) - 1) 

    m = re_second_level.match(line)
    if m != None:
        print(m.group(1))
        print(m.group(2))
        return (2, int(m.group(1).lstrip("0")) - 1,\
                   int(m.group(2).lstrip("0")) - 1)

    m = re_first_level.match(line)
    if m != None:
        return (1, int(m.group(0).lstrip("0")) - 1) 

if __name__ == "__main__":
    
    classification = []
    contextual_order = None
    current_title = ''
    NEXT_IS_TITLE = False 
    NEXT_IS_ORDER = True

    with open(raw_data_path) as f:
        for idx, line in enumerate(f):
            print(idx)
            if skip(line) == False:
                if NEXT_IS_TITLE:
                    current_title += line
                if NEXT_IS_ORDER:
                    contextual_order = parse_order(line)
                    NEXT_IS_TITLE = True
                    NEXT_IS_ORDER = False
            elif current_title != '' and NEXT_IS_TITLE:
                if (contextual_order[0] == 1):
                    print(contextual_order[1])
                    classification.append({'order': contextual_order[1],
                                                                'title': current_title,
                                                                'children': []})
                elif (contextual_order[0] == 2):
                    level_length = len (classification)
                    if level_length < contextual_order[1]:
                        for i in range(0, contextual_order[1] - (level_length - 1)):
                            classification.append({'order': level_length + i,
                                                   'title': '',
                                                   'children': []})

                    classification[contextual_order[1]]['children'].append({'order': contextual_order[2],
                                                                'title': current_title,
                                                                'children': []})
                elif (contextual_order[0] == 3):
                    level_length = len (classification)
                    if level_length <= contextual_order[1]:
                        print (level_length, contextual_order[1])
                        for i in range(0, contextual_order[1] - (level_length - 1)):
                            classification.append({'order': level_length + i,
                                                   'title': '',
                                                   'children': []})

                    level_length = len(classification[contextual_order[1]]['children'])
                    print (level_length, contextual_order[2])
                    if level_length  <= contextual_order[2]:
                        for i in range(0, contextual_order[2] - (level_length - 1)):
                            classification[contextual_order[1]]['children'].append({'order': level_length + i,
                                                                                    'title': '',
                                                                                    'children': []})

                    classification[contextual_order[1]]['children'][contextual_order[2]]\
                                                       ['children'].append({'order': contextual_order[3],
                                                                         'title': current_title})
                #print(classification)
                NEXT_IS_ORDER = True
                NEXT_IS_TITLE = False
                current_title = ''

            
