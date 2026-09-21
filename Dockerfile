FROM public.ecr.aws/docker/library/python:3.12-slim

COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.8.4 /lambda-adapter /opt/extensions/lambda-adapter

WORKDIR /var/task

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ ./src/

ENV PORT=8000
ENV AWS_LWA_INVOKE_MODE=response_stream

CMD ["python", "-m", "src.server"]