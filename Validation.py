def validate_date(start_date, end_date):
    data_s = list(map(int, start_date.split("-")))
    date_e = list(map(int, end_date.split("-")))
    if data_s[0] == date_e[0]:
        data_s[1] -= 1
        date_e[1] -= 1
        data_s[1] *= 30
        date_e[1] *= 30

        if data_s[0] + data_s[1] + data_s[2] < date_e[0] + date_e[1] + date_e[2]:
            #print("Все правильно")
            return True
        else:
            #print("Дата кінця раніша за початок")
            return False

    elif data_s[0] < date_e[0]:
        #print("Все правильно")
        return True
    else:
        #print("Дата кінця раніша за початок")
        return False


'''    
start_date = input('Y-m-d: ')
end_date= input('Y-M-D:')'''
start_date='2025-04-05'
end_date='2025-04-06'
print(validate_date(start_date,end_date))
