FROM python:3.8
LABEL maintainer="noemail@website.domain"
COPY . /stuff
WORKDIR /stuff
RUN pip install -r requirements.txt
CMD ["python", "api.py"]
