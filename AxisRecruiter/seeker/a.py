import glob
import wget;

url='https://docs.intersystems.com/irisforhealth20231/csp/docbook/pdfs.zip';
wget.download(url)
# extract docs
import zipfile
with zipfile.ZipFile('pdfs.zip','r') as zip_ref:
  zip_ref.extractall('.')