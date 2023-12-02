FROM fedora
RUN dnf update -y
RUN dnf install python3 -y
RUN dnf install python3-pip -y
RUN mkdir /healthchecker
WORKDIR /healthchecker
RUN pip3 install flask
RUN pip3 install requests
COPY healthchecker/main.py .
EXPOSE 8000
ENTRYPOINT python3 main.py $IP_TO_CHECK
