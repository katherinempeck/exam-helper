import pandas as pd
import random

#Parameters

randomize_question_order = False
randomize_answer_order = True
line_breaks_after_short = 6
course_name = 'Python 101'
exam_name = 'Quiz 1'
semester = 'Spring'
year = '2025'

input_file = "input/exam1.tsv"
output_file = "intermediate_files/exam_1.txt"

#Run
#Should not need to change anything below this line if you're ok with the default heading and styles
input = pd.read_csv(input_file, sep = '\t')
output = output_file
#Shuffle the TSV first to randomize questions (if parameter set to True)
if randomize_question_order:
    input = input.sample(frac = 1, ignore_index = True)
f = open(output, 'a', encoding="utf-8")

#Write a YAML header to control the typesetting when converting to PDF
#Right now, this just sets the font family to times and margins to 1 inch
yamlheader = '''---
fontfamily: times
geometry: margin=1in
---'''
f.write(yamlheader)

#Write a simple exam header with a space for the student's name and a heading with the course name, exam name, and semester
f.write('\nName:\n')
f.write('&nbsp;\n')
f.write('\n')
f.write(f'## **{course_name} - {exam_name}** *{semester} {year}* ') #Calls variables defined in parameters section above
f.write('&nbsp;\n')
f.write('\n')

#Iterate through the TSV and write each row as a question with specific formatting
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

#To convert with pandoc:
#pandoc intermediate_files/exam_1.txt -s -o intermediate_files/exam_1.md
#Then
#pandoc -f markdown intermediate_files/exam_1.md -t pdf -o output/exam_1.pdf