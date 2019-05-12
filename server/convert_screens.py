from __future__ import with_statement, print_function, unicode_literals
from __future__ import division
from __future__ import absolute_import
from builtins import str
from builtins import range
from builtins import object
import os.path
import re
import json

LEVELDIR = 'screens'
JSONDIR = 'jsonscreens'
TESTDIR = 'tests'

def main():
    for i in range(1,63):
        json_string = convert_level(i)
        with open(os.path.join(JSONDIR, 'screen{0}.json'.format(i)),'w') as jf:
            jf.write(json_string)

def convert_level(level_num):
    '''Return json representation of screen'''
    level_dict = {}     #will be populated by _section_parser
    filename = os.path.join(LEVELDIR, 'screen{0}.txt'.format(level_num))
    level_parser(filename, level_dict)
    rows = int(level_dict['num_rows'])
    cols = int(level_dict['num_cols'])
    author = level_dict.get('author', '')
    title = level_dict.get('title', '')

    json_dict = {
        'level_num':level_num,
        'title':title,
        'author':author,
        'time':int(level_dict['time']),
        'rows':rows,
        'cols':cols,
        'grid': [
            level_dict['grid_data'][irow] for irow in range(rows)
        ],
        'under_objects':[],
        'solution_score':0,
        'solution_count':0,
        'solution':'',
    }
    if 'solution' in level_dict:
        json_dict['solution'] = ''.join(level_dict['solution'])
        json_dict['solution_score'] = level_dict['solution_score']
        json_dict['solution_count'] = level_dict['solution_moves']

    if 'under_objects' in level_dict:
        json_dict['under_objects'] = level_dict['under_objects']

    return json.dumps(json_dict)


def get_screenfile_lines(level_file):
    '''Open the file, trying several different directory locations.
    return the lines read'''
    lines = []
    try:
        with open(os.path.join(LEVELDIR, level_file), 'r') as lf:
            lines = lf.readlines()
    except FileNotFoundError:
        # try the tests directory
        try:
            with open(os.path.join(TESTDIR, level_file), 'r') as lf:
                lines = lf.readlines()
        except FileNotFoundError:
            # try finding the file in the local directory
            with open(level_file, 'r') as lf:
                lines = lf.readlines()
    return lines

def level_parser(level_file, level_dict):
    '''read input file and populate level_dict with section info'''
    lines = get_screenfile_lines(level_file)
    # match the first line of form "40x17", or "40 x 17"
    match = re.search(r'(\d+)\s*[xX]\s*(\d+)', lines[0])
    num_cols, num_rows = int(match.group(1)), int(match.group(2))
    lines = lines[1:] # move past first line now
    grid_data = [line.rstrip('\r\n') for line in lines[:num_rows]]
    lines = lines[num_rows:]
    #Some old files assume space padding at end of incomplete lines.
    for i in range(num_rows):
        length_delta = num_cols-len(grid_data[i])
        if length_delta > 0:
            grid_data[i] += ' '*length_delta
    assert num_rows == len(grid_data), "Incorrect number of rows in screen file"
    #I only test the first line here -- could need DEBUG in future
    assert num_cols == len(grid_data[0]), "Incorrect number of columns in screen file"
    #Check if Edge (or Wrapping_Edge) objects already there. If not, insert
    if grid_data[0][0] not in ['E', 'e', 'W', 'w']:
        #Insert Edge objects around the perimeter
        for i in range(len(grid_data)):
            grid_data[i] = 'E' + grid_data[i] + 'E'
        edgerow = 'E' * (num_cols+2)
        grid_data.insert(0, edgerow)
        grid_data.append(edgerow)
        num_rows += 2
        num_cols += 2
    level_dict['num_rows'] = num_rows
    level_dict['num_cols'] = num_cols
    level_dict['grid_data'] = grid_data
    level_dict['under_objects'] = []
    in_solution = False
    for line in lines:
        lowline = line.lower().strip()
        if in_solution:
            if first_solution_line:
                first_solution_line = False
                numbers = lowline.split()
                level_dict['solution_score'] = int(numbers[0])
                level_dict['solution_moves'] = int(numbers[1])
                solution = []
            elif lowline.startswith('end solution:'):
                in_solution = False
                level_dict['solution'] = solution
            else:
                solution.extend(line.strip())
        elif lowline.startswith('solution:'):
            in_solution = True
            first_solution_line = True
        elif lowline.startswith('time:'):
            level_dict['time'] = int(lowline.split(':')[-1])
        elif lowline.startswith('author:'):
            level_dict['author'] = line.split(':')[-1].strip()
        elif lowline.startswith('title:'):
            level_dict['title'] = line.split(':')[-1].strip()
        elif lowline.startswith('under:'):
            under_dict = {}
            rhs = line.split(':')[-1].strip()
            rhslist = rhs.split(',')
            assert len(rhslist) >= 3
            under_dict['type'] = rhslist[0]
            under_dict['location'] = (int(rhslist[1]), int(rhslist[2]))
            if len(rhslist) >= 5:
                under_dict['wall_vector'] = (int(rhslist[3]), int(rhslist[4]))
            level_dict['under_objects'].append(under_dict)
        else:
            pass


if __name__ == '__main__':
    main()
