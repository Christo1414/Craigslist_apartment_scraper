''' remove_duplicates.py
This script will iterate through the csv list and create a new file which
only contains entries with unique values in the link attribute.

This script can be imported for use of the following function:
    * remove_duplicates(infile)
'''


def remove_duplicates(infile):

    print("Removing duplicate entries...")
    outfile = infile[0:infile.find('.')] + "_nodups.csv"

    with open(infile,'r') as in_file, open(outfile,'w') as out_file:
    
        seen = set() 
        duplicates = 0
        for line in in_file:
            if line =='\n':
                continue # skip empty lines
            line_list = line.split(",")
            if line_list[-1] in seen:
                duplicates+=1
                continue # skip duplicate

            seen.add(line_list[-1])
            out_file.write(line)
    print("number of duplicates removed: " + str(duplicates))
    in_file.close()
    out_file.close()

    return outfile