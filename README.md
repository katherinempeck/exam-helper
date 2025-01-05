# exam-helper
## Overview
This simple Python script, given a TSV (tab delimited file) with a specific format (see below), generates a text file in markdown language formating the rows in the csv into a typical exam format.

## Input
The input for this script is a csv with three columns:
* **class** - The kind of question being asked (```multiple```, ```short-single```, ```short-multi```, ```match```)
* **question** - The main question text
* **parts** - The answers/secondary question parts
* **image_ref** - TBD
 
Numbering is automatic and is based on the order of the questions in the csv. If ```randomize_order``` is set to true, the rows will be shuffled before the exam is generated. Examples of tsv input can be found at ```input/exam1.tsv``` and intermediate text/markdown outputs can be found in the intermediate_files folder. The output pdf file (after conversion) is ```exam_1.pdf```.

### Multiple choice questions
In the class column, ```multiple``` refers to a multiple choice question. The question column will contain the question text and the parts column will contain the answers students can choose from, with each answer separated by a ```;```. 
 
### Single-part short-answer question
```short-single``` refers to a single-part short-answer question. The question column contains the question and the other columns are left blank.
 
The attribute ```line_breaks_after_short``` determines how many line breaks are created to make the short answer question space.

### Multi-part short-answer question
```short-multi``` refers to a multi-part short-answer question. The question column contains the main question and instructions, while the parts column contains the sub-questions, separated by ```;```.

### Matching
```match``` refers to a "matching" question composed of two column - one of e.g., vocabulary words and the other of definitions. The question column includes a description or a question, and the parts column contains the two sets of items to match. Within the column, the two sets are separated by a pipe (```|```) and the individual answers/definitions are separated by ```;```.

## Other formatting options
The script also generates a YAML header for the markdown file, specifying a font family of Times New Roman and a 1 inch margin. Other attributes could be added within the ```yamlheader``` variable to make other global adjustments to formatting.

## Output
Running ```generate_exam.py``` outputs a .txt file (with markdown syntax) capturing all questions in the input.

## Render to PDF
I render the output text file to a PDF using pandoc on the command line with ```pandoc intermediate_files/exam_1.txt -s -o intermediate_files/exam_1.md|pandoc -f markdown intermediate_files/exam_1.md -t pdf -o exam_1.pdf``` where ```input/exam_1.txt``` is the output file name defined in ```generate_exam.py```.