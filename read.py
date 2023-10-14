import json
import gspread
import time

with open("credentials.json", encoding="utf-8") as file:
    credentials = json.load(file)

with open("spreadsheets.json", encoding="utf-8") as file:
    spreadsheets = json.load(file)

with open("quiz_params.json", encoding="utf-8") as file:
    quiz_params = json.load(file)

lesson = input("Zadej číslo lekce: ")
if lesson not in quiz_params:
    email_points = input("Zadej číslo sloupce s e-mailovými adresami: ")
    column_points = input("Zadej číslo sloupce s výsledky: ")
    quiz_params[lesson] = {}
    quiz_params[lesson]["email_points"] = email_points
    quiz_params[lesson]["column_points"] = column_points
    with open("quiz_params.json", "w", encoding="utf-8") as file:
        json.dump(quiz_params, file, indent=4)
else:
    email_points = quiz_params[lesson]["email_points"]
    column_points = quiz_params[lesson]["column_points"]

gc = gspread.service_account_from_dict(credentials)
sh_input = gc.open_by_key(spreadsheets[f"input_{lesson}"]).sheet1
sh_output = gc.open_by_key(spreadsheets["output"]).sheet1

email_list = sh_input.col_values(email_points)
points_list = sh_input.col_values(int(column_points))
data_list = zip(email_list, points_list)
email_output_list = sh_output.col_values(1)
added_emails = 0

for i, data_row in enumerate(data_list):
    email, points = data_row
    if i == 0:
        continue
    if not email or not points:
        continue
    user = email.split("@")[0]
    if user in email_output_list:
        index_destination = email_output_list.index(user)
        sh_output.update_cell(index_destination + 1, int(lesson) + 1, float(points))
    else:
        index_destination = len([x for x in email_output_list if x]) + added_emails
        sh_output.update_cell(index_destination + 1, 1, user)
        sh_output.update_cell(index_destination + 1, int(lesson) + 1, float(points))
        added_emails += 1

