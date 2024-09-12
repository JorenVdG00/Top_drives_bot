
def find_differences(list1, list2):
    # Elements in list1 but not in list2
    only_in_list1 = [item for item in list1 if item not in list2]

    # Elements in list2 but not in list1
    only_in_list2 = [item for item in list2 if item not in list1]

    return only_in_list1, only_in_list2