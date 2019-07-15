import json
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from collections import OrderedDict
import operator

# Number of not accepted entries (not validated)
not_accepted = 0

# Number of corrected entries
corrected_pieces = 0

# Number of deleted entries
deleted_pieces = 0

# full number of entries
full_number = 0

# dict of validated timestamps
timestamps_validated = {}

# names dict
names_dict = {}

# open the main db
with open('db.json', encoding='utf-8') as json_file:
    # read the db.json
    dataset = json.load(json_file)
    newDataset = {}


    for entry in dataset:
        full_number += 1
        subject = dataset[entry].get("subject",None)
        if(subject != None):
            del(dataset[entry]['subject'])
            corrected_pieces += 1

        textBody = dataset[entry].get("textBody", None)
        if (textBody != None):
            del (dataset[entry]['textBody'])
            corrected_pieces += 1

        htmlBody = dataset[entry].get("htmlBody", None)
        if (htmlBody != None):
            del (dataset[entry]['htmlBody'])
            corrected_pieces += 1

        original_gender = dataset[entry].get("original_gender", None)
        if (original_gender != None):
            del (dataset[entry]['original_gender'])
            corrected_pieces += 1

        salutation = dataset[entry].get("salutation", None)
        if (salutation != None):
            del (dataset[entry]['salutation'])
            corrected_pieces += 1

        ip_address = dataset[entry].get("ip_address", None)
        if (ip_address != None):
            del (dataset[entry]['ip_address'])
            corrected_pieces += 1

        link = dataset[entry].get("link", None)
        if (link != None):
            del (dataset[entry]['link'])
            corrected_pieces += 1

        if(dataset[entry]['validated'] != 1):
            not_accepted = not_accepted + 1

        if(dataset[entry]['validated'] == 1):
            dt_object = str(dt.date.fromtimestamp(dataset[entry]['confirmation_time']/1000.0))
            if (dt_object in timestamps_validated):
                timestamps_validated[dt_object] = timestamps_validated[dt_object] + 1
            else:
                timestamps_validated[dt_object] = 0

        if(dataset[entry]['email'] == 'christian@shootclever.com'):
            deleted_pieces += 1
        else:

            newDataset[entry] = dataset[entry]
            ### names dict
            name = newDataset[entry]['first_name'] + ' ' + newDataset[entry]['last_name']
            if (name in names_dict):
                names_dict[name] = names_dict[name] + 1
            else:
                names_dict[name] = 0

    json.dump(newDataset, open("test.json", "w"), ensure_ascii=False)


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


print("Number of not accepted " + str(not_accepted))
print("Number of items " + str(full_number))
print("Percentage not accepted " + str(not_accepted / (full_number / 100)))

print("Total of valid entries " + str(full_number - not_accepted))


print("Number of corrected " + str(corrected_pieces))
print("Number of deleted " + str(deleted_pieces))
