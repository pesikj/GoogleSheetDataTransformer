import json
import gspread
import time

with open("credentials.json", encoding="utf-8") as file:
    credentials = json.load(file)

with open("spreadsheets.json", encoding="utf-8") as file:
    spreadsheets = json.load(file)

lesson = input("Zadej číslo lekce: ")
column_points = input("Zadej číslo sloupec s výsledky: ")

gc = gspread.service_account_from_dict(credentials)
sh_input = gc.open_by_key(spreadsheets[f"input_{lesson}"]).sheet1
sh_output = gc.open_by_key(spreadsheets["output"]).sheet1

email_list = sh_input.col_values(2)
points_list = sh_input.col_values(int(column_points))
data_list = zip(email_list, points_list)
email_output_list = sh_output.col_values(1)

for i, data_row in enumerate(data_list):
    email, points = data_row
    if i == 0:
        continue
    if not email or not points:
        break
    user = email.split("@")[0]
    if user in email_output_list:
        index_destination = email_output_list.index(user)
        sh_output.update_cell(index_destination + 1, int(lesson) + 1, float(points))

