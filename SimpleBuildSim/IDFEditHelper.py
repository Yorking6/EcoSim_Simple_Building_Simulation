
def read_idf_to_dict(idf_file_path):
    # 1. read idf file into list of lines
    idf_file = open(idf_file_path, "r")
    idf_lines = idf_file.readlines()
    idf_file.close()
    # 2. prepare temporary variables before do parsing
    idf_dict = {} # the structure is:
                  # {object_name: [[object contents 1], [object contents 2], ...]}
    obj_end = True # this flag becomes True when reaching ";", otherwise it is False
    current_obj_name = None # temporarily remember object name
    current_obj_content = [] # temporarily store the current object contents
    # 3. read through all lines in the idf file
    for idf_line in idf_lines:
        idf_line = idf_line.strip() # remove leading and tailing blank spaces of a line
        if len(idf_line) > 0: # ignore empty lines
            # 4. separate comment and non-comment code (anything after ! is comment)
            idf_line_eles = idf_line.split('!')
            idf_line_effective = idf_line_eles[0]
            if len(idf_line_eles) > 1:
                idf_line_comment = '!' + idf_line_eles[1]
            else:
                idf_line_comment = ''
            # 5. parse the code
            if len(idf_line_effective) > 0:
                idf_line_effective = idf_line_effective.strip() # remove leading and tailing empty spaces of a line
                line_eles = idf_line_effective.split(',') # separate the line by ",", elements are separated by "," 
                # 6. parse each element separated by ','
                for line_ele_i in range(len(line_eles)):
                    line_ele = line_eles[line_ele_i]
                    if obj_end: # if obj_end flag is True, then this element represents the new object name
                        if line_ele not in idf_dict:
                            idf_dict[line_ele] = [] # initiate a new empty list if this is a fresh new object
                        current_obj_name = line_ele
                        obj_end = False
                    else: # if obj_end flag is not True, then this element is the part of the object
                        # 7.1 if reaching the object end
                        if ';' in line_ele: 
                            line_ele_effective = line_ele.split(';')[0].strip() + idf_line_comment
                            current_obj_content.append(line_ele_effective)
                            # this is end of an object, so append the object contents to the list
                            idf_dict[current_obj_name].append(current_obj_content)
                            obj_end = True
                            current_obj_name = None
                            current_obj_content = []
                        # 7.2 if not reaching the object end
                        else:
                            line_ele_effective = line_ele.strip()
                            # the element is not valid content if the length of the element is zero and 
                            # this is not the first element separated by ','
                            if line_ele_i == 0 or len(line_ele_effective) > 0:
                                line_ele_effective += idf_line_comment
                                current_obj_content.append(line_ele_effective)
    return idf_dict
                    

def write_dict_to_idf(idf_dict, idf_write_path):
    new_idf_lines = []
    # 1. loop through all class names in the idf dict
    for idf_obj in idf_dict:
        obj_contents = idf_dict[idf_obj]
        # 2. loop through all objects under this class
        for obj_content in obj_contents:
            new_idf_lines.append(idf_obj + ',\n') # add a line sepration symbol
            # 3. loop through all elements in the object
            for i in range(len(obj_content)):
                obj_line = obj_content[i]
                if i < len(obj_content) - 1: # if not the last element in the object
                    if '!' in obj_line:
                        this_line = obj_line.split('!')[0] + ',' + '!' + obj_line.split('!')[1]
                    else:
                        this_line = obj_line + ','
                else: # if the last element in the object
                    if '!' in obj_line:
                        this_line = obj_line.split('!')[0] + ';' + '!' + obj_line.split('!')[1]
                    else:
                        this_line = obj_line + ';'
                new_idf_lines.append(this_line)
                new_idf_lines.append('\n')
            new_idf_lines.append('\n')
    idf_file_to_write = open(idf_write_path, "w")
    idf_file_to_write.writelines(new_idf_lines)
    idf_file_to_write.close()