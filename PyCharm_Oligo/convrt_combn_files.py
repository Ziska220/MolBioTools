#convert and combine multiple excel sheets into one tab deliminated file

import xlrd
from Bio.Seq import Seq
import os
import fileinput

#opens and read lines of reference file
ref_file = open('/Users/karlysindy/Documents/django_test/oligo_db/PyCharm_Oligo/reference_file.txt')
ref_read = ref_file.readline()
#turns reference file into bioseq Seq object with string (eg upper) and biological methods (eg compliment)
ref_caps = ref_read.upper()
ref_seq = Seq(ref_caps)
#creates a variable assigned to the reverse compliment of the reference file
ref_rev_comp = Seq.reverse_complement(ref_seq)

#opens excel sheet
book1 = xlrd.open_workbook('/Users/karlysindy/Documents/django_test/oligo_db/PyCharm_Oligo/AJ Oligo Sheet.xls')
book2 = xlrd.open_workbook('/Users/karlysindy/Documents/django_test/oligo_db/PyCharm_Oligo/AZ Oligos.xlsx')
#print "The number of worksheets is", book2.nsheets
#print "Worksheet name(s):", book2.sheet_names()


#loads requested sheet
# ?how determine which sheet? user input.
#sheet1 = book1.sheet_by_index(0)
#sheet2 = book2.sheet_by_index(0)

#sets variable to number of rows in designated sheet
#nrows = sheet.nrows
#print sheet.name, sheet.nrows, sheet.ncols
#print "Cell D30 is", sheet.cell_value(rowx=1, colx=1)

#sets variables to starting row and column. need to add user input code for column or can I have it find the oligos?


#summary: add +1 to oligo_row until reach nrows (the total number of rows in the sheet)
no_match = 0
name_match_list = []
f =('/Users/karlysindy/Documents/django_test/oligo_db/PyCharm_Oligo/AZ Oligos.xlsx', '/Users/karlysindy/Documents/django_test/oligo_db/PyCharm_Oligo/AJ Oligo Sheet.xls')
for xlsfile in f:
    print ("enter for")
    book = xlrd.open_workbook(xlsfile)
    sheet = book.sheet_by_index(0)
    nrows = sheet.nrows
    print (nrows)
    print (xlsfile)
    print sheet.cell_value(rowx=0, colx=2)



    oligo_row = 0
    oligo_col = 2
    name_col = 1

    for oligo in range(sheet.nrows):
        cell = sheet.cell_value(rowx=oligo_row, colx=oligo_col)
        if oligo_row < nrows:
            oligo_caps = cell.upper()
            oligo_find = ref_seq.find(oligo_caps)
            oligo_rev_find = ref_rev_comp.find(oligo_caps)
            if oligo_find == -1 and oligo_rev_find == -1 or cell == '':
                oligo_row += 1
            elif oligo_find != -1 or oligo_rev_find != -1:
                print ('elif1')
                name = sheet.cell_value(rowx=oligo_row, colx=name_col)
                name_match_list.extend((name,))
                no_match += 1
                oligo_row += 1
                print (name)
                print (oligo_caps)
                print ("GOT IT")


    print "this is name_match_list % s" % name_match_list








    # while oligo_row < nrows:
    #     print 'pass'
    #     print oligo_row
    #     print nrows
    #     oligo = sheet.cell_value(rowx=oligo_row, colx=oligo_col)
    #     oligo_caps = oligo.upper()
    #     oligo_find = ref_seq.find(oligo_caps)
    #     oligo_rev_find = ref_rev_comp.find(oligo_caps)
    #     if oligo_find == -1 and oligo_rev_find == -1:
    #         print "if"
    #         oligo_row += 1
    #     elif oligo_find ==0 or oligo_rev_find == 0:
    #         print 'elif1'
    #         name = sheet.cell_value(rowx=oligo_row, colx=name_col)
    #         print name
    #         print oligo_caps
    #         break



#
# for sheet in book.sheets():
#     print "pass for"
#     print sheet
    #for oligo in sheet.cell(oligo_row, oligo_col):
    # for oligo in sheet.col(2):
    #     print help(oligo)
     #   print "pass for2"

        #print sheet.nrows
        #print oligo.decode('utf-8').upper()
        #print oligo.upper()
        #print dir(oligo)


        #print oligo


        # oligo = sheet.cell_value(rowx=oligo_row, colx=oligo_col)
        # oligo_caps = oligo.upper()
        # oligo_find = ref_seq.find(oligo_caps)
        # print oligo_find
        # if oligo_find == -1:
        #      oligo_row = +1
        #      print oligo_row







# oligo = sheet.cell_value(rowx=oligo_row, colx=oligo_col)
# oligo_caps = oligo.upper()
# print oligo_caps
# oligo_find = ref_seq.find(oligo_caps)
# print oligo_find

#    elif oligo_row == 30:



