# Salary REST API

Minimal FastAPI service to:
1. **Authenticate** users by login/password → return token  
2. **Query** salary & next raise date by token  

Tokens auto-rotate every hour.

## Project structure
```bash
Salary_REST/
├─ app/
│  ├─ __init__.py
│  ├─ main.py
│  └─ utils.py
├─ employee.json
└─ req.txt
```

## Requirements

```bash
pip install -r req.txt
```

# Run
```bash
uvicorn app.main:app --reload
```

# Endpoints

## POST ```/token```
### **Body** (JSON)

```bash
{ "login": "user1", "password": "Rw28r8ktA-Fjvs3C" }
```

### **Response**
```bash
{ "token": "<token>" }
```

## GET  ```/salary```
### **Query Param**
```bash
?token=<your_token>
```

### **Response**
```bash
{
  "current_salary": 50000,
  "next_raise_date": "2026-11-01"
}
```