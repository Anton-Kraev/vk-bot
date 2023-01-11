import os
import sys
from os import listdir
from os.path import isfile, join

path = sys.argv[1]
files = [join(path, f) for f in listdir(path) if isfile(join(path, f))]

for i in range(0, len(files), 2):
    os.rename(files[i], files[i][:-5] + files[i][-4:])
    os.rename(files[i + 1], files[i + 1][:-4] + '-0' + files[i + 1][-4:])
    os.rename(files[i][:-5] + files[i][-4:], files[i][:-6] + files[i][-4:])

print(len(files))
