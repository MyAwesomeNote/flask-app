FROM python:3.11

COPY . /app
WORKDIR /app

# RUN apt-get update

RUN mv /app/init.bat /app/init.sh
RUN chmod +x /app/init.sh

RUN echo '#!/bin/bash' > /app/run.sh && cat /app/run.bat >> /app/run.sh && chmod +x /app/run.sh
RUN chmod +x /app/run.sh

EXPOSE 5000

RUN sed -i 's/\r$//' /app/init.sh
RUN sed -i 's/\r$//' /app/run.sh

RUN /app/init.sh

CMD ["./run.sh"]
