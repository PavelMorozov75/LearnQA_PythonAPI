FROM python
WORKDIR /test_project/
COPY requirements.txt .
RUN pip install -r requirements.txt
ENV ENV=dev
CMD python -m pytest -s /test_project/tests/
# docker build -t pytest_runner .
# docker run --rm --mount type=bind,src=C:\Users\User\PycharmProjects\LearnQA_PythonAPI,target=/test_project/ pytest_runner
