import json
import gspread

with open("credentials.json", encoding="utf-8") as file:
    credentials = json.load(file)

with open("spreadsheets.json", encoding="utf-8") as file:
    spreadsheets = json.load(file)


gc = gspread.service_account_from_dict(credentials)

sh_input = gc.open_by_key(spreadsheets["input"]).sheet1
sh_output = gc.open_by_key(spreadsheets["output"]).sheet1
for i in range(2, 50):
    email = sh_input.acell(f'B{i}').value
    if not email:
        break
    user = email.split("@")[0]
    points = sh_input.acell(f'L{i}').value
    sh_output.update(f'A{i}', user)
    sh_output.update(f'B{i}', points)

