#!/usr/bin/env python   

from os import write
import argparse
import re 
 
def get_args():             
    """This function passes arguements to a python script to"""
    parser = argparse.ArgumentParser(description="A program remove PCR Duplicates from SAM files")
    parser.add_argument("-f", "--filename", help="Your filename", required=True)               
    parser.add_argument("-p", "--paired", help="paired end", required=False, type=bool)
    parser.add_argument("-u", "--umi", help="UMI file?", required=False,)
    parser.add_argument("-o", "--output", help="what is your outputfile?", required=True)
    return parser.parse_args()
	
args = get_args()    
filename = (args.filename)
paired = (args.paired)
umi = (args.umi)
output = (args.output)

umi_dict = {}

with open(umi, "r") as umi:
    for line in umi:
        line=line.strip() 
        umi_dict[line]=[""]
umi.close() 

def numParser(s):
    """this function takes a list of strings and returns them as integers if possible"""
    try:
        return int(s)
    except ValueError:
        return s

def numSummer(list):
    """this function takes a list of integers and returns them summed"""
    the_sum=0
    for x in list:
        if isinstance(x, str):
            pass
        elif isinstance(x, int):
            the_sum += x
    return(the_sum)

def cigar_parse(lst):
    """this function takes a plus strand cigar string and returns the number of bp's required to adjust leftmost soft clipping """
    lst=re.split(r'[S]', lst)
    lst=map(numParser, lst)
    lst=numSummer(lst)
    return(lst)

def cigar_parse_rev(lst):
    """this function takes minus strand cigar string and returns adjusted positon""" 
    first_s='S'    
    lst=re.findall(r'([0-9]+[A-Z])', lst)
    if first_s in lst[0]:
        lst.pop(0)
    lst="".join(lst[:])
    lst=str(lst)
    lst=re.findall(r'([0-9]+[A-Z])', lst)
    lst="".join(lst[:])
    lst=re.sub(r'[0-9]+[I]','',lst)
    lst=re.split(r'[A-Z]', lst)
    lst=map(numParser, lst)
    lst=list(lst)
    lst=numSummer(lst)
    return(lst)

main_dict={}
i=0 
dedup_count=0
with open(filename, "r") as fh: 
    with open(output, "w") as ffh:
        for line in fh:
            while line.startswith("@"):
                ffh.write(str(line))
                line=fh.readline()
            
            i+=1
            origin_line=line
            line=line.strip('\n').split("\t")

            umihead=line[0]
            chrom=line[2]
            pos=line[3]
            pos=int(pos) #
            cigar=line[5]
            umihead=umihead.split(":")
            umihead=umihead[7] #  
            flag=int(line[1])

            if umihead not in umi_dict:
                continue
            if((flag & 16) == 16):
                    #do cigar fuxns on reverse strand 
                    adjustment=cigar_parse_rev(cigar)
                    adj_pos=(int(pos) + abs(int(adjustment)))
            else: 
                    # do cigar fxns on plus strand 
                    adjustment=cigar_parse(cigar)
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