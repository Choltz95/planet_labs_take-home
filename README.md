Chester Holtz Planet Labs Take Home Code Test
============================================

## Overview

Implementation of a REST service using Python and the Flask web frmework. A user record is represented in JSON as 
```json
{
    "first_name": "Joe",
    "last_name": "Smith",
    "userid": "jsmith",
    "groups": ["admins", "users"]
}
```
Interface provides all ths usual REST operations on an sqlite database - ie GET, POST, PUT, DELETE.

unfortunately, since I convert class attributes to a dictionary, I cannot retain any kind of key order in the json, so the responses are not as pretty as they could be.

## Example usage

```bash
curl -H "Content-Type: application/json" -X POST -d '{"name":"cs"}' http://127.0.0.1:5000/groups/
curl -H "Content-Type: application/json" -X POST -d '{"name":"mth"}' http://127.0.0.1:5000/groups/
curl -H "Content-Type: application/json" -X POST -d '{"userid":"choltz", "groups":["cs","mth"]}' http://127.0.0.1:5000/users/
curl -i -H "Content-Type: application/json" -X PUT -d '{"first_name":"Chester", "last_name":"Holtz"}' http://127.0.0.1:5000/users/choltz
```

```json
{
  "group_name": "cs", 
  "id": 1
}{
  "group_name": "mth", 
  "id": 3
}{
  "first_name": "", 
  "groups": [
    "cs", 
    "mth"
  ], 
  "id": 1, 
  "last_name": "", 
  "userid": "choltz"
}{
  "first_name": "Chester", 
  "groups": [
    "cs", 
    "mth"
  ], 
  "id": 1, 
  "last_name": "Holtz", 
  "userid": "choltz"
}
```


## Installation

Test the app to be hosted on heroku
or
Clone the repository and run pip install -r requirements.txt, then run python app.py

## Tests

bash tests.txt > output.txt

## Future

given more time I would have liked to further refine the general structure of the app. There are some ugly hacks (model -> dictionary -> json), and the code is in general not my best.