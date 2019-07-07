import json
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from collections import OrderedDict
import operator


import time

notAccepted = 0
correctedPieces = 0
full_number = 0
timestamps_validated = {}
names_dict = {}

with open('db.json', encoding='utf-8') as json_file:
    dataset = json.load(json_file)


    for entry in dataset:
        full_number += 1
        subject = dataset[entry].get("subject",None)
        if(subject != None):
            del(dataset[entry]['subject'])
            correctedPieces += 1

        textBody = dataset[entry].get("textBody", None)
        if (textBody != None):
            del (dataset[entry]['textBody'])
            correctedPieces += 1

        htmlBody = dataset[entry].get("htmlBody", None)
        if (htmlBody != None):
            del (dataset[entry]['htmlBody'])
            correctedPieces += 1

        original_gender = dataset[entry].get("original_gender", None)
        if (original_gender != None):
            del (dataset[entry]['original_gender'])
            correctedPieces += 1

        salutation = dataset[entry].get("salutation", None)
        if (salutation != None):
            del (dataset[entry]['salutation'])
            correctedPieces += 1

        ip_address = dataset[entry].get("ip_address", None)
        if (ip_address != None):
            del (dataset[entry]['ip_address'])
            correctedPieces += 1

        link = dataset[entry].get("link", None)
        if (link != None):
            del (dataset[entry]['link'])
            correctedPieces += 1

        if(dataset[entry]['validated'] != 1):
            notAccepted = notAccepted + 1

        if(dataset[entry]['validated'] == 1):
            dt_object = str(dt.date.fromtimestamp(dataset[entry]['confirmation_time']/1000.0))
            if (dt_object in timestamps_validated):
                timestamps_validated[dt_object] = timestamps_validated[dt_object] + 1
            else:
                timestamps_validated[dt_object] = 0

        ### names dict
        name = dataset[entry]['first_name'] + ' ' + dataset[entry]['last_name']
        if (name in names_dict):
            names_dict[name] = names_dict[name] + 1
        else:
            names_dict[name] = 0

    json.dump(dataset, open("test.json", "w"), ensure_ascii=False)


duplicates = 0
cleaned_names_dict = {}
for key, value in names_dict.items():
    if (value > 1):
        cleaned_names_dict[key] = value
        duplicates += value - 1
names_dict_sorted = sorted(cleaned_names_dict.items(), key=operator.itemgetter(1))

print("Duplicates")
print("Duplicated Entries " + str(len(cleaned_names_dict)))
print("Duplicates in total " + str(duplicates))
print("*************")

timestamps_validated_sorted = OrderedDict(sorted(timestamps_validated.items()))
plt.bar(range(len(timestamps_validated_sorted)), timestamps_validated_sorted.values(), align='center')
plt.xticks(range(len(timestamps_validated_sorted)), list(timestamps_validated_sorted.keys()))
plt.xticks(rotation=90)
plt.yticks(np.arange(0, 1400, step=100))
plt.grid(True)
plt.show()


print("Number of not accepted " + str(notAccepted))
print("Number of items " + str(full_number))
print("Percentage not accepted " + str(notAccepted / (full_number / 100)))

print("Total of valid entries " + str(full_number - notAccepted))


print("Number of corrected " + str(correctedPieces))
