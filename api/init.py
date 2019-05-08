import json

def parsePackageList():
    with open("./../data100.txt", 'r') as f:
        documents = []
        for i in f.readlines():
            for c in '[],\n': #':-/@.'
                i = i.replace(c, ' ')
            documents.append(i)
    with open("./package/package.dat", 'w') as f:
        for line in documents:
            f.write(line + '\n')

def parseDescriptions():
    with open("./../popular_package.json", 'r') as f:
        packages = json.loads(f.readline())
    descriptions = []
    parsed_packages = []
    for p in packages:
        try:
            p["des"].encode('ascii')
        except:
            print(p)
        else:
            descriptions.append(p['des'] + ' ' + p["title"])
            titles.append(p["title"])
            parsed_packages.append(p)
    with open("./description/description.dat", 'w') as f:
        for line in descriptions:
            f.write(line + '\n')
    with open("./parsed_packages.json", 'w') as f:
        f.write(json.dumps(parsed_packages))
