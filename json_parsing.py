import json
string_as_json_format = '{"answer": "Hallo user"}'
obj = json.loads(string_as_json_format)
key = 'answer'
if key in obj:
    print(obj[key])
else:
    print(f"Ключа {key} нет в словаре ")

print(json.dumps(obj))



