#!/usr/bin/env python   


from os import write
import argparse
import re 
# import Bioinfo

#argparse arguements 
def get_args():             
    """This function passes arguements to a python script to"""
    parser = argparse.ArgumentParser(description="A program remove PCR Duplicates from SAM files")
    parser.add_argument("-f", "--filename", help="Your filename", required=True)               
    parser.add_argument("-p", "--paired", help="paired end", required=False, type=bool)
    parser.add_argument("-u", "--umi", help="UMI file?", required=False,)
    #parser.add_argument("-h", "--help", help="help?", required=False, action=help)
    parser.add_argument("-o", "--output", help="what is your outputfile?", required=True)
    #parser.add_argument("-o2", "--output2", help="what is your duplicate outputfile?", required=True)
    return parser.parse_args()
	
args = get_args()    
filename = (args.filename)
paired = (args.paired)
umi = (args.umi)
#help = (args.help)
output = (args.output)
#output2 = (args.output2)

# Include the following argparse options
#     - ```-f```, ```--file```: required arg, absolute file path 
#     - ```-p```, ```--paired```: optional arg, designates file is paired end (not single-end)
#     - ```-u```, ```--umi```: optional arg, designates file containing the list of UMIs (unset if randomers instead of UMIs)
#     - ```-h```, ```--help```: optional arg, prints a USEFUL help message (see argparse docs)
#         - If your script is not capable of dealing with a particular option (ex: no paired-end functionality), your script should print an error message and quit

umi_dict = {}

with open(umi, "r") as umi:
    for line in umi:
        line=line.strip() 
        umi_dict[line]=[""]
umi.close()
#print(umi_dict)  #dictionary of umi's looking good 

def numParser(s):
    try:
        return int(s)
    except ValueError:
        return s

def reverse_numParser(s):
    try:
        return str(s)
    except ValueError:
        return s

def numSummer(list):
    the_sum=0
    for x in list:
        if isinstance(x, str):
            pass
        elif isinstance(x, int):
            the_sum += x
    return(the_sum)

# 1S71M
# 1S71M
# 72M
# 72M
excig1="1S71M"
# 3S69M
# 1S71M
# 71M1S
excig2="1S17M931781N54M1S"
# 72M
excig3="72M"
# 1S71M
# 22M15110N50M

#make cigar fxn here: 


#test_list=[17,"93178M1",54,1]
#print("numsum test:", numSummer(test_list))

def cigar_parse(lst):
    lst=re.split(r'[S]', lst)
    lst=map(numParser, lst)
    lst=numSummer(lst)
    return(lst)

#print(cigar_parse(excig1))

def cigar_parse_rev(lst):
    #print(type(lst))
    first_s='S'    
    lst=re.findall(r'([0-9]+[A-Z])', lst)
    if first_s in lst[0]:
        lst.pop(0)
    lst="".join(lst[:])
    lst=str(lst)
    lst=re.findall(r'([0-9]+[A-Z])', lst)
    lst="".join(lst[:])
    # lst=str(lst)
    lst=re.sub(r'[0-9]+[I]','',lst)
    #lst=re.findall(r'([0-9]+[A-Z])', lst)
    # lst=re.sub(r'[A-Z]','',lst)
    lst=re.split(r'[A-Z]', lst)
    # print(lst)
    lst=map(numParser, lst)
    lst=list(lst)
    lst=numSummer(lst)
    return(lst)



# print(cigar_parse_rev(excig2))

main_dict={}
i=0 
dedup_count=0
with open(filename, "r") as fh: 
    with open(output, "w") as ffh:
        #with open(output2, "w") as o2: 
            for line in fh:
                
                while line.startswith("@"):
                    ffh.write(str(line))
                    line=fh.readline()
                    # print(line)
                # print(line)
                #print("Header:",header)
                
                i+=1
                # print("i is:", i)
                origin_line=line
                line=line.strip('\n').split("\t")
                # print(line)
                umihead=line[0]
                # print("umiheader",umihead)
                chrom=line[2]
                # print("chrom",chrom)
                pos=line[3]
                pos=int(pos)
                # print("pos:",pos)     # things looking good 
                cigar=line[5]
                # print("cigar",cigar)
                umihead=umihead.split(":")
                umihead=umihead[7] # got the umi's out 
                flag=int(line[1])
                # print(cigar)
                # print(flag)
                # if i == 10: 
                #     break
                if umihead not in umi_dict:
                    # print(umi_dict)
                    continue
                if((flag & 16) == 16):
                        #do cigar fuxns on reverse strand 
                        adjustment=cigar_parse_rev(cigar)
                        # print(adjustment)
                        adj_pos=(int(pos) + abs(int(adjustment)))
                else: 
                        # do cigar fxns on plus strand 
                        adjustment=cigar_parse(cigar)
                        # print(adjustment)
                        adj_pos=(int(pos) - abs(int(adjustment)))
                        
                # mapping to the dictionary 
                key = (umihead,  chrom, adj_pos, flag)
                if key not in main_dict:
                    main_dict[key]=[" "]
                    ffh.write(str(origin_line))
                else: 
                    dedup_count+=1
                if line == " ":
                    break
                    
                    
print("PCR duplicate line count:",dedup_count)


fh.close()
ffh.close()
#o2.close()

                ## Jason's advice 
                ## Draw out all the cases, soft clipping on both sides, etc 