import json

def parsePackageList():
    with open("./../data100.txt", 'r') as f:
        documents = []
        for i in f.readlines():
            for c in '[],\n': #':-/@.'
                i = i.replace(c, ' ')
            documents.append(i)
    with open("./package.dat", 'w') as f:
        for line in documents:
            f.write(line + '\n')

with open("./../popular_package.json", 'r') as f:
    packages = f.readline()
    json.loads(packages)
# with open("./package.dat", 'w') as f:
#     for line in documents:
#         f.write(line + '\n')
