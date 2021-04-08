from datetime import date

def prueba_from_cod(cod_prueba):
    split=cod_prueba.split("_")
    cod_prueba=split[2]
    return cod_prueba

def calculateAge(born):
    split=born.split("-")
    y=int(split[0])
    m=int(split[1])
    d=int(split[2])
    born=date(y,m,d)
    today = date.today()
    try: 
        birthday = born.replace(year = today.year)
  
    # raised when birth date is February 29
    # and the current year is not a leap year
    except ValueError: 
        birthday = born.replace(year = today.year,
                  month = born.month + 1, day = 1)
  
    if birthday > today:
        return today.year - born.year - 1
    else:
        return today.year - born.year
          
