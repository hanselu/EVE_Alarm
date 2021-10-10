import eve


def show_list(l: list):
    for i in l:
        print(i)


local = eve.get_local()
# local = 'P-UCRP'
a_list = eve.get_alarm_list(local)
print(local)
show_list(a_list)