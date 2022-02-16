
infile="test_visualization.csv"
outfile = infile[0:infile.find('.')] + "_nolinks.csv"

with open(infile,'r') as in_file, open(outfile,'w') as out_file:

    out_file.write(in_file.readline())
    lines = in_file.readlines()
    for line in lines:
        line_list = line.split(",")
        line_list[-1]  = "https://dummylink.com\n"
        line_nolink = ','.join(line_list)  

        out_file.write(line_nolink)
in_file.close()
out_file.close()


