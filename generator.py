# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


# Collating file to bugzilla components within subdirectories.


import sys

# Only look at this subdirectory.
baseDirName = "dom"

# Ignore paths containing any of these as a directory.
ignoreDirs = ["test", "tests", "crashtests"]

# Ignore paths with more directory components than this.
maxPathDepth = 2


# Show this many results for each subdirectory.
numCompToShow = 4


# Insert component |compName| for a file in directories |dirs| into map |m|.
def addFileComponent(compName, dirs, m):
    if not len(dirs):
        m = m.setdefault('', {})
        m[compName] = m.setdefault(compName, 0) + 1
        return

    m = m.setdefault(dirs[0], {})
    addFileComponent(compName, dirs[1:], m)


def showTopCounts(m, d):
    for x, v in m.iteritems():
        if x == '':
            l = [(count, comp) for (comp, count) in v.iteritems()]
            l.sort()
            l.reverse()

            lout = ', '.join(['{0} ({1})'.format(comp, count) for (count, comp) in l[:numCompToShow]])

            print '{0}: {1}'.format('/'.join(d), lout)
        else:
            d.append(x)
            showTopCounts(v, d)
            d.pop()


files = {}

for l in sys.stdin:
    splitAt = l.find(",")
    fileName = l[:splitAt]

    if not fileName.startswith(baseDirName):
        continue

    fileNameSplit = fileName.split("/")
    fileDirs = fileNameSplit[:-1]
    fileName = fileNameSplit[-1]
    compName = l[splitAt+1:].rstrip()

    ignore = False
    for d in ignoreDirs:
        if d in fileDirs:
            ignore = True
            break

    if ignore:
        continue

    if len(fileDirs) > maxPathDepth:
        continue

    addFileComponent(compName, fileDirs, files)


showTopCounts(files, [])

