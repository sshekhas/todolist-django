
from datetime import datetime
import random
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token as TokenModel
from django.contrib.auth import get_user_model

def create_token_for_user(user):
    token, _ = TokenModel.objects.get_or_create(user=user)
    user.last_login = datetime.now()
    user.save()
    return token

def destroy_token_for_user(user):
    try:
        TokenModel.objects.get(user=user).delete()
    except ObjectDoesNotExist:
        pass


def get_similer_username(username: str, existing_set: set[str] = None) -> list[str]: 
    
    if existing_set is None or len(existing_set) == 0:
        existing = get_user_model().objects.only("username")
        existing_set = set()
        for user in existing:
            existing_set.add(user.username)
    suggested_names = []
    for _ in range(0,10):
        if len(suggested_names) > 2:
            return suggested_names
        new_username = generate_username(username)
        if new_username in existing_set:
            continue
        suggested_names.append(new_username)
    
    for _ in range(0,10):
        if len(suggested_names) > 2:
            return suggested_names
        new_username = generate_username(username, append_at_start=True)
        if new_username in existing_set:
            continue
        suggested_names.append(new_username)
    
    for _ in range(0,10):
        if len(suggested_names) > 2:
            return suggested_names
        new_username = generate_username(username, append_at_mid=True)
        if new_username in existing_set:
            continue
        suggested_names.append(new_username)

    while len(suggested_names) < 3:
        ran_val = random.randint(0,100)
        if ran_val < 34:
            new_username = generate_username(username)
        elif ran_val > 66:
            new_username = generate_username(username, append_at_start=True)
        else:
            new_username = generate_username(username, append_at_mid=True)
        if new_username in existing_set:
            continue
        suggested_names.append(new_username)
    return suggested_names
    
   


 
def generate_username(name_of_user: str, **kwargs) -> str:
    minimum_specia_char = 2
    minimum_digits = 2
    min_len_of_username = 8
    special_chars = ['@','.','+','-', '_']
 
    username = ""
 
    name_of_user = "".join(name_of_user.split())
 
    name_of_user = name_of_user.lower()
 
    minimum_char_from_name = min_len_of_username-minimum_digits-minimum_specia_char
 
    for i in range(random.randint(minimum_char_from_name,len(name_of_user))):
        username += name_of_user[i]
 
    temp_list = []
    for i in range(minimum_digits):
        temp_list.append(str(random.randint(0,9)))
 
    for i in range(minimum_specia_char):
        temp_list.append(special_chars[random.randint(0,len(special_chars)-1)])
 
    random.shuffle(temp_list)
    temp = "".join(temp_list)
    if kwargs.get("append_at_start"):
        username = temp + username
    elif kwargs.get("append_at_mid"):
        username1 = username[:len(username)//2]
        username2 = username[len(username)//2:]
        username = username1 + temp + username2
    else:
        username += temp
 
    return username