import os
import sys
import requests
from mysqlUtils import *
from download_config import *

def download(target_url, output_dir, filename, mode='skip', timeout=30, retries=3):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    file_path = os.sep.join([output_dir, filename])
    if os.path.exists(file_path):
        return file_path

    for i in range(retries):
        try:
            response = requests.get(target_url, timeout=timeout)
            with open(file_path, 'wb') as fp:
                fp.write(response.content)
            break
        except Exception:
            print 'download error, retry ', i+1, ' times, url: ', target_url
    return file_path

def downloadfromdb(hospital_id, study_id):
    host = '127.0.0.1'
    user = 'efilm'
    pwd = 'efilm'
    db = 'efilm'
    sql = """
          SELECT dcmImg FROM INSTANCE WHERE BINARY hospitalId = '%s' AND studyId = '%s'
          """%(hospital_id, study_id)

    output_dir = '/home/huiying/Downloads/dicom'
    mode = 'skip'
    timeout = 30
    retries = 3

    print 'SQL : ', sql
    print
    print 'Results :'
    results = fetchall(host, user, pwd, db, sql)
    if results:
        # fetch results log
        i = 0
        for result in results:
            i += 1
            print str(i).rjust(10), result[0]

        print

        # download
        print
        print '.......... start download ..........'
        print
        i = 0
        output_dir = output_dir + '/' + study_id
        for result in results:
            target_url = result[0]
            filename = target_url[(target_url.rfind('/') + 1) : ]
            i += 1
            print str(i).rjust(10), filename, ' downloading......'
            download(target_url, output_dir, filename, mode, timeout, retries)
        print
        print '.......... end download ..........'
        print
    return

def downloadfromurl():
    target_urls = [
        'http://192.168.1.205:8011/group1/M00/03/C0/wKgBzVn_wzSAer4LAPAE5lJnC94233.dcm',
        'http://192.168.1.205:8011/group1/M00/03/BF/wKgBzVn_wyqASj7vAPAE5vX1N98897.dcm',
        'http://192.168.1.205:8011/group1/M00/03/C0/wKgBzVn_w3mAeAf0APAE5u8_Zec081.dcm',
        'http://192.168.1.205:8011/group1/M00/03/BC/wKgBzVn9Y8yAIFFUAPAE6pAl8VM769.dcm' 
    ]
    output_dir = '/home/huiying/Downloads/dicom'
    mode = 'skip'
    timeout = 30
    retries = 3
    print
    print '.......... start download ..........'
    print

    i = 0 
    for target_url in target_urls:
        filename = target_url[(target_url.rfind('/') + 1) : ]
        i += 1
        print str(i).rjust(10), filename
        download(target_url, output_dir, filename, mode, timeout, retries)

    print
    print '.......... end download ..........'
    print


if __name__ == '__main__':
    if len(DOWNLOAD_STUDY_LIST) > 0:
        for study in DOWNLOAD_STUDY_LIST:
            downloadfromdb(study['hospital_id'], study['study_id'])
    else:
        print 'No study in config to download. Please input study list in download_config.py ...'
    #downloadfromurl()

    """
    if sys.argv and len(sys.argv) > 1:
        study_id = sys.argv[1]
        downloadfromdb(study_id)
    else:
        print 'Please input argv of study_id...'
    """
