
HELLO THERE! 

Welcome to John's deduper pseudocode workflow! Just like you I have been tasked with deduping the currenlty un-deduped! Thank you for your time and extensive commentary! :D  

The PROBLEM : 

We need to remove deduplicated strands that contain all of the following attributes with another strand: 

- same RNAME column 3 chromosome 

- same POS column 4 starting position 

- same strand (FLAG) bitwise flag i.e. 

        if ((flag & 16) == 16):
            rev_comp = True

            means that the sequence in question is the rev_comp? 

- CIGAR column 6 
    need a fxn here with a pass/no pass boolean -- see below 

- same UMI sam column 1 (QUNAME)

General thought process for checking: 

pull out header lines that begin with an @ symbol > add them back in later 
Use samtools to sort the sam file, first by chromosome then by position number. 
open the sam file (human readable, txt file)

As you read down the file, add the columns of interest into tuples, in a dictionary 
# This has been previously done before check
# lab notebook for Bi621

take the dictionary entries and compare it to the next line by variable of interest

    if RNAME line1 is in dict:
        check if POS line1 is in dict: 
            if line1 ((flag & 16) == 16) is in dict:
                if line1 cigar_fxn is in dict: 
                    if QNAME line1 is in dict:
                        This is a PCR duplicate and needs to be DESTROYED -> write out to duplicate file

                    else: add to the dictionary 
                else: add to the dictionary 
            else: add to the dictionary 
        else: add to the dictionary 
    else: add to the dictionary 
                
                repeat 


Higher Level Functionalities: 

cig_bool_test 
"""this fxn reads the cigar string and will count back the number of softclipped bases, returns a beginning of line position by adding those to the POS...?""" 
<fxn code here>
return(int)


add the pulled out header lines from the begining of the program. 