import csv
import json

data = []
problem_data = []

current_status = ['WITHDRAWN', 'ACTIVE', 'GRADUATED']
grade_status = ['FR', 'SO', 'JR', 'SR', '5TH']
min_gpa = 2.00
max_gpa = 4.00

with open('students.csv') as csvfile:
    readCSV = csv.reader(csvfile)
    data_header = next(readCSV)
    for row in readCSV:
        data.append(row)


class CleanData:

    def __init__(self):
        self.row = None
        self.col = None
        self.index = 0
        self.check_problems()

    def check_problems(self):
        # Create a copy of the data to go iterate through
        for row in data[:]:
            is_error = False
            for index, col in enumerate(row):
                self.col = col
                self.index = index
                if col == '' or self.check_type_specs():
                    is_error = True
            if is_error:
                problem_data.append(row)
                data.remove(row)

    def check_type_specs(self):
        # Return True if there is a problem with the row data
        if self.index == 0:
            try:
                int(self.col)
            except:
                return True
        elif self.index == 1 or self.index == 2 or self.index == 6:
            try:
                str(self.col)
            except:
                return True
        elif self.index == 3:
            try:
                str(self.col)
            except:
                return True
            if str(self.col).upper() not in current_status:
                return True
        elif self.index == 4:
            try:
                str(self.col)
            except:
                return True
            if str(self.col).upper() not in grade_status:
                return True
        elif self.index == 5:
            try:
                float(self.col)
            except:
                return True
            # Could check for absolute value -- Checks for decimals longer than 2 chars
            if min_gpa > float(self.col) or float(self.col) > max_gpa or float(self.col) != float(self.col).__round__(2):
                return True
        return False


def sort():
    temp = data.pop(0)
    data.sort(key=lambda x: x[2])
    data.insert(0, temp)


def json_write():
    json_data = {}
    json_data['students'] = []
    for row in data:
        json_data['students'].append({
            str(data_header[0]): row[0],
            data_header[1]: row[1],
            data_header[2]: row[2],
            data_header[3]: row[3],
            data_header[4]: row[4],
            data_header[5]: row[5],
            data_header[6]: row[6]})
    with open('students.json', 'w') as outfile:
        json.dump(json_data, outfile, indent=4)


def tab_write():
    with open('students.tsv', 'w') as outfile:
        for index, col in enumerate(data_header):
            if index < data_header.__len__() - 1:
                outfile.write(col + '\t')
            else:
                outfile.write(col + '\n')
        for row in data:
            for index, col in enumerate(row):
                if index == row.__len__() - 1 and row == data[data.__len__() -1]:
                    outfile.write(col)
                elif index < row.__len__() - 1:
                    outfile.write(col + '\t')
                elif index == row.__len__() - 1:
                    outfile.write(col + '\n')


# Initial Clean Using Provided Specifications
CleanData()

# Change Parameters For Advanced Search
min_gpa = 3.00
current_status = ['ACTIVE']

# Second Search Using Advanced Parameters
CleanData()

# Sort The Latest Data
sort()

# Write Data To Files
json_write()
tab_write()