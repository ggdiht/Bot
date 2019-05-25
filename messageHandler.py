import vkapi
import os
import importlib
from command_system import command_list
from dbquery import db_ans

def get_answer(body, user_id):
    # Сообщение по умолчанию если распознать не удастся
    ga = ""

    try:
        if body.split()[0] == "[club146231252|GG" and body.split()[1] == "ФИВТ]":
            body = " ".join(map(str, body.split()[2:]))
    except:
        pass

    try:
        if body.split()[0] == "[club146231252|@ggdiht]":
            body = " ".join(map(str, body.split()[1:]))
    except:
        pass



    ans = db_ans("select level from Access where id = " + str(user_id));
    if ans:
        level = ans[0]
    else:
        level = 0

    for c in command_list:
        if body.split()[0].lower() in c.keys:
            if level in c.min_level:
                ga = c.process(body, level, user_id)
            else:
                ga = "Недостаточно прав", ""
        if len(body.split()) >= 2:
            if (body.split()[0].lower() + " " + body.split()[1].lower()) in c.keys:
                if level in c.min_level:
                    ga = c.process(body, level, user_id)
                else:
                    ga = "Недостаточно прав", ""
    return ga


def create_answer(data, token):
    load_modules()
    user_id = data['peer_id']
    ga = get_answer(data['text'], user_id)
    if len(ga) == 2:
        message, attachment = ga
    else:
        message = ga
        attachment = ""
    if message != "" or attachment != "":
        vkapi.send_message(user_id, token, message, attachment)

def load_modules():
   # путь от рабочей директории
   files = os.listdir("mysite/commands")
   modules = filter(lambda x: x.endswith('.py'), files)
   for m in modules:
       importlib.import_module("commands." + m[0:-3])

