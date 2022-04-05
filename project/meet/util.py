from datetime import date

def user_age(d_o_b):
    today = date.today()

    try: 
        birthday = d_o_b.replace(year = today.year)
    except ValueError:
        birthday = d_o_b.replace(year = today.year, month=d_o_b.month+1, day=1)

    if birthday > today:
        return today.year - d_o_b.year - 1
    else:
        return today.year - d_o_b.year