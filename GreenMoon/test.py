import sys
import os

path = os.path.dirname(os.path.realpath(__file__))

# orig_stdout = sys.stdout
file = open(path + '/templates/' + 'twitter_buffer.html', 'r')

# sys.stdout = file
# print(html)
# sys.stdout = orig_stdout

line_offset = []
offset = 0
for line in file:
    line_offset.append(offset)
    offset += len(line)
file.seek(0)
print(offset)
print(line_offset)
print(file.seek(1927))
print(file.readline())
# Now, to skip to line n (with the first line being line 0), just do
# print(file.seek(line_offset[43]))


file.close()