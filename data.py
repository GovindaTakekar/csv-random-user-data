import requests
import time
import pandas as pd
import threading

name_list = []


  ## below function helps to talk to API and also fetch the data from that api and
  ## convert it into a csv file

def get_new_user():
    global name_list
    while True:
        response = requests.get(url="https://random-data-api.com/api/v2/users?size=1&is_xml=true")
        response.raise_for_status()
        data = response.json()

        new_person_details = {
            "id": data["id"],
            "first_name": data["first_name"],
            "last_name": data["last_name"],
            "username": data["username"],
            "email": data["email"],
            "avatar": data["avatar"],
            "gender": data["gender"],
            # "DOB": data["date_of_birth"],
            "address": [{
                "city": data["address"]["city"],
                "street_name": data["address"]["street_name"],
                "country": data["address"]["country"]
            }
            ],
        }


        df = pd.DataFrame(new_person_details)
        df.to_csv("user.csv", mode="a", index=False,header=False)


        ## sorted list of users

        read_data = pd.read_csv("user.csv")
        sorted_data = read_data.sort_values(["first_name"], ascending=True)
        sorted_data.to_csv("users-sorted.csv")
        
        ## adding data after after every 5 seconds
        
        time.sleep(5)


## search for a user by it's first name

def search_user():
    while True:
        user_data = pd.read_csv("user.csv")
        name_list = list(user_data["first_name"])
        pd.set_option('display.max_columns', None)

        search_user = input("Search user by username")
        if (search_user in name_list):
            print(user_data[user_data["first_name"] == search_user])
        else:
            print("No user Found")

        time.sleep(2)


# run 2 loops at a same time


thread1 = threading.Thread(target=get_new_user)
thread1.start()

thread2 = threading.Thread(target=search_user)
thread2.start()






# print(user_data[user_data["first_name"] == search_user])


