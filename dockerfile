FROM alpine:3.14
RUN apk add --update python3 py3-pip
RUN pip install fastapi
RUN pip install uvicorn
# RUN pip install jinja2
RUN pip install python-multipart
RUN pip install pymongo
WORKDIR /app
COPY . /app
CMD ["uvicorn", "router:app", "--host", "0.0.0.0", "--port", "80"]
EXPOSE 80