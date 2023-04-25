with open("type_map.raw", "r") as f:
    lines = f.readlines()
    # remove any leading/trailing whitespaces and newlines
    lines = [line.strip() for line in lines]
    # create a list of lists, where each inner list contains one element from each line
    data = [line.split() for line in lines]
    # print the final list of lists
    print(data)
