FROM python:3.9.12

ADD requirements.txt .
RUN python -m pip install -r requirements.txt

ADD portescap_mysql_fcs/portescap_mysql_fcs/
WORKDIR /portescap_mysql_fcs/
CMD python /portescap_mysql_fcs/main.py