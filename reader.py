
import sys


doublequote=True
escapechar=None
quotechar='"'
lineterminator='&|\r\n'
delimiter='+|'
rows=[]
row=[]

quoting = False #any mode other than QUOTING_NONE



f = open(sys.argv[1], 'r', newline='', encoding='utf-16')


inquote=False
linebuffer=''
fieldbuffer=''
for line in f:
    if quoting:
        i = 0
        end = len(line)
        while i < end:
            if inquote and line[i:].startswith(quotechar):
                i += len(quotechar)
                if line[i:].startswith(delimiter):  #end of field
                    inquote = False
                    i += len(delimiter)
                    row.append(fieldbuffer)
                    fieldbuffer = ""
                elif line[i:].startswith(quotechar): #doublequoted quote
                    fieldbuffer += quotechar
                    i += len(quotechar)
                else:
                    print(line)
                    raise RuntimeError(f"Reader error - invalid quote at index {i}")
            elif not inquote and line[i:].startswith(quotechar):
                if len(fieldbuffer) == 0:
                    inquote=True
                    i += len(quotechar)
                else:
                    raise RuntimeError(f"Reader error - quote not doubled at index {i}")
            elif not inquote and line[i:].startswith(delimiter): # end of field
                i += len(delimiter)
                row.append(fieldbuffer)
                fieldbuffer = ""
            elif not inquote and line[i:].startswith(lineterminator): #row end
                row.append(fieldbuffer)
                rows.append(row)
                fieldbuffer = ""
                i += len(lineterminator)
            else:
                fieldbuffer += line[i]
                i += 1
    else: # no quoting
        i = 0
        end = len(line)
        while i < end:
            if line[i:].startswith(delimiter):
                i += len(delimiter)
                row.append(fieldbuffer)
                fieldbuffer = ""
            elif line[i:].startswith(lineterminator):
                i += len(lineterminator)
                row.append(fieldbuffer)
                fieldbuffer = ""
                rows.append(row)
                row = []
            else:
                fieldbuffer += line[i]
                i += 1

for r in rows:
    print(f"row starting with {r[0]} has {len(r)} fields.")
