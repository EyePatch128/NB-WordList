import sys
import getopt
from itertools import permutations, combinations
from pathlib import Path

# Arguments
dst_file            = ""
overwrite_file      = False
input_file          = ""
special_characters  = False 
special_characters_format = []
birthday_format     = []
name_format         = []
pwd_format          = ["default"]


# Usage function
def usage():
    print("Usage:")
    print("\t%s -f [destination file] [-s] [-S [format]] [-b [format]] [-n [format]] [-p [format]]", sys.argv[0])
    print("\n")
    print("DESCRIPTION:")
    print("\n")
    print("\t\t-f, --file [path-to-file]")
    print("\t\t\t\t\t\tSpecify a destination file where password list will be stored")
    print("\n")
    print("\t\t-o, --overwrite-file")
    print("\t\t\t\t\t\tOverwrite destination file.")
    print("\n")
    print("\t\t-i, --input-file")
    print("\t\t\t\t\t\tSpecify an input file to extract user input from")
    print("\t\t\t\t\t\t\t\tFormat:")
    print("\t\t\t\t\t\t\t\t\t\tFirst Name\n")
    print("\t\t\t\t\t\t\t\t\t\tLast Name\n")
    print("\t\t\t\t\t\t\t\t\t\tBirth day\n")
    print("\t\t\t\t\t\t\t\t\t\tBirth Month\n")
    print("\t\t\t\t\t\t\t\t\t\tBirth Year\n")
    print("\t\t\t\t\t\t\t\t\t\tSpecial characters")
    print("\n")
    print("\t\t-s, --special-characters")
    print("\t\t\t\t\t\tEnable special characters")
    print("\n")
    print("\t\t-S, --special-characters-format [format]")
    print("\t\t\t\t\t\tSpecify format for special characters")
    print("\t\t\t\t\t\tPossible formats")
    print("\t\t\t\t\t\t\tName combinations: (Only one possible)")
    print("\t\t\t\t\t\t\t(DEFAULT:\tGenerate name combinations without special character)")
    print("\t\t\t\t\t\t\t\tonlyspcharname:\tOnly generate name combinations with special character")
    print("\t\t\t\t\t\t\t\tandspcharname :\tGenerate name combinations with and without special character")
    print("\t\t\t\t\t\t\tBirthday combinations: (Only one possible)")
    print("\t\t\t\t\t\t\t(DEFAULT:\tGenerate birthday combinations without special character)")
    print("\t\t\t\t\t\t\t\tonlyspcharbday:\tOnly generate birthdat combinations with special character")
    print("\t\t\t\t\t\t\t\tandspcharbday :\tGenerate birthday combinations with and without special character")
    print("\t\t\t\t\t\t\tMax formats: 2 (1name_format 1birthday_format). Separate formats with ' '(space)")
    print("\n")
    print("\t\t-n, --name-format [format]")
    print("\t\t\t\t\t\tSpecify the format of name combination")
    print("\t\t\t\t\t\t\tCombination format:")
    print("\t\t\t\t\t\t\t\tnoLen2       :\tRemove two length combinations (three length if -s)")
    print("\t\t\t\t\t\t\t\tnoUpper      :\tRemove combinations where either first name or last name is uppercase")
    print("\t\t\t\t\t\t\t\tnoUpperBoth  :\tRemove combinations where both first name and last name are uppercase")
    print("\t\t\t\t\t\t\t\tnoCap        :\tRemove combinations where either first name or last name is capitalized")
    print("\t\t\t\t\t\t\t\tnoCapBoth    :\tRemove combinations where both first name and last name are capitalized")
    print("\t\t\t\t\t\t\t\tnoDoubleName :\tRemove combinations with both first name and last name")
    print("\t\t\t\t\t\t\t\tnoSingleName :\tRemove combinations with either first name or last name (One name)")
    print("\n")
    print("\t\t-b, --bday-format [format]")
    print("\t\t\t\t\t\tSpecify the format of birthday combination")
    print("\t\t\t\t\t\t\tCombination format:")
    print("\t\t\t\t\t\t\t\tnoDoubleLen3 :\tRemove [(DD, MM, YYYY) | (DD, MM, YY)    Length: 3]  format")
    print("\t\t\t\t\t\t\t\tnoSingleLen3 :\tRemove [(D, M, YYYY) | (D, M, YY)        Length: 3]  format")
    print("\t\t\t\t\t\t\t\tnoDoubleLen2 :\tRemove [(DD, MM, YYYY) | (DD, MM, YY)    Length: 2]  format")
    print("\t\t\t\t\t\t\t\tnoSingleLen2 :\tRemove [(D, M, YYYY) | (D, M, YY)        Length:2]   format")
    print("\t\t\t\t\t\t\t\tnoDoubleLen1 :\tRemove [(DD, MM, YYYY) | (DD, MM, YY)    Length: 1]  format")
    print("\t\t\t\t\t\t\t\tnoSingleLen1 :\tRemove [(D, M, YYYY) | (D, M, YY)        Length:1]   format")
    print("\n")
    print("\t\t-p, --password-format [format]")
    print("\t\t\t\t\t\tSpecify the format of password combination")
    print("\t\t\t\t\t\t\tCombination format:")
    print("\t\t\t\t\t\t\t\tdefault      :\tGenerate combination of format `name``birthday`. Default")
    print("\t\t\t\t\t\t\t\tboth         :\tGenerate combination of format `name``birthday` and `birthday``name`")
    print("\t\t\t\t\t\t\t\tbdaybeg      :\tGenerate combination of format `birthday``name`")
    print("\t\t\t\t\t\t\t\tandspchar    :\tGenerate combination with and without special character")
    print("\n")
    print("\n")
    print("INPUT FORMAT:")
    print("\n")
    print("\t\tFirst name           :\t\t(lowercase)")
    print("\t\tLast name            :\t\t(lowercase)")
    print("\t\tBirthday day         :\t\t(DD)")
    print("\t\tBirthday month       :\t\t(MM")
    print("\t\tBirthday year        :\t\t(YYYY)")
    print("\t\tSpecial characters   :\t\t('SChar''Position')(Separator=Space)")
    print("\t\t\t\tPossible special characters positions:")
    print("\t\t\t\t\tname       :\tSpecial character between name combination")
    print("\t\t\t\t\tbday       :\tSpecial character between birthday combination")
    print("\t\t\t\t\tbetween    :\tSpecial character between name combination and birthday combination")
    print("\t\t\t\t\tstart      :\tSpecial character at start of password combination")
    print("\t\t\t\t\tend        :\tSpecial character at end of password combination")


try:
    opts, args = getopt.getopt(sys.argv[1:], "hf:oi:sS:b:n:p:", ["help", "file", "overwrite-file", "input-file", "special-characters", "special-characters-format", "birthday-format", "name-format", "password-format"])
    for opt, val in opts:
        if opt in ('-h', '--help'):
            usage()
        elif opt in ('-f', '--file'):
            dst_file = val
        elif opt in ('-o', '--overwrite-file'):
            overwrite_file = True
        elif opt in ('-i', '--input-file'):
            input_file = val
        elif opt in ('-s', '--special-characters'):
            special_characters = True
        elif opt in ('-S', '--special-characters-format'):
            special_characters_format = val.split(" ")
        elif opt in ('-b', '--birthday-format'):
            birthday_format = val.split(" ")
        elif opt in ('-n', '--name-format'):
            name_format = val.split(" ")
        elif opt in ('-p', '--password-format'):
            pwd_format = val.split(" ")
except getopt.GetoptError:
    print("Invalid arguments! Please refer usage")
    usage()
    sys.exit(1)

# Parse arguments
if not dst_file:
    print("Not enough arguments! Please refer to usage\n")
    usage()
    sys.exit(1)


# Get user input
special_chars = []
if input_file:
    # Read input file
    with open(input_file, 'r') as credentials:
        credentials.seek(0)
        l = credentials.readlines()
        # Remove trailing newline
        for i in l:
            i.rstrip("\n")

        fst_name    = l[0]
        lst_name    = l[1]

        b_day       = l[2]
        b_month     = l[3]
        b_year      = l[4]

        if special_characters:
            special_chars = l[5].split(" ")

else:
    fst_name    = input("First Name: ")
    lst_name    = input("Last Name: ") 

    b_day       = input("Birth day (DD): ")
    b_month     = input("Birth month (MM): ")
    b_year      = input("Birth year (YYYY): ")

    if special_characters:
        special_chars = input("Special characters: ").split(" ")

fst_name = fst_name.lower()
lst_name = lst_name.lower()

# If input is of format D
if len(b_day) == 1:
    b_day = "0" + b_day
# If input is of format M
if len(b_month) == 1:
    b_month= "0" + b_month

def stripSpecialCharacter(array, spchar):
    if len(array[0]) == 2:
        for i in range(len(array)):
            array[i] = (array[i][0], array[i][1].rstrip(spchar))
    else:
        for i in range(len(array)):
            array[i] = (array[i][0], array[i][1], array[i][2].rstrip(spchar))
    return array


def generateNameCombinations():
    name_comb = []
    iter_name_comb = []
    # Get iteritems combinations list
    if "noDoubleName" not in name_format:
        iter_name_comb = list(permutations([fst_name, lst_name, fst_name.upper(), lst_name.upper(), fst_name.capitalize(), lst_name.capitalize(), fst_name[0].upper(), lst_name[0].upper(), fst_name[0], lst_name[0]], 2))
    if "noSingleName" not in name_format:
        iter_name_comb0 = list(permutations([fst_name, lst_name, fst_name.upper(), lst_name.upper(), fst_name.capitalize(), lst_name.capitalize(), fst_name[0].upper(), lst_name[0].upper(), fst_name[0], lst_name[0]], 1))
        iter_name_comb = iter_name_comb + iter_name_comb0

    try:
        if special_characters and "noDoubleName" not in name_format:
            if "onlyspcharname" in special_characters_format:
                # If only special character
                spchar_format = [i for i in special_chars if "name" in i][0]
                spchar = spchar_format[0]
                iter_name_comb0 = list(permutations([fst_name + spchar, lst_name + spchar, fst_name.upper() + spchar, lst_name.upper() + spchar, fst_name.capitalize() + spchar, lst_name.capitalize() + spchar, fst_name[0].upper() + spchar, lst_name[0].upper() + spchar, fst_name[0] + spchar, lst_name[0] + spchar], 2))
                # Strip special character from end of combinations
                iter_name_comb0 = stripSpecialCharacter(iter_name_comb0, spchar)
                iter_name_comb = iter_name_comb0
            elif "andspcharname" in special_characters_format:
                # If with special character
                spchar_format = [i for i in special_chars if "name" in i][0]
                spchar = spchar_format[0]
                iter_name_comb0 = list(permutations([fst_name + spchar, lst_name + spchar, fst_name.upper() + spchar, lst_name.upper() + spchar, fst_name.capitalize() + spchar, lst_name.capitalize() + spchar, fst_name[0].upper() + spchar, lst_name[0].upper() + spchar, fst_name[0] + spchar, lst_name[0] + spchar], 2))
                # Strip special character from end of combinations
                iter_name_comb0 = stripSpecialCharacter(iter_name_comb0, spchar)
                iter_name_comb = iter_name_comb + iter_name_comb0
    except:
        print("Error while generating name combinations (with special character)")
        print("Make sure to include ['Schar'name] in 'Special characters' input field")
        sys.exit(1)
        

    # Clean redunduncy
    def cleanRedunduncy(elem):
        comb = "".join(elem)
        if len(elem) != 1:
            if not (fst_name in elem and lst_name in elem) and (elem[0].upper() == elem[1].upper() or elem[0][0].upper() == elem[1][0].upper()):
                return False
        return True
    
    iter_name_comb = list(filter(cleanRedunduncy, iter_name_comb))
    name_comb_rem  = []
    
    # Filter and parse list
    for i in range(len(iter_name_comb)):

        elem = iter_name_comb[i]
        comb = "".join(iter_name_comb[i])
        
        name_comb.append(comb)
    else:

        if "noLen2" in name_format:
            for i in range(len(iter_name_comb)):
                elem = iter_name_comb[i]
                comb = "".join(iter_name_comb[i])

                min_length = len(fst_name) if len(fst_name) < len(lst_name) else len(lst_name)
                if len(comb) < min_length:
                    name_comb_rem.append(comb) 
        if "noUpper" in name_format:
            for i in range(len(iter_name_comb)):
                elem = iter_name_comb[i]
                comb = "".join(iter_name_comb[i])

                if fst_name.upper() in elem or lst_name.upper() in elem:
                    name_comb_rem.append(comb) 
        if "noUpperBoth" in name_format:
            for i in range(len(iter_name_comb)):
                elem = iter_name_comb[i]
                comb = "".join(iter_name_comb[i])

                if fst_name.upper() in elem and lst_name.upper() in elem:
                    name_comb_rem.append(comb) 
        if "noCap" in name_format:
            for i in range(len(iter_name_comb)):
                elem = iter_name_comb[i]
                comb = "".join(iter_name_comb[i])

                if fst_name.capitalize() in elem or lst_name.capitalize() in elem:
                    name_comb_rem.append(comb) 
        if "noCapBoth" in name_format:
            for i in range(len(iter_name_comb)):
                elem = iter_name_comb[i]
                comb = "".join(iter_name_comb[i])

                if fst_name.capitalize() in elem and lst_name.capitalize() in elem:
                    name_comb_rem.append(comb) 
    # Remove undesired combinations
    for i in name_comb_rem:
        if i in name_comb:
            name_comb.remove(i)

    return name_comb


def generateBdayCombinations():
    b_comb = []
    # Get iteritems combinations list
    # >> list 0: Format --> (DD, MM, YYYY) | (DD, MM, YY)   Length: 3
    iter_b_comb0 = list(permutations([b_day, b_month, b_year, b_year[2:]], 3))
    # >> list 1: Format --> (D, M, YYYY) | (D, M, YY)[* Only if DD or MM begin with 0]  Length: 3
    iter_b_comb1 = list(permutations([b_day[1] if b_day[0] == "0" else "", b_month[1] if b_month[0] == "0" else "", b_year ,b_year[2:]], 3))
    # >> list 2: Format --> (DD, MM, YYYY) | (DD, MM, YY)   Length: 2
    iter_b_comb2 = list(permutations([b_day, b_month, b_year, b_year[2:]], 2))
    # >> list 3: Format --> (D, M, YYYY) | (D, M, YY)   Length:2
    iter_b_comb3 = list(permutations([b_day[1] if b_day[0] == "0" else "", b_month[1] if b_month[0] == "0" else "", b_year, b_year[2:]], 2))
    # >> list 4: Format --> (DD, MM, YYYY) | (DD, MM, YY)   Length: 1
    iter_b_comb4 = list(permutations([b_day, b_month, b_year, b_year[2:]], 1))
    # >> list 5: Format --> (D, M, YYYY) | (D, M, YY)   Length:1
    iter_b_comb5 = list(permutations([b_day[1] if b_day[0] == "0" else "", b_month[1] if b_month[0] == "0" else "", b_year, b_year[2:]], 1))
    
    try:
        if special_characters:
            if "andspcharbday" in special_characters_format:
                spchar_format = [i for i in special_chars if "bday" in i][0]
                spchar = spchar_format[0]
                iter_b_comb0_temp = list(permutations([b_day + spchar, b_month + spchar, b_year + spchar, b_year[2:] + spchar], 3))
                iter_b_comb0_temp = stripSpecialCharacter(iter_b_comb0_temp, spchar)
                iter_b_comb0 = iter_b_comb0 + iter_b_comb0_temp

                iter_b_comb1_temp = list(permutations([b_day[1] + spchar if b_day[0] == "0" else "", b_month[1] + spchar if b_month[0] == "0" else "", b_year + spchar ,b_year[2:] + spchar], 3))
                iter_b_comb1_temp = stripSpecialCharacter(iter_b_comb1_temp, spchar)
                iter_b_comb1 = iter_b_comb1 + iter_b_comb1_temp

                iter_b_comb2_temp = list(permutations([b_day + spchar, b_month + spchar, b_year + spchar, b_year[2:] + spchar], 2))
                iter_b_comb2_temp = stripSpecialCharacter(iter_b_comb2_temp, spchar)
                iter_b_comb2 = iter_b_comb0 + iter_b_comb2_temp

                iter_b_comb3_temp = list(permutations([b_day[1] + spchar if b_day[0] == "0" else "", b_month[1] + spchar if b_month[0] == "0" else "", b_year + spchar, b_year[2:] + spchar], 2))
                iter_b_comb3_temp = stripSpecialCharacter(iter_b_comb3_temp, spchar)
                iter_b_comb3 = iter_b_comb3 + iter_b_comb3_temp
            elif "onlyspcharbday" in special_characters_format:
                spchar_format = [i for i in special_chars if "bday" in i][0]
                spchar = spchar_format[0]
                iter_b_comb0_temp = list(permutations([b_day + spchar, b_month + spchar, b_year + spchar, b_year[2:] + spchar], 3))
                iter_b_comb0_temp = stripSpecialCharacter(iter_b_comb0_temp, spchar)
                iter_b_comb0 = iter_b_comb0_temp

                iter_b_comb1_temp = list(permutations([b_day[1] + spchar if b_day[0] == "0" else "", b_month[1] + spchar if b_month[0] == "0" else "", b_year + spchar ,b_year[2:] + spchar], 3))
                iter_b_comb1_temp = stripSpecialCharacter(iter_b_comb1_temp, spchar)
                iter_b_comb1 = iter_b_comb1_temp

                iter_b_comb2_temp = list(permutations([b_day + spchar, b_month + spchar, b_year + spchar, b_year[2:] + spchar], 2))
                iter_b_comb2_temp = stripSpecialCharacter(iter_b_comb2_temp, spchar)
                iter_b_comb2 = iter_b_comb2_temp

                iter_b_comb3_temp = list(permutations([b_day[1] + spchar if b_day[0] == "0" else "", b_month[1] + spchar if b_month[0] == "0" else "", b_year + spchar, b_year[2:] + spchar], 2))
                iter_b_comb3_temp = stripSpecialCharacter(iter_b_comb3_temp, spchar)
                iter_b_comb3 = iter_b_comb3_temp
    except:
        print("Error while generating birthday combinations")
        print("Make sure to include ['Schar'bday] in 'Special characters' input field")

            


    # B combinations 0
    if "noDoubleLen3" not in birthday_format:
        for i in range(len(iter_b_comb0)):
            elem = iter_b_comb0[i]
            comb = "".join(iter_b_comb0[i])
            # Clean redunduncy
            skip = False
            # >> Year
            if b_year in elem and b_year[2:] in elem:
                skip = True
            if special_characters and ("onlyspcharbday" in special_characters_format or "andspcharbday" in special_characters_format):
                spchar_format = [i for i in special_chars if "bdaybetween" in i][0]
                spchar = spchar_format[0]
                if b_year + spchar in elem or b_year in elem:
                    if b_year[2:] + spchar in elem or b_year[2:] in elem:
                        skip = True
            if skip:
                continue
            b_comb.append(comb)

    # B combinations 1
    if "noSingleLen3" not in birthday_format:
        for i in range(len(iter_b_comb1)):
            elem = iter_b_comb1[i]
            comb = "".join(iter_b_comb1[i])
            # Clean redunduncy
            skip = False
            if comb == b_year[2:] or comb == b_year or comb in b_comb or (b_year in elem and b_year[2:] in elem):
                skip = True
            if special_characters and ("onlyspcharbday" in special_characters_format or "andspcharbday" in special_characters_format):
                spchar_format = [i for i in special_chars if "bdaybetween" in i][0]
                spchar = spchar_format[0]
                if b_year + spchar in elem or b_year[2:] + spchar in elem:
                    if b_year in elem or b_year[2:] in elem:
                        skip = True
                    if comb == b_year + spchar or comb == b_year[2:]:
                        skip = True
            if skip:
                continue
            b_comb.append(comb)

    # B combinations 2
    if "noDoubleLen2" not in birthday_format:
        for i in range(len(iter_b_comb2)):
            elem = iter_b_comb2[i]
            comb = "".join(iter_b_comb2[i])
            # Clean redunduncy
            skip = False
            if comb in b_comb or (b_year in elem and b_year[2:] in elem):
                skip = True
            if special_characters and ("onlyspcharbday" in special_characters_format or "andspcharbday" in special_characters_format):
                if b_year in elem or b_year[2:] in elem or b_year + spchar in elem or b_year[2:] + spchar in elem:
                    if b_year in elem or b_year[2:] in elem or b_year + spchar in elem or b_year[2:] + spchar in elem:
                        skip = True
            if skip:
                continue
            b_comb.append(comb)

    # B combinations 3
    if "noSingleLen2" not in birthday_format:
        for i in range(len(iter_b_comb3)):
            elem = iter_b_comb3[i]
            comb = "".join(iter_b_comb3[i])
            # Clean redunduncy
            skip = False
            if comb in b_comb or (b_year in elem and b_year[2:] in elem):
                skip = True
            if special_characters and ("onlyspcharbday" in special_characters_format or "andspcharbday" in special_characters_format):
                if b_year in elem or b_year[2:] in elem or b_year + spchar in elem or b_year[2:] + spchar in elem:
                    if b_year in elem or b_year[2:] in elem or b_year + spchar in elem or b_year[2:] + spchar in elem:
                        skip = True
            if skip:
                continue
            b_comb.append(comb)

    # B combinations 4
    if "noDoubleLen1" not in birthday_format:
        for i in range(len(iter_b_comb4)):
            elem = iter_b_comb4[i]
            comb = "".join(iter_b_comb4[i])
            # Clean redunduncy
            skip = False
            if comb in b_comb:
                skip = True
            
            if skip:
                continue
            b_comb.append(comb)
    
    # B combinations 5
    if "noSingleLen1" not in birthday_format:
        for i in range(len(iter_b_comb5)):
            elem = iter_b_comb5[i]
            comb = "".join(iter_b_comb5[i])
            # Clean redunduncy
            skip = False
            if comb in b_comb:
                skip = True
            
            if skip:
                continue
            b_comb.append(comb)
    
    return b_comb

# Get name combinations
name_combinations = generateNameCombinations()

# Get birthday combinations
bday_combinations = generateBdayCombinations()

# Include special characters
def addSpecialChars(name_bday, bday_name, name_len, bday_len):
    for i in special_chars:
        if i[1:] == "between":
            name_bday = name_bday[0:name_len] + i[0] + name_bday[name_len:]
            bday_name = bday_name[0:bday_len] + i[0] + bday_name[bday_len:]
        if i[1:] == "end":
            name_bday += i[0]
            bday_name += i[0]
        if i[1:] == "start":
            name_bday = i[0] + name_bday
            bday_name = i[0] + bday_name
    return [name_bday, bday_name]
            


def mergeCombinations(name_combinations, bday_combinations):
    pwd_comb = []
    for name in name_combinations:
        for bday in bday_combinations:
            # Without special character
            pwd0 = name + bday
            pwd1 = bday + name
            # With special character
            pwd0s = ""
            pwd1s = ""
            if special_characters:
                pwd0s, pwd1s = addSpecialChars(pwd0, pwd1, len(name), len(bday))

            if "default" in pwd_format or "bdayend" in pwd_format:
                pwd_comb.append(pwd0)
                if "andspchar" in pwd_format:
                    pwd_comb.append(pwd0s)
            elif "both" in pwd_format:
                pwd_comb.append(pwd0)
                pwd_comb.append(pwd1)
                if "andspchar" in pwd_format:
                    pwd_comb.append(pwd0s)
                    pwd_comb.append(pwd1s)
            elif "bdaybeg" in pwd_format:
                pwd_comb.append(pwd1)
                if "andspchar" in pwd_format:
                    pwd_comb.append(pwd1s)
    return pwd_comb

# Merge combinations
pwd_combinations = mergeCombinations(name_combinations, bday_combinations)

# Make password list
# Write to file
def overwriteFile():
    with open(dst_file, "w+") as pwd_list:
        pwd_list.write("\n".join(pwd_combinations))
def writeFile(mode):
    with open(dst_file, mode) as pwd_list:
        pwd_list.seek(0)
        old_list = []
        if mode == 'r+':
            old_list = pwd_list.readlines()
        for i in pwd_combinations:
            if i + '\n' not in old_list:
                old_list.append(i + '\n')
        pwd_list.seek(0)
        pwd_list.write("".join(old_list))
        pwd_list.truncate()

if dst_file:
    if overwrite_file:
        overwriteFile()
    else:
        f = Path(dst_file)
        if f.is_file():
            writeFile('r+')
        else:
            writeFile('w+')
    print("Passworld list successfuly written to '%s'" % dst_file)

