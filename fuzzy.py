import Levenshtein as Levenshtein
from fuzzywuzzy import fuzz



def fuzzy_search(search_name_list, bd_result):
    words = len(search_name_list)
    result_list = []
    if words == 1:
        for i in bd_result:
            srav_name = fuzz.ratio(search_name_list[0], i[1])
            srav_lastname = fuzz.ratio(search_name_list[0], i[2])
            if srav_name > 60 or srav_lastname > 60:
                result_list.append(i)

    else:
        name_in_search_str = search_name_list[0] + ' ' + search_name_list[1]
        for i in bd_result:
            srav = fuzz.WRatio(name_in_search_str, i[1] + ' ' + i[2])
            if srav > 50:
                result_list.append(i)
    if len(result_list) == 0:
        print("никого не нашел")
    return result_list


