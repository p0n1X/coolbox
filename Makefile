run_app:
	sleep 15
	python manage.py makemigrations
	python manage.py migrate
	python manage.py flush --noinput
	python manage.py loaddata server/data.json
	python manage.py runserver 0.0.0.0:8000

run_test:
	docker exec data_app python manage.py test