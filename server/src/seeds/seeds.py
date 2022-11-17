import json
import requests

URL = 'http://127.0.0.1:5000'

course_seed_1 = {
    'name': 'Physics 1',
    'dept_course': 'PHY101',
}

course_seed_2 = {
    'name': 'Physics 2',
    'dept_course': 'PHY102',
}

course_seed_3 = {
    'name': 'Physics 3',
    'dept_course': 'PHY103',
}

course_seeds = [course_seed_1, course_seed_2, course_seed_3]


def createCourses():
    # create courses
    try:
        print('create courses')
        for seed in course_seeds:
            res = requests.post(url = URL + str('/api/course/create'), data=json.dumps(seed))
            print(str(res))

    except Exception as ex:
        print(ex)


user_seed_1 = {
    'netid': 'user1',
    'name': 'user name 1',
    'email': 'user1@princeton.ed',
}

user_seed_2 = {
    'netid': 'user2',
    'name': 'user name 2',
    'email': 'user2@princeton.ed',
}

user_seed_3 = {
    'netid': 'user 3',
    'name': 'user name 3',
    'email': 'user3@princeton.ed',
}

user_seeds = [user_seed_1, user_seed_2, user_seed_3]
def createUsers():
    # create users
    try:
        print('create user')
        for seed in user_seeds:
            res = requests.post(url = URL + str('/api/user/create'), data=json.dumps(seed))
            print(str(res))
        print('update user')
        res = requests.post(url = URL + str('/api/course/users'), data=json.dumps(seed))
        print(str(res))
        res = requests.post(url = URL + str('/api/course/users'), data=json.dumps(seed))
        print(str(res))
        res = requests.post(url = URL + str('/api/course/users'), data=json.dumps(seed))
        print(str(res))

    except Exception as ex:
        print(ex)
    


def main():
    createCourses()
    # createUsers()
    


    return None


if __name__ == "__main__":
    main()