with open("./../data100.txt", 'r') as f:
    documents = []
    for i in f.readlines():
        for c in '[],\n': #':-/@.'
            i = i.replace(c, ' ')
        documents.append(i)
with open("./package.dat", 'w') as f:
    for line in documents:
        f.write(line + '\n')
