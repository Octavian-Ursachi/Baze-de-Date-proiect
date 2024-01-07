import re


def verifica_datatype(valoare, tip_data):
    if valoare.isnumeric():
        # print(valoare+" e numar?")
        if tip_data == 'numeric':
            return True
        else:
            return False
    elif len(valoare) == 19:
        text = valoare
        rezultat = re.search("[2-9][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9] [0-2][0-9]:[0-5][0-9]:[0-5][0-9]", text)
        if rezultat is not None:
            # print(valoare+" e timestamp?")
            # trebuie verificate in plus luna ziua si ora pentru ca regexul nu e suficient de exact
            luna = int(text[5]+text[6])
            ziua = int(text[8]+text[9])
            ora = int(text[11]+text[12])
            print(luna, ziua, ora)
            if tip_data == 'timestamp' and 0 < luna <= 12 and 0 < ziua <= 31 and ora <= 23:
                return True
            else:
                return False
        else:
            # print(valoare+" e string?")
            if tip_data == 'varchar2':
                return True
            else:
                return False
    else:
        # print(valoare+" e string?")
        if tip_data == 'varchar2':
            return True
        else:
            return False


def verifica_constrangeri(valoare, constrangere):
    if constrangere == 'not_null' or constrangere == 'foreign_key' or constrangere == 'primary_key':
        print("Nenul")
        if valoare == '':
            return False
        else:
            return True
    else:
        print("Alta constrangere")
        return True


if __name__ == '__main__':
    listaCiudata = (('123', 'numeric'), ('2023-12-32 22:59:00', 'timestamp'), ('segehg', 'varchar2'),  ('segehgjdjdjdjdjdjdj', 'timestamp'))
    for valoare in listaCiudata:
        print("Este "+valoare[0]+" "+valoare[1]+" ? "+str(verifica_datatype(valoare[0], valoare[1])))
