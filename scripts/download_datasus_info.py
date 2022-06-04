import calendar
import datetime
import os
import shutil
import tempfile
import urllib.request as request
import zipfile
from contextlib import closing

import boto3 as boto3

# missing files on Datasus
SKIPS = ["201801"]


def add_months(source_date, months):
    month = source_date.month - 1 + months
    year = source_date.year + month // 12
    month = month % 12 + 1
    day = min(source_date.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)


def cnes_get_urls(start, end):
    dates_urls = dict()
    i = start
    while (end - i).days > 0:
        date = f"{i.year}{str(i.month).rjust(2, '0')}"
        urlcns = "ftp://ftp.datasus.gov.br/cnes/BASE_DE_DADOS_CNES_" + f"{i.year}{str(i.month).rjust(2, '0')}" + ".ZIP"
        if date not in SKIPS:
            dates_urls.update({date: urlcns})
        i = add_months(i, 1)

    return dates_urls


def download(target_url, output_url):
    print(f"Downloading {target_url} to {output_url}")
    output_url_path = os.path.dirname(output_url)
    if not os.path.exists(output_url_path):
        os.mkdir(output_url_path)
    if os.path.exists(output_url):
        return output_url
    with closing(request.urlopen(target_url)) as r:
        with open(output_url, 'wb') as f:
            shutil.copyfileobj(r, f)
            return output_url


def unzip(target_url, output_url, members=None):
    print(f"Unzipping files {members} from {target_url} to {output_url}")
    zip = zipfile.ZipFile(target_url)
    if members:
        for member in members:
            zip.extract(member=member, path=output_url)
    else:
        zip.extractall(output_url)
    return output_url


def to_s3(local_file, bucket, key):
    print(f"Uploading {local_file} to {bucket}/{key}")
    s3c = boto3.client("s3", region_name="us-east-1")
    s3c.upload_file(local_file, bucket, key)


def get_filename(url):
    return url.split("/").pop()


def clear_extension(filename):
    return filename.split(".")[0]


def cli():
    """
    Download CNES files from Datasus ftp and store in a location adding the partition (data's date)
    :return:
    """
    # reconfigure to run to all files
    # initial_moment = datetime.date.fromisoformat("2018-02-01")
    initial_moment = datetime.date.fromisoformat("2020-08-01")
    final_moment = datetime.date.fromisoformat("2022-01-01")
    dates_urls: dict[str, str] = cnes_get_urls(initial_moment, final_moment)

    context = tempfile.gettempdir()
    print(f"Using context {tempfile.gettempdir()}, create data warehouse from {initial_moment.isoformat()} "
          f"to {final_moment.isoformat()}")
    for date, url in dates_urls.items():
        download(url, f"{context}/{get_filename(url)}")
        unzip(f"{context}/{get_filename(url)}", f"{context}/BASE_DE_DADOS_CNES",
              [f"tbEstabelecimento{date}.csv"])
        to_s3(local_file=f"{context}/BASE_DE_DADOS_CNES/tbEstabelecimento{date}.csv",
              bucket="fernando-bontorin-datasus",
              key=f"tbEstabelecimento{date}.csv")


if __name__ == "__main__":
    cli()