# 💻 How to Setup
## 1. Set environment variables
First you need to create ```.env``` file in the main directory with the data from ```env_example``` file.

## 2. Build docker containers
```
docker-compose build
```

## 3.Run docker container
```
docker-compose up
```

## 4. Run tests
```
    make run_test
```


# 🔐 Administrator for BE
```
username: admin
password: admin
```

# 🏗 How to work
Django REST API endpoint. When we call only this endpoint without any parameters we're getting all data information about companies   
```
/api/companies/
```

## 1. Free-form or structured search string
```
country:Bulgaria size > 100
```
Call with API like search query with 'q' parameter
```
/api/companies/?q=country:Bulgaria size > 100
```

## 2. Support also partial string searching
We can search with part of "Bulgaria" like "Bulg". This searching method work with all text fields in our database - "name", "country", "industry" and etc.
```
Bulg size > 100
```
Call with API 
```
/api/companies/?q=Bulg size > 100
```

## 3. Implemented sorting in free-form search
When we're using this form also can sort our data
```
country:Bulgaria size=DESC
```
Call with API 
```
/api/companies/?q=country:Bulgaria size=DESC
```

## 4. Filtering with combinations of multiple conditions
```
country=Bulgaria AND net_income>100 NOT headquarters=Plovdiv
```
Call with API like filter query with 'filter' parameter

```
/api/companies/?filter=country=Bulgaria AND net_income>100 NOT headquarters=Plovdiv
```

## 5. Sortable by one or more fields with ascending and descending order
```
net_income=ASC
```

Call with API like sort query with 'sort' parameter
```
/api/companies/?sort=net_income=ASC
```

## 6. Combination with search, filter and sort also well good
This works only with direct call with API
```
/api/companies/?q=industry:Tech size>100 &filter=country=Bulgaria AND net_income>100 NOT headquarters=Plovdiv&sort=net_income=ASC
```