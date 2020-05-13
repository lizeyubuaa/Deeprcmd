file = open('/Users/crescendo/Projects/DouyinDataAnalyse/resource/wordbase/医疗raw.text')
ofile = open('/Users/crescendo/Projects/DouyinDataAnalyse/resource/wordbase/医疗.text', 'w')
lines = file.readlines()

for line in lines:
    position = line.find('\t')
    if position != -1:
        line = line[:position] + '\n'
    ofile.write(line)