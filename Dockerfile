FROM amazoncorretto:17

WORKDIR /server

COPY ./server-files/eula.txt .
COPY ./server-files/server-setup-config.yaml .
COPY ./server-files/start-server.sh .

ENTRYPOINT [ "./start-server.sh" ]

# COPY ./wait.sh .
# CMD ["./wait.sh"]