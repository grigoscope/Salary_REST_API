import json
from secrets import token_hex
from typing import Optional, Tuple


def refresh_all_tokens(path_to_json: str) -> None:
    """
    Rotate every employee's token in the JSON store.
    """
    with open(path_to_json, 'r', encoding='utf-8') as f:
        employees = json.load(f)

    for emp in employees:
        emp['token'] = token_hex(20)

    with open(path_to_json, 'w', encoding='utf-8') as f:
        json.dump(employees, f, ensure_ascii=False, indent=2)

    print("All tokens have been refreshed.")


def generate_token(login: str, password: str, path_to_json: str) -> Optional[str]:
    """
    If credentials match, generate a new token, persist it, and return it.
    """
    with open(path_to_json, 'r', encoding='utf-8') as f:
        employees = json.load(f)

    for emp in employees:
        if emp['login'] == login and emp['password'] == password:
            new_token = token_hex(20)
            emp['token'] = new_token
            break
    else:
        return None

    with open(path_to_json, 'w', encoding='utf-8') as f:
        json.dump(employees, f, ensure_ascii=False, indent=2)

    return new_token


def get_salary_and_next_raise(token: str, path_to_json: str) -> Optional[Tuple[int, str]]:
    """
    Lookup salary and next raise date by token.
    """
    with open(path_to_json, 'r', encoding='utf-8') as f:
        employees = json.load(f)

    for emp in employees:
        if emp['token'] == token:
            return emp['current_salary'], emp['next_raise_date']

    return None
