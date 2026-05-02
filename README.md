```bash
python -m venv .venv
source .venv/bin/activate   

pip install -r requirements.txt
cp .env.example .env

alembic upgrade head
python seed.py
uvicorn main:app --reload
```


```bash
pytest -v
```

```bash
# 9.1
curl http://localhost:8000/products

# 10.1 
curl -i http://localhost:8000/errors/items/999                       # 404 
curl -i -X POST "http://localhost:8000/errors/buy/2?quantity=5"      # 409 
curl -X POST "http://localhost:8000/errors/buy/1?quantity=2"         # ok

# 10.2
curl -X POST -H "Content-Type: application/json" \
  -d '{"username":"alice","age":25,"email":"a@b.com","password":"qwerty12"}' \
  http://localhost:8000/validation/users

# 11
curl -X POST -H "Content-Type: application/json" \
  -d '{"username":"alice","age":25}' http://localhost:8000/users
curl http://localhost:8000/users/1
curl -X DELETE http://localhost:8000/users/1
```
