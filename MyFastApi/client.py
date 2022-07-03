from http import cookies
import requests


URL = 'http://localhost:8000/api/v1/users'
USER = {
  "username": "eduardoonetto",
  "password": "12345"
}


response = requests.post(URL+'/login', json=USER)
print(response)

if response.status_code == 200:
    print('Usuario Autenticado')
    #get cookies
    user_id = response.cookies.get_dict().get('user_id')
    print(user_id)
    cookies = {
        "user_id" : user_id
    }
    #get reviews by user_id from cookie
    response = requests.get(URL+'/reviews', cookies=cookies)
    print(response)
    if response.status_code == 200:
        for review in response.json():
            print(f"{review['review']} - {review['score']}")