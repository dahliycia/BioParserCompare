#!python
all_list = open('author.idx', 'r')

all_lines = all_list.readlines()
used_str = []
used_file = open('test_structures.txt', 'w')


for n in range(0, len(all_lines)-1, 10000):
    line = all_lines[n]
    name = line[0:4]
    used_str.append(name)
    used_file.write(name + '\n')

used_file.close()