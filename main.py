import math


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


def da_range(set, attribute):
    sort_by(set, attribute)
    r = float(set[len(set)-1][attribute]) - float(set[0][attribute])
    #print("Min:", float(set[0][attribute]), "Max:", float(set[len(set)-1][attribute]))
    return r


def discreeett(dat, num_of_bins, attribute):
    sort_by(dat, attribute)
    bin_size = len(dat) / num_of_bins
    for i in range(len(dat)):
        num = int(i / bin_size) + 1
        dat[i][attribute] = num
    return dat


def binify(set, bins, attribute):
    i = 0
    binz = []
    sort_by(set, attribute)
    ran = da_range(set, attribute)
    interval = float(ran) / float(bins)
    #print("Interval:", interval)
    chart = []
    cutoff = float(set[0][attribute]) + interval
    #print("Cutoff:", cutoff)

    begin = 0
    end = 0
    num_of_appends = 0
    for elem in set:
        #print("comparing", float(elem[attribute]), "and", cutoff, "i =", i)
        if (float(elem[attribute]) > cutoff) & (num_of_appends + 1 < bins):
            end = i
            binz.append(set[begin:end])
            num_of_appends = num_of_appends + 1
            #print("appending range", begin, "and", end)
            begin = end
            cutoff = cutoff + interval
            #print("new cutoff", cutoff)
        i = i + 1
    binz.append(set[begin:len(set)])
    return binz


def how_many(set, element, kind):
    num = 0
    for s in set:
        #print(s[element], "vs", kind)
        if int(s[element]) == int(kind):
            num = num + 1
    return num


def entrofy(set, attribute): #dont need the attribute
    p0 = (float(how_many(set, 2, 0)) / float(len(set)))
    p1 = (float(how_many(set, 2, 1)) / float(len(set)))
    #print(how_many(set, 2, 0), float(len(set)), p0, how_many(set, 2, 1), float(len(set)), p1)
    if p0 == 0.0:
        entropy = 0
    elif p1 == 0.0:
        entropy = 0
    else:
        entropy = float(-(float(p0) * float(math.log2(p0))) - (float(p1) * float(math.log2(p1))))
    return entropy


def gainz(dt, bz):
    col_entropy = 0
    tot = float(len(dt))
    for asdf in bz:
        ent = entrofy(asdf, 2)
        #print("Entropy:", ent)
        col_entropy += ent * float(len(asdf)) / tot
    return entrofy(dt, 2) - col_entropy


def remove_column(da_set, col_num):
    temp = []
    for elem in da_set:
        temp_elem = []
        for i in range(0, len(elem)):
            if i != col_num:
                temp_elem.append(elem[i])
        temp.append(temp_elem)
    return temp


def rucursiv(parent, depth):
    if depth == 3:
        print("leaf?")
    else:
        print("depth:", depth)
        bins = 5
        gain_so_far = 0
        highest_gain_col_index = -1;
        for i in range(0, len(parent[0]) - 1):
            benz = binify(parent, bins, i)
            rez = gainz(parent, benz)
            if rez > gain_so_far:
                gain_so_far = rez
                highest_gain_col_index = i
        print("highest info gain from column", highest_gain_col_index)
        print("splitting on column", highest_gain_col_index)
        benz = binify(parent, bins, highest_gain_col_index)
        depth += 1
        i = 1
        for b in benz:
            print("entering column", highest_gain_col_index, "branch", i, "wish me luck...")
            i += 1
            b = remove_column(b, highest_gain_col_index)
            print(b)
            rucursiv(b, depth)



def main():
    f = open("synthetic-1.csv", 'r')
    #f = open("test.csv", 'r')
    data = []
    for line in f:
        entry = line.split(",")
        entry[len(entry)-1] = entry[len(entry)-1][:-1]
        entry[0] = float(entry[0])
        entry[1] = float(entry[1])
        entry[2] = int(entry[2])
        data.append(entry)
    #print(data)
    sort_by(data, 0)
    #print(data)
    sort_by(data, 1)
    #print("lenght of data", len(data))
    bins = 5
    #print("Range 0:", da_range(data, 0))
    print(data)
    data = discreeett(data, 4, 0)
    print(data)
    data = discreeett(data, 5, 1)
    print(data)
    benz = binify(data, bins, 0)
    rez = gainz(data, benz)
    #print("info gain col 0:", rez)
    benz = binify(data, bins, 1)
    rez2 = gainz(data, benz)
    #print("info gain col 1:", rez2)
    visited = []
    #rucursiv(data, 1)
    data1 = remove_column(data, 0)
    #print(data1)

    #for asdf in benz:
        #print(len(asdf), "->", asdf)
        #ent = entrofy(asdf, 2)
        #print("Entropy:", ent)


if __name__ == '__main__': main()
