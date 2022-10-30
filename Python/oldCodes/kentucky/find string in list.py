def findString(string_in_list,the_list):
    string_location = []
    for i in range(len(the_list)):
        if string_in_list in the_list[i]:
            string_location.append(i)
    return string_location