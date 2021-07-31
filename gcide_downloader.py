import requests
import zipfile
import shutil
import os


def download_gcide_xml(url='http://www.ibiblio.org/webster/gcide_xml-0.51.zip'):
    r = requests.get(url, allow_redirects=True)
    open('gcide_xml-0.51.zip', 'wb').write(r.content)
    zipfile.ZipFile('gcide_xml-0.51.zip', 'r').extractall('gcide_xml_unzipped')
    shutil.move('gcide_xml_unzipped/gcide_xml-0.51/xml_files', '.')
    shutil.rmtree('gcide_xml_unzipped')
    os.remove('gcide_xml-0.51.zip')
