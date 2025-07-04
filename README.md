# exam-helper
## Overview
This simple Python script, given a TSV (tab delimited file) with a specific format (see below), generates a text file in markdown language and formats the rows in the tsv into a typical exam format. This is not the only project out there for quick exam typesetting (the [LaTeX exam class](https://www.overleaf.com/learn/latex/Typesetting_exams_in_LaTeX) is a great option). But, if you have relatively simple exam formatting needs, want to be able to randomize questions and answers, and want to avoid repetitive copy/pasting, the script in this repo might be a good option for you.

## Requirements
* [Pandas](https://pandas.pydata.org/) (I wrote this using 2.0.3)
* Some way to convert a markdown file to your final desired format (I use [pandoc](https://pandoc.org/) with [MiKTeX](https://miktex.org/) as my LaTex distribution to convert the .md to a PDF)

## Input
The input for this script is a tsv with three columns:
* **class** - The kind of question being asked (```multiple```, ```short-single```, ```short-multi```, ```match```)
* **question** - The main question text
* **parts** - The answers/secondary question parts
* **image_ref** - TBD
* **pts** - TBD

TSVs can be created, for example, by exporting a .txt file (tab delimited) from Excel and changing the file extension on the exported file. 
 
Numbering in the output file is automatic and is based on the order of the questions in the tsv. If ```randomize_order``` is set to true, the rows will be shuffled before the exam is generated. An example TSV input can be found at ```input/exam1.tsv``` and intermediate text/markdown outputs can be found in the intermediate_files folder. The output pdf file (after conversion) is ```exam_1.pdf```.

### Multiple choice questions
In the class column, ```multiple``` refers to a multiple choice question. The question column will contain the question text and the parts column will contain the answers students can choose from, with each answer separated by a ```;```. 
 
### Single-part short-answer question
```short-single``` refers to a single-part short-answer question. The question column contains the question and the other columns are left blank.
 
The attribute ```line_breaks_after_short``` determines how many line breaks are created to make the short answer question space.

### Multi-part short-answer question
```short-multi``` refers to a multi-part short-answer question. The question column contains the main question and instructions, while the parts column contains the sub-questions, separated by ```;```.

### Matching
```match``` refers to a "matching" question composed of two column - one of e.g., vocabulary words and the other of definitions. The question column includes a description or a question, and the parts column contains the two sets of items to match. Within the column, the two sets are separated by a pipe ```|``` and the individual answers/definitions are separated by ```;```.

## Other formatting options
The script also generates a YAML header for the markdown file, specifying a font family of Times New Roman and a 1 inch margin. Other attributes could be added within the ```yamlheader``` variable to make other global adjustments to formatting.

## Running the script
The repository contains two scripts. Running ```generate_exam.py``` outputs a .txt file (with markdown syntax) capturing all questions in the input. To run, open the script in a Python environment with the required libraries installed. Then, edit the variables under the ```#Parameters``` header to match your input file, output file, and other attributes (e.g., course name).

Alternatively, the script ```generate_exam_CLI.py``` lets you run the script directly from the command line without having to edit the script. Open a terminal instance and activate your Python environment with the required libraries installed (I recommend Anaconda/Miniconda for managing Python libraries, but you can also use the ```venv``` module which is built in). Navigate to the folder containing the ```generate_exam_CLI.py``` script (i.e., this cloned repository). Then, run the command ```python generate_exam_CLI.py -i input.tsv -o output.txt``` replacing ```input.tsv``` with the filepath to your input file and replacing ```output.txt``` with the filename/location for saving your output text file. The ```-i``` and ```-o``` attributes are the minimum parameters you have to provide for the script to run. You can also set additional attributes:

* ```-rq```, randomize questions. Defaults to False. 
* ```-ra```, randomize answers. Defaults to False.
* ```-c```, course name. Defaults to "coursename" (this can be edited later in the text/markdown file, or set here)
* ```-e```, exam name. Defaults to "examname."
* ```-s```, semester. Defaults to "semester."
* ```-y```, year. Defaults to the current year (calculated using the ```datetime``` library).

For instance, running ```python generate_exam_CLI.py -i input.tsv -o output.txt` -rq True -c "Python 101"``` would generate the exam with randomized questions and a course name of "Python 101" (note that strings with spaces in them need to be enclosed in ""). 

## Render to PDF
Render the output text file to a markdown file using pandoc on the command line with ```pandoc intermediate_files/exam_1.txt -s -o intermediate_files/exam_1.md``` where ```intermediate_files/exam_1.txt``` is the output file name defined by ```generate_exam.py```. Then, convert the markdown to your desired output format using ```pandoc -f markdown intermediate_files/exam_1.md -t pdf -o exam_1.pdf```.  

## Other considerations
* Currently, this script does not have a good way to control for page breaks/dangling lines ("widows and orphans"). Converting to .docx or .odt rather than PDF allows for additional easy typesetting options like this (while still removing repetitive formatting tasks). 
* In the future, support will be added for linking included images using the image_ref column in the TSV. Right now, if you'd like to work with images, I recommend exporting to .docx, .odt, or .tex and manually adding them where needed.
* Currently, the **pts** column has no effect on exam typesetting and is simply included as a way for the user to track point totals. 
