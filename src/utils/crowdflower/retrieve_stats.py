import sys, csv, string

def generate_R_input(report_path, output_path):
    confidence_values = []
    report_file       = open(report_path, 'r')
    first_line = True
    for line in report_file:
        if first_line:
	    first_line = False
	    continue
        line = line.strip().split(',')
	if line[5]   == 'Yes':
	    confidence_values.append(line[6])
	elif line[5] == 'No':
	    confid = 1 - float(line[6])
	    confidence_values.append(confid)
    output_file = open(output_path, 'w')
    output_file.write('Confidence' + '\n')
    first_val = True
    for confid in confidence_values:
        if not first_val:
            output_file.write(str(confid) + '\n')
        else:
            output_file.write(str(confid) + '\n')
	    first_val = False
    output_file.close()


if __name__ =="__main__":
    _report_path = sys.argv[1]
    _output_path = sys.argv[2]

    generate_R_input(_report_path, _output_path)

