import math
phi = ( 1 + math.sqrt(5) ) / 2

def getFibbonacci(length:int = 0) -> list:
    sequence:list = [0,1]
    for i in range(1,length):
        sequence.append(sequence[i-1]+sequence[i])
    return sequence


def filterSequence(sequence:list, multipli:float)-> list:
    filt_seq : list = []
    for i in sequence:
        if(i % multipli == 0):
            filt_seq.append(i)
    return filt_seq


def findProportion(sequence:list, error = 0.0001):
    for i in range(2,len(sequence)):
        if sequence[i]/sequence[i-1] % phi <= error:
            return i, True
    return -1, False 


print(filterSequence(getFibbonacci(int(input("sequence length: "))),int(input("filter multipli: "))))

index, found = findProportion(getFibbonacci(int(input("sequence length: "))))
if(found):
    print("proportion found whith sequence length: ", index)
else:
    print("proportion not found with sequence length: ", index)
