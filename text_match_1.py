import re


def read_lines_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines


def find_matching_lines(file1_lines, file2_lines):
    matching_lines_file1 = []
    matching_lines_file2 = []

    for line1 in file1_lines:
        latlon_match = re.search(r'latlon\.(\d+\.\d+)', line1)
        if latlon_match:
            latlon_number = latlon_match.group(1)
            for line2 in file2_lines:
                testWave_match = re.search(r'testWave\.(\d+\.\d+)', line2)
                if testWave_match:
                    testWave_number = testWave_match.group(1)
                    if latlon_number == testWave_number:
                        matching_lines_file1.append(line1.strip())
                        matching_lines_file2.append(line2.strip())
                        break

    return matching_lines_file1, matching_lines_file2


def write_lines_to_file(file_path, lines):
    with open(file_path, 'w') as file:
        for line in lines:
            file.write(line + "\n")


def main():
    #file1path takes simulated lai file and file2path takes real lai file
    file1_path = "/exports/csce/datastore/geos/groups/MSCGIS/s2318635/240723/LAI/SIM_LAI.txt"
    file2_path = "/exports/csce/datastore/geos/groups/MSCGIS/s2318635/240723/rhovariation/rho0.11/real_LAI0.11rho.txt"

    file1_lines = read_lines_from_file(file1_path)
    file2_lines = read_lines_from_file(file2_path)

    matching_lines_file1, matching_lines_file2 = find_matching_lines(
        file1_lines, file2_lines)

    if matching_lines_file1:
        write_lines_to_file("/exports/csce/datastore/geos/groups/MSCGIS/s2318635/240723/rhovariation/rho0.11/SIM_LAI_matched_segmentsrho0.11.txt", matching_lines_file1)
        print("Matching lines from File 1 written")

    if matching_lines_file2:
        write_lines_to_file("/exports/csce/datastore/geos/groups/MSCGIS/s2318635/240723/rhovariation/rho0.11/REAL_LAI_matched_segmentsrho0.11.txt", matching_lines_file2)

        print("Matching lines from File 2 written")

    if not matching_lines_file1 and not matching_lines_file2:
        print("No matching lines found between the two files.")


if __name__ == "__main__":
    main()


# 