# ----------------------------- IMPORTS ------------------------------------ #

import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime
from os import path
import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.S3_hook import S3Hook

# ----------------------------- EXTRACT DATA ------------------------------- #

def get_rj_table_info_from_url(
        URL="http://www.insideairbnb.com/get-the-data/"):
    """
    Função que extrai todos os dados da tabela "Rio de Janeiro" 
    do site "Inside Airbnb" e salva as informações 
    no arquivo "info_from_rj_table.html".
    """
    resp = requests.get(URL)
    print(resp)
    html_like_text = resp.text
    search = re.findall("<table.*?>(.*?)</table>", html_like_text)
    for cities in search:
        if 'rio-de-janeiro' in cities:
            with open('/tmp/info_from_rj_table.html', 'w') as f:
                f.write(cities)


def get_urls_from_rj_table_info(data="/tmp/info_from_rj_table.html"):
    """
    Função que extrai as urls do arquivo info_from_rj_table.html e
    salva informações sobre estas em "extract_urls_info.txt".
    """
    with open(data, 'r') as f:
        soup = BeautifulSoup(f, 'html.parser')
        for a in soup.find_all('a'):
            if 'listings.csv.gz' in a.get('href'):
                url_listings = a.get('href')
            elif 'reviews.csv.gz' in a.get('href'):
                url_reviews = a.get('href')

    # Responses e Last-Modified:
    resp_url_listings = requests.get(url_listings)
    lm_listings = resp_url_listings.headers['Last-Modified']
    resp_url_reviews = requests.get(url_reviews)
    lm_reviews = resp_url_reviews.headers['Last-Modified']

    # Verificando se houve atualização nas urls do site:
    if lm_listings == 'Wed, 22 Jun 2022 17:58:20 GMT' and \
            lm_reviews == 'Wed, 22 Jun 2022 17:58:22 GMT':
        try:
            get_urls_from_rj_table_info
        except FileNotFoundError:
            with open('/tmp/extracted_urls_info.txt', 'a') as f:
                now = datetime.now()
                f.write(f"----------  {now}  ----------")
                f.write("\n")
                f.write(url_listings)
                f.write("\n")
                f.write(url_reviews)
    else:
        with open('/tmp/extracted_urls_info.txt', 'a') as f:
            now = datetime.now()
            f.write("\n")
            f.write("!!!!!!!!!! DADOS ATUALIZADOS !!!!!!!!!!")
            f.write("\n")
            f.write(f"----------  {now}  ----------")
            f.write("\n")
            f.write(url_listings)
            f.write("\n")
            f.write(url_reviews)
    return url_listings, url_reviews


def extract_data_from_url(ti):
    """
    Função que cria os dois arquivos .csv, a partir das urls
    onde encontram-se os dados de Listings e Reviews.
    """
    urls = ti.xcom_pull(task_ids=[
        'get_urls_from_rj_table_info'
    ])

    # Urls, suas Responses e Last-Modified:
    url_listings = urls[0][0]
    url_reviews = urls[0][1]
    resp_url_listings = requests.get(url_listings)
    lm_listings = resp_url_listings.headers['Last-Modified']
    resp_url_reviews = requests.get(url_reviews)
    lm_reviews = resp_url_reviews.headers['Last-Modified']

    # Definindo path para os arquivos .csv:
    datafile_listings = "/tmp/listings-rj-insideairbnb" + "-" + \
        lm_listings[:12].replace(' ', '').replace(',', '').lower() + ".csv"
    datafile_reviews = "/tmp/reviews-rj-insideairbnb" + "-" + \
        lm_reviews[:12].replace(' ', '').replace(',', '').lower() + ".csv"

    # Se os arquivos .csv ainda não existem, os crio:
    if path.exists(datafile_listings) == False and \
            path.exists(datafile_reviews) == False:
        # crio o arquivo de Listings:
        df = pd.read_csv(url_listings)
        with open(datafile_listings, "w") as f:
            df.to_csv(f, index=False)
        # crio o arquivo de Reviews:
        df = pd.read_csv(url_reviews)
        with open(datafile_reviews, "w") as f:
            df.to_csv(f, index=False)

    return datafile_listings, datafile_reviews

# ----------------------------- LOAD DATA ---------------------------------- #

def upload_to_s3(filename: str, key: str, bucket_name: str):
    hook = S3Hook('s3_conn')
    hook.load_file(filename=filename,
                   key=key,
                   bucket_name=bucket_name,
                   replace=True
                   )

# ----------------------------- DAG ---------------------------------------- #

with DAG(dag_id="extract_and_load_dag",
         description="DAG que extrai dados de urls presente no site \
            Inside Airbnb, os armazena no container local e faz o \
            upload destes dados para um bucket S3 da AWS.",
         start_date=datetime(2022, 9, 8),
         schedule_interval='@daily',
         catchup=False,
         ) as dag:

    # Extract:
    get_rj_table_info_from_url_task = PythonOperator(
        task_id="get_rj_table_info_from_url",
        python_callable=get_rj_table_info_from_url,
        dag=dag
    )

    get_urls_from_rj_table_info_task = PythonOperator(
        task_id="get_urls_from_rj_table_info",
        python_callable=get_urls_from_rj_table_info,
        dag=dag
    )

    extract_data_from_url_task = PythonOperator(
        task_id="extract_data_from_url",
        python_callable=extract_data_from_url,
        dag=dag
    )

    # Load:
    upload_to_s3_listings_task = PythonOperator(
        task_id='upload_to_s3_listings',
        python_callable=upload_to_s3,
        op_kwargs={
            'filename': '/tmp/listings-rj-insideairbnb-wed22jun.csv',
            'key': 'listings-rj-insideairbnb-wed22jun.csv',
            'bucket_name': 'lagoa-de-dados'
        }
    )

    upload_to_s3_reviews_task = PythonOperator(
        task_id='upload_to_s3_reviews',
        python_callable=upload_to_s3,
        op_kwargs={
            'filename': '/tmp/reviews-rj-insideairbnb-wed22jun.csv',
            'key': 'reviews-rj-insideairbnb-wed22jun.csv',
            'bucket_name': 'lagoa-de-dados'
        }
    )

# ------------------------------- RELAÇÃO ---------------------------------- #

get_rj_table_info_from_url_task >> \
    get_urls_from_rj_table_info_task >> \
    extract_data_from_url_task >> \
    [upload_to_s3_listings_task, upload_to_s3_reviews_task]
