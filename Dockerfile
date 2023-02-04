FROM python:3.8
WORKDIR /polymath
COPY . .
RUN pip install -r requirements.txt
RUN sh build.sh

EXPOSE 8080
VOLUME /polymath/data
ENV PYTHONUNBUFFERED "1"
CMD ["python", "-u", "run"]