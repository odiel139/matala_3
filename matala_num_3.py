# -*- coding: utf-8 -*-
"""
Created on Tue May  4 20:52:33 2021

@author: odiel
"""
import re
import json
import os

#########################################################################
#שים לב, יש להכניס את הנתיב שבו שמור קובץ הטקסט באמצע הקוד ובסופו.
def get_metadata(first_lines):

    first_line, second_line = first_lines
    creation_date = re.search(r'\d{1}.\d{1}.\d{4}, \d{2}:\d{2}', first_line) or re.search(r'\d{1}.\d{1}.\d{4}, \d{1}:\d{2}', first_line)
    creation_date = creation_date.group()

    # get only alpha beta characters
    words = re.sub('[^A-Za-z\u0590-\u05fe ]+', '', second_line)

    # if you are the creator
    if 'יצרת' in words:
        chat_name = words.split("יצרת את הקבוצה")[1].strip()
        creator = 'אתה'

    else:
        # get the chat name indexes in the string
        start = words.find("הקבוצה") + len("הקבוצה")
        end = words.find("נוצרה על ידי")

        chat_name = words[start:end].strip()

        creator = second_line.split('נוצרה על ידי')[-1]

        # remove special characters from creator name
        creator = re.sub('[^A-Za-z0-9\u0590-\u05fe +\-]+', '', creator).strip()

    return {'creation_date': creation_date, 'chat_name': chat_name, 'creator': creator}


def whatsapp_group(local_path_to_file):

    list_of_dict = []
    count_id = 1
    dict_id = dict()
    n = -1

    with open(local_path_to_file,encoding="utf-8") as f:
        content = f.readlines()

    metadata = get_metadata(content[:2])

    for line in content[2:]: # iterate over the chat

        dict1 = dict()
        line = line.strip()
        check_the_line = line.split("-")
        check_the_line = check_the_line[1:]
        check_the_line = str(check_the_line)
        # if(check_the_line.find(":")==-1):
        # pass
        if ":" not in line:
            # A situation where there are no colon at all, a situation where the continuation of someone's sentence has dropped to another line
            line = line.strip()
            # todo may cause out of range error
            # todo may cause key error
            list_of_dict[-1]['text'] = list_of_dict[-1]['text'] + " " + line
            # צריך להוסיף את השורה הזו לשורה שמעליה

        elif check_the_line.find("הוסיף/ה") == n and check_the_line.find(":") != -1:
            # print(line)
            line = line.strip()
            # A line where there is a message that someone has sent - with a cell phone number or a contact name
            x1 = line.split("-")
            x2 = x1[1].split(":")
            person = x2[0]
            # print(person)
            # for id in dict_id:
            if person not in dict_id:
                dict_id[person] = str(count_id)
                # id_of_last_line=count_id
                dict1["id"] = dict_id[person]
                count_id = count_id + 1

            else:
                dict1["id"] = dict_id[person]
            # date_time=line.split()
            # datetime=date_time[1]+" "+date_time[0]
            datetime = line.split("-")[0]
            dict1["datetime"] = datetime
            x1 = line.split("-", 1)
            x2 = x1[1].split(":")
            text = x2[1]
            dict1["text"] = text
            # print(count_id)
            # print(dict1)
            list_of_dict.append(dict1)

    metadata["num_of_participants"] = len(dict_id)

    all_data = {"messages": list_of_dict, "metadata": metadata}
    
    file=open(r"C:\Users\odiel\Desktop\limudim\python\matala3\�צאט WhatsApp עם יום הולדת בנות לנויה.txt",encoding='utf-8')
    file = file.readlines()
    for line in file:
        if(line.find('נוצרה על ידי')!=n):
            line=line.strip()
            the_name=line.split(":")[1]
            chat_name=the_name[the_name.find('"'):the_name.find('נוצרה על ידי')]
            chat_name=chat_name.rstrip()
            chat_name=chat_name[1:len(chat_name)-1]
        if(line.find('יצרת את הקבוצה')!=n):
            line=line.strip()
            the_name=line.split(":")[1]
            chat_name=the_name[the_name.find('"'):the_name.find('נוצרה על ידי')]
            chat_name=chat_name.rstrip()
            chat_name=chat_name[1:len(chat_name)-1]    
    
    chat_name=chat_name+".txt"

    json_file_name = chat_name
    local_path_to_dir = os.path.dirname(local_path_to_file)

    with open(os.path.join(local_path_to_dir, json_file_name), 'w', encoding='utf8') as file_json:
        json.dump(all_data, file_json, ensure_ascii=False, indent=4)

    return all_data


whatsapp_group(r"C:\Users\odiel\Desktop\limudim\python\matala3\�צאט WhatsApp עם יום הולדת בנות לנויה.txt")
