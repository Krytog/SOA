# Примеры комманд для теста API:


```
curl -H "Content-Type: application/json" -d '{"login": "roflik", "password": "12345"}' -X POST http://localhost:31337/api/signup
```

```
curl -H "Content-Type: application/json" -d '{"login": "roflik", "password": "12345"}' -X POST http://localhost:31337/api/login
```

```
curl -H "Content-Type: application/json" -H "Auth: <токен из предыдущей команды>" -d '{"name": "Roflonimo", "surname": "Baklazhanenko", "bio": "young tomato", "birthdate": "01.01.1970", "phone": "+123456789", "email": "bebra@gmail.com"}' -X PUT http://localhost:31337/api/update
```

```
curl http://localhost:31337/api/about/roflik
```

При первом запуске в новом томе alembic автоматически произведёт миграцию бд.

Чтобы удалить том, который маунтится в бд, нужно написать:
```
docker volume rm soa_db_main
```


# Примеры комманд для теста новго API:
```
#curl -H "Content-Type: application/json" -H "Auth: <token>" -d '{"content": "A new post!"}' -X POST http://localhost:31337/api/content/create_post
```


```
#curl -H "Content-Type: application/json" -H "Auth: <token>" -d '{"content": "Hey guys! I have just decided to update this old post!"}' -X PUT http://localhost:31337/api/content/update_post/{<post_id>}
```

```
#curl -H "Content-Type: application/json" -H "Auth: <token>" http://localhost:31337/api/content/get_post/{<post_id>}
```

```
#curl -H "Content-Type: application/json" -H "Auth: <token>" -X PUT http://localhost:31337/api/content/delete_post/{<post_id>}
```

```
curl -H "Content-Type: application/json" -H "Auth: <token>" -d '{"user_id": "1", "page": "1", "per_page": "2"}' -X GET http://localhost:31337/api/content/get_postslist
```