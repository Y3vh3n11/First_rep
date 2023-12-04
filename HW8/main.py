from datetime import date, datetime, timedelta


def get_birthdays_per_week(users):
    if len(users) == 0:
        return {}

    dict_of_user = {}  # словник іменинників
    
    # todayy = datetime(year=2023, month=12, day=6)
    # todayy = datetime.today()
    todayy = datetime(2023, 12, 26)
    
    # print(todayy)
    for user in users:
        # print(f"todayy.mont = {todayy.month}  user['birthday'].month = {user['birthday'].month}")
        # monut_rizne = todayy.month - user['birthday'].month
       
        dnivdodr = todayy.date() - user['birthday']            
        str_dnivdodr = str(dnivdodr).split()
        str_dnivdodr2 = int(str_dnivdodr[0])
       
        if 0 >= str_dnivdodr2 >= -7:
            day_of_week_user = user['birthday'].strftime('%A')
            # print(f"day_of_week_user = {day_of_week_user}")
            if len(dict_of_user) == 0:
                for i in range(7):
                    day_week_for_dict = todayy + timedelta(days=i)
                    # print(f'Створення словника {day_week_for_dict}')
                    if day_week_for_dict.strftime('%A') not in ['Saturday', 'Sunday']:
                        dict_of_user[day_week_for_dict.strftime('%A')] = []
            try:
                dict_of_user[day_of_week_user].append(user['name'])
                # print(dict_of_user)
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
    # dict_of_user2 = dict(dict_of_user)
    # return dict_of_user2


if __name__ == "__main__":
    today = datetime(2023, 12, 26)
    users = [            
           {
                "name": "Alice",
                "birthday": (datetime(2021, 1, 1)).date(),
            },
        ]

    result = get_birthdays_per_week(users)
    print(result)
    # Виводимо результат
    for day_name, names in result.items():
        print(f"{day_name}: {', '.join(names)}")
