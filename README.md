Task 2 
--
HTTP API через которое можно получить:  
* список всех продуктов с их категориями,  
* список категорий с продуктами,  
* список всех пар «Имя продукта – Имя категории».  

В SQL базе данных есть продукты и категории. Одному продукту может соответствовать много категорий, в одной категории может быть много продуктов.

### Install  

Download repo
```
git clone https://github.com/babyBosss/MindBoxTask2.git
```
Launch the application
```
cd MindBoxTask2 

docker-compose up 
```

Now in the browser you can see the result of the program at:

http://127.0.0.1:8888/get_products  
http://127.0.0.1:8888/get_categories  
http://127.0.0.1:8888/get_pairs  