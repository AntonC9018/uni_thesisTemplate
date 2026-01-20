import sys
import os

filePath = sys.argv[1]
segmentName = sys.argv[2]
language = os.path.splitext(filePath)[1].lstrip('.').lower()

if language in ['zig', 'js', 'cpp', 'c', 'java']:
    commentStringStart = '//'
    commentStringEnd = ''
elif language in ['bash', 'py']:
    commentStringStart = '#'
    commentStringEnd = ''
elif language in ['lua']:
    commentStringStart = '%'
    commentStringEnd = ''
else:
    raise Exception(f"Unsupported language {language}")

segmentBeginString = f"{commentStringStart} Segment {segmentName} begin{commentStringEnd}"
segmentEndString = f"{commentStringStart} Segment {segmentName} end{commentStringEnd}"

# Search for start and end of segment in the file
segmentBegin = -1
segmentEnd = -1
with open(filePath, "r") as fp:
    index = 0
    for line in fp:
        if segmentBeginString in line:
            segmentBegin = index
        if segmentEndString in line:
            segmentEnd = index
        index += 1

try:
    if segmentBegin == -1 or segmentEnd == -1:
        print(f"Segment {segmentName} not found in file {filePath}")
        exit(-1) # not actually sure this affects the error.

    print(f"\\inputminted[firstline={segmentBegin + 2},lastline={segmentEnd}]{{{language}}}{{{filePath}}}", flush=True)

# This error floods the output if you don't close the stderr at the end.
except (BrokenPipeError):
    sys.stderr.close()
