import pandas as pd
import random
import argparse
import sys
from datetime import datetime

#Setup argparse
parser = argparse.ArgumentParser()
parser.add_argument('-rq', '--randomizequestion', default = False)
parser.add_argument('-ra', '--randomizeanswers', default = True)
parser.add_argument('-lb', '--linebreaks', default = 6)
parser.add_argument('-c', '--coursename', default = 'coursename')
parser.add_argument('-e', '--examname', default = 'examname')
parser.add_argument('-s', '--semester', default = 'semester')
parser.add_argument('-y', '--year', default = datetime.now().year)
parser.add_argument('-i', '--input')
parser.add_argument('-o', '--output')

args = parser.parse_args()

if args.input == None:
    print('Input file not specified. No output generated.')
    sys.exit()

if args.output == None:
    print('Output file not specified. No output generated.')
    sys.exit()

#Parameters

randomize_question_order = args.randomizequestion
randomize_answer_order = args.randomizeanswers
line_breaks_after_short = args.linebreaks
course_name = args.coursename
exam_name = args.examname
semester = args.semester
year = args.year

input_file = args.input
output_file = args.output

#Run
#Should not need to change anything below this line if you're ok with the default heading and styles
input = pd.read_csv(input_file, sep = '\t', encoding = 'latin1')
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

print(f'Exam text generated and available at {output_file}.')
print(f'To convert with pandoc, run pandoc {output_file} -s -o exam_1.md')
print('Then, run pandoc -f markdown exam_1.md -t pdf -o exam_1.pdf')