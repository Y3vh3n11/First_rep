from datetime import date, datetime, timedelta


def get_birthdays_per_week(users):
    if len(users) == 0:
        return {}

    dict_of_user = {}       # словник іменинників
    todayy = date.today()   # дата сьогодні
    for user in users:
        if todayy.month == 12 and user['birthday'].month == 1:
            user['birthday'] = datetime(
                todayy.year+1, 
                user['birthday'].month,
                user['birthday'].day
                ).date()
        dnivdodr = todayy - user['birthday']
        str_dnivdodr = str(dnivdodr).split()
        str_dnivdodr2 = int(str_dnivdodr[0])
        if 0 >= str_dnivdodr2 >= -7:
            day_of_week_user = user['birthday'].strftime('%A')
            if len(dict_of_user) == 0:
                for i in range(7):
                    dayfordict = todayy + timedelta(days=i)
                    if dayfordict.strftime('%A') not in ['Saturday', 'Sunday']:
                        dict_of_user[dayfordict.strftime('%A')] = []
            try:
                dict_of_user[day_of_week_user].append(user['name'])
            except KeyError:
                dict_of_user['Monday'].append(user['name'])
        elif str_dnivdodr2 > 0:
            continue
    list_of_del_keys = []
    for k, v in dict_of_user.items():
        if len(v) == 0:
            list_of_del_keys.append(k)
    for i in list_of_del_keys:
        dict_of_user.pop(i)
    return dict_of_user


if __name__ == "__main__":
    users = [
        {"name": "Jan Koum", "birthday": datetime(1976, 1, 1).date()},
    ]

    result = get_birthdays_per_week(users)
    print(result)
    # Виводимо результат
    for day_name, names in result.items():
        print(f"{day_name}: {', '.join(names)}")
