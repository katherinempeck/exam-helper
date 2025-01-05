import pandas as pd
import random

#Parameters

randomize_question_order = True
randomize_answer_order = True
line_breaks_after_short = 6

input = pd.read_csv("input/exam1.tsv", sep = '\t')
output = 'intermediate_files/exam_1.txt'

#Run
if randomize_question_order:
    input = input.sample(frac = 1, ignore_index = True)
f = open(output, 'a', encoding="utf-8")

yamlheader = '''---
fontfamily: times
geometry: margin=1in
---'''
f.write(yamlheader)

f.write('\nName:\n')
f.write('&nbsp;\n')
f.write('\n')
f.write('## **Course Name - Exam Name** *Semester Year* ')
f.write('&nbsp;\n')
f.write('\n')

for index, row in input.iterrows():
    if row['class'] == 'multiple':
        q = row['question']
        a = row['parts'].split(';')
        if randomize_answer_order:
            random.shuffle(a)
        f.write(f'{index + 1}\. {q}\n')
        f.write('\n')
        for i, ans in enumerate(a):
            lab = chr(i + 97)
            f.write(f'{lab}. {ans}\n')
        f.write('\n')
    elif row['class'] == 'short-single':
        q = row['question']
        f.write(f'{index + 1}\. {q}')
        f.write('\n')
        n = 0
        while n < line_breaks_after_short:
            f.write('&nbsp;\n')
            f.write('\n')
            n += 1
        f.write('\n')
    elif row['class'] == 'short-multi':
        q = row['question']
        f.write(f'{index + 1}\. {q}\n')
        f.write('\n')
        parts = row['parts'].split(';')
        for ix, p in enumerate(parts):
            lab = chr(ix + 97)
            f.write(f'{lab}. {p}\n')
            f.write('\n')
            f.write('&nbsp;\n')
            f.write('\n')
            f.write('&nbsp;\n')
            f.write('\n')
            f.write('&nbsp;\n')
            f.write('\n')
        f.write('\n')
    elif row['class'] == 'match':
        f.write(f'{index + 1}\. {row["question"]}')
        f.write('\n')
        f.write('\n')
        opt_def = row['parts'].split('|')
        opt = opt_def[0].split(';')
        defi = opt_def[1].split(';')
        if randomize_answer_order:
            random.shuffle(opt)
            random.shuffle(defi)
        for o, d in zip(opt, defi):
            lab = chr(opt.index(o) + 97)
            f.write(f'{lab}. {o} &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; ____ {d}\n')
            f.write('\n')

#Convert with pandoc:
#pandoc intermediate_files/exam_1.txt -s -o intermediate_files/exam_1.md|pandoc -f markdown intermediate_files/exam_1.md -t pdf -o exam_1.pdf