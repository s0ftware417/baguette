import math
import csv
import time
# import matplotlib.pyplot as plt


def da_range(set, attribute):
    sort_by(set, attribute)
    r = float(set[len(set)-1][attribute]) - float(set[0][attribute])
    #print("Min:", float(set[0][attribute]), "Max:", float(set[len(set)-1][attribute]))
    return r


def copy(data):
    new = []
    for d in data:
        new.append(d)
    return new


def sort_by(set, attribute):
    for s in set:
        temp = s[0]
        s[0] = s[attribute]
        s[attribute] = temp
    set.sort()
    for s in set:
        temp = s[0]
        s[0] = s[attribute]
        s[attribute] = temp


def dis_shit(dat, num_of_bins, attribute): #####################################################
    binz = []
    sort_by(dat, attribute)
    range = float(set[len(dat)-1][attribute]) - float(dat[0][attribute])
    interval = float(range) / float(num_of_bins)


def discreeett(dat, num_of_bins, attribute):
    sort_by(dat, attribute)
    #
    # partition_point = len(dat)/num_of_bins
    #
    # label = 1
    # counter = 1
    # for data_point in dat:
    #     if counter <= partition_point:
    #         data_point[attribute] = label
    #     else:
    #         partition_point += partition_point
    #         label += 1
    #         data_point[attribute] = label
    #     counter += 1
    # return dat

    bin_size = len(dat) / num_of_bins
    for i in range(len(dat)):
        num = int(i / bin_size) + 1
        dat[i][attribute] = num
    return dat


def options(data):
    big = []
    for i in range(len(data[0])):
        column = [row[i] for row in data]
        columnSet = set(column)
        #print(list(columnSet))
        YEEE = list(columnSet)
        big.append(YEEE)
    #print(big)
    return big

def unique(data, column):
    unique = []
    for d in data:
        if d[column] not in unique:
            unique.append(d[column])
    return unique


def split(data, attribute): #could make this more efficient by sorting
    splitt = []
    uni = unique(data, attribute)
    for n in uni:
        temp = []
        for entry in data:
            if n == entry[attribute]:
                temp.append(entry)
        if len(temp) > 0:
            splitt.append(temp)
    return splitt


def how_many(dat, kind):
    num = 0
    for s in dat:
        #print(s[len(dat[0])-1], "vs", kind)
        if s[len(dat[0])-1] == kind:
            num = num + 1
    return num

def number_at_index(dat, kind, index):
    num = 0
    for s in dat:
        #print(s[len(dat[0])-1], "vs", kind)
        if s[index] == kind:
            num = num + 1
    return num


def entrofy(da_set):
    tot = 0
    denom = len(da_set)
    uunique = unique(da_set, len(da_set[0])-1)
    for each in uunique:
        ratio = how_many(da_set, each)/denom
        #print("ration of", each, ":", ratio)
        if ratio != 0:
            ent = float(-(float(ratio) * float(math.log2(ratio))))
            tot += ent
            #print("\tadding", ent, "total is", tot)
    return tot


def gainz(dt, att):

    col_entropy = 0
    tot = float(len(dt))
    div = split(dt, att)
    for asdf in div:
        ent = entrofy(asdf)
        #print("Entropy:", ent)
        col_entropy += ent * float(len(asdf)) / tot
    return entrofy(dt) - col_entropy


def remove_column(da_set, col_num):
    temp = []
    for elem in da_set:
        temp_elem = []
        for i in range(0, len(elem)):
            if i != col_num:
                temp_elem.append(elem[i])
        temp.append(temp_elem)
    return temp


def tabs(num):
    for i in range(num*2):
        print("\t", end="")


def rucursiv(parent, depth, visited):
    if depth >= 3:
        tot = len(parent)
        majority = ""
        percent = 0
        if tot > 0:
            for item in unique(parent, len(parent[0])-1):
                new_percent = how_many(parent, item) / tot
                if new_percent >= percent:
                    percent = new_percent
                    majority = item
            tabs(depth)
            print("Guessing... |||", majority, "|||", percent * 100, "% sure...", visited)
            return majority
    else:
        tabs(depth)
        gain_so_far = 0
        highest_gain_col_index = -100
        for i in range(0, len(parent[0]) - 1):
            if i not in visited:
                rez = gainz(parent, i)
                if rez >= gain_so_far:
                    gain_so_far = rez
                    highest_gain_col_index = i
        if gain_so_far == 0:
            print("|||", parent[0][len(parent[0])-1], "|||")
            return parent[0][len(parent[0])-1]
        elif gain_so_far < 0:
            print("im so fucked...")
        else:
            asdfasdf = []
            asdfasdf.append(highest_gain_col_index)
            tabs(depth-1)
            print("splitting on index", highest_gain_col_index)
            div = split(parent, highest_gain_col_index)
            visited.append(highest_gain_col_index)
            depth += 1
            lit = []
            for b in div:
                extra = []
                tabs(depth)
                print(b[0][highest_gain_col_index], "- size:", len(b))
                extra.append(b[0][highest_gain_col_index])
                for_now = rucursiv(b, depth, visited)
                extra.append(for_now)
                lit.append(extra)
            asdfasdf.append(lit)
            return asdfasdf


def traversal(listt, entry):
    if type(listt) != list:
        return listt
    else:
        index = -1
        i = 0
        for elem in listt[1]:
            a = elem[0]
            b = entry[int(listt[0])]
            if a == b:
                index = i
            i += 1
        return traversal(listt[1][index][1], entry)


def disc_ranges(original, already_disc, record, attribute):
    count = []
    for item in record[attribute]:
        c =number_at_index(already_disc, item, attribute)
        count.append(c)
    sort_by(original,attribute)
    end = 0
    ranges = []
    for amm in count:
        entry = []
        begin = end
        end += amm
        #print(begin, end)
        entry.append(original[begin][attribute])
        entry.append(original[end-1][attribute])
        ranges.append(entry)
    return ranges


def categorize(input, disc_attribute_ranges, attribute):
    closest = 100000000000
    index = -1
    i = 1
    for elem in disc_attribute_ranges[attribute]:
        if abs(input - elem[0]) < closest:
            closest = abs(input - elem[0])
            index = i
        if abs(input - elem[1]) < closest:
            closest = abs(input - elem[1])
            index = i
        i += 1
    return index


def boxes(ranges, tree, bins):
    boxes = []
    print("splitting on", tree[0])
    for middle in tree[1]:
        #print(middle)
        xindex = middle[0]-1
        x_min = ranges[tree[0]][xindex][0]
        x_max = ranges[tree[0]][xindex][1]
        print("attribute", tree[0], "range(x) from", ranges[tree[0]][xindex][0], "to", ranges[tree[0]][xindex][1])
        if type(middle[1]) != list:
            other = 0
            if tree[0] == 0:
                other = 1
            print("\ty range from", ranges[other][0][0], "to", ranges[other][len(ranges[other])-1][1])
            y_min = ranges[other][0][0]
            y_max = ranges[other][len(ranges[other])-1][1]
            rec = [x_min, y_min, x_max - x_min, y_max - y_min, middle[1]]
            boxes.append(rec)

        else:
            for inner in middle[1][1]:
                yindex = inner[0] - 1
                print("inner:", inner)
                y_min = ranges[middle[1][0]][yindex][0]
                y_max = ranges[middle[1][0]][yindex][1]
                print("\tattribute", middle[1][0], "range(y) from", ranges[middle[1][0]][yindex][0], "to", ranges[middle[1][0]][yindex][1])
                rec = [x_min, y_min, x_max - x_min, y_max - y_min, inner[1]]
                boxes.append(rec)
    return boxes


def main():
    f = open("Video_Games_Sales.csv", 'r') #<------------- this shit's important , use it
    first_line = f.readline()
    data = list(csv.reader(f))
    visited = []
    tree = rucursiv(data, 1, visited)
    print("tree ->", tree)
    wins = 0
    for m in data:
        if traversal(tree, m) == m[len(m) - 1]:
            wins += 1
    print("percent correct predictions:", int(100 * float(wins / len(data))))


if __name__ == '__main__': main()