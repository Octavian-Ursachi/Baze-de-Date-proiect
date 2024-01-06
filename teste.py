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
        rezultat = re.search("[2-9][0-9][0-9][0-9]-[0-2][0-9]-[0-3][0-9] [0-2][0-9]:[0-5][0-9]:[0-5][0-9]", text)
        if rezultat is not None:
            # print(valoare+" e timestamp?")
            if tip_data == 'timestamp':
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


if __name__ == '__main__':
    listaCiudata = (('123', 'numeric'), ('2023-00-20 10:00:00', 'timestamp'), ('segehg', 'varchar2'),  ('segehgjdjdjdjdjdjdj', 'timestamp'))
    for valoare in listaCiudata:
        print("Este "+valoare[0]+" "+valoare[1]+" ? "+str(verifica_datatype(valoare[0], valoare[1])))
