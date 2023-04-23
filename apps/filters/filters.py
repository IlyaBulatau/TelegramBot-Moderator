from apps.config.config import SWEAR
import string



def swear_controller(msg_text):
        swears_list = SWEAR.split()

        for swear in swears_list:
            len_swer = len(swear)
            for i in range(0, len(msg_text)+len_swer):
                if swear == msg_text[i:i+len_swer].translate(str.maketrans('', '', string.punctuation)).lower():
                    return True
        return False
