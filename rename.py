import os
import sys
from os import listdir
from os.path import isfile, join

path = sys.argv[1]
files = [f for f in listdir(path) if isfile(join(path, f))]
result = []
for i in range(0, len(files) - 1, 2):
    files[i] = join(path, files[i])
    files[i + 1] = join(path, files[i + 1])
    result.append(join(path, str(int(i / 2 + 1)) + '-0' + files[i][-4:]))
    result.append(join(path, str(int(i / 2 + 1)) + files[i + 1][-4:]))

for i in range(len(files)):
    os.rename(files[i], result[i])
