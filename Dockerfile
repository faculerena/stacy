FROM python:3.9-slim
RUN git clone --recurse-submodules https://github.com/faculerena/stacy /opt/stacy

WORKDIR /opt/stacy

COPY . .

RUN python3 -m venv venv
RUN ./venv/bin/pip install -r requirements.txt
RUN make

ENTRYPOINT ["sh", "-c", "ls -la && ls -la venv/bin && . venv/bin/activate && stacy-analyzer --target $INPUT_TARGET"]
