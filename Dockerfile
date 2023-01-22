FROM python:3-alpine3.15
WORKDIR /app
COPY . /app
RUN pip install -r requiraments.txt
EXPOSE 5000
CMD python ./run.py
# CMD ["flask", "run", "--host", "0.0.0.0"]

# FROM python:3.10
# EXPOSE 5000
# WORKDIR /app
# COPY requiraments.txt .
# RUN pip install -r requiraments.txt
# COPY . .
# CMD ["flask", "run", "--host", "0.0.0.0"]