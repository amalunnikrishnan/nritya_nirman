FROM python:3.10 AS base

WORKDIR /app

FROM base AS deps
COPY ./requirements.txt ./
RUN pip install -r requirements.txt

FROM deps AS runner

COPY . .
EXPOSE 8501

CMD [ "python3", "-m" , "streamlit", "run", "app.py"]
