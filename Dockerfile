# syntax=docker/dockerfile:1.2
FROM python:3.11-slim
# put you docker configuration here

WORKDIR /app
COPY . .

ARG PIP_ROOT_USER_ACTION=ignore
RUN pip install --upgrade pip
RUN pip install -c requirements.txt --progress-bar off .
CMD ["uvicorn", "challenge:app", "--host", "0.0.0.0"]
EXPOSE 8000
