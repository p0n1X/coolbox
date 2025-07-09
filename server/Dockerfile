FROM python:3.9

ENV PYTHONUNBUFFERED=1

WORKDIR /data_app

COPY . /data_app/.

RUN rm -rf /data_app/venv
RUN python3 -m pip install --upgrade pip

RUN pip install -r  requirements.txt --no-cache

EXPOSE 8000

CMD ["make", "run_app"]