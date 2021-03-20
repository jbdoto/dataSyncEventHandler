FROM public.ecr.aws/lambda/python:3.8

COPY app.py /var/task

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "app.handle_event" ]
