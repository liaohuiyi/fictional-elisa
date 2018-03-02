import os
import requests
from mysqlUtils import *
from remove_config import *

def remove(target_dir, filename):
    if not os.path.exists(target_dir):
        print '            ', target_dir, ' does not exsisted...'

    file_to_remove = os.sep.join([target_dir, filename])
    if os.path.exists(file_to_remove):
        os.remove(file_to_remove)
        print '             remove successfully!'
    else:
        print '             no such file: ', file_to_remove

    print

    return

def removefromdb(hospital_id, study_id):
    host = '127.0.0.1'
    user = 'efilm'
    pwd = 'efilm'
    db = 'efilm'
    sql1 = """DELETE FROM ORIGINALREPORT WHERE BINARY hospitalId = '%s' AND studyId = '%s'"""%(hospital_id, study_id)
    sql2 = """DELETE FROM CHECKINFO WHERE BINARY hospitalId = '%s' AND studyId = '%s'"""%(hospital_id, study_id)
    sql3 = """DELETE FROM PATIENT WHERE BINARY hospitalId = '%s' AND patientId = '%s'"""%(hospital_id, study_id)
    sql4 = """DELETE FROM INSTANCE WHERE BINARY hospitalId = '%s' AND studyId = '%s'"""%(hospital_id, study_id)
    sql5 = """DELETE FROM SERIES WHERE BINARY hospitalId = '%s' AND studyId = '%s'"""%(hospital_id, study_id)
    sql6 = """DELETE FROM STUDY WHERE BINARY hospitalId = '%s' AND studyId = '%s'"""%(hospital_id, study_id)
    sql7 = """DELETE FROM study_dx WHERE BINARY hospital_id = '%s' AND study_id = '%s'"""%(hospital_id, study_id)
    sql8 = """DELETE FROM study_series_dx WHERE BINARY hospital_id = '%s' AND study_id = '%s'"""%(hospital_id, study_id)
    sqls = [sql1, sql2, sql3, sql4, sql5, sql6, sql7, sql8]

    print
    print 'SQL : '
    print sqls
    print
    executedmsqls(host, user, pwd, db, sqls)
    return

def removefromfdfs(hospital_id, study_id):
    host = '127.0.0.1'
    user = 'efilm'
    pwd = 'efilm'
    db = 'efilm'
    sql = """SELECT jpgImg, jpegImg, dcmImg FROM INSTANCE WHERE BINARY hospitalId = '%s' AND studyId = '%s'"""%(hospital_id, study_id)
    print 'SQL : ', sql
    print
    results = fetchall(host, user, pwd, db, sql)
    if results:
        target_dir = '/data/fdfs_data/data/'
        print
        print '.......... start remove files ..........'
        print
        i = 0
        for result in results:
            i += 1

            jpg_url = result[0]
            file_to_remove = jpg_url[jpg_url.find('/group1/M00/') + 12 :]
            print str(i).rjust(10), ' jpg :',  file_to_remove
            remove(target_dir, file_to_remove)

            jpeg_url = result[1]
            file_to_remove = jpeg_url[jpeg_url.find('/group1/M00/') + 12 :]
            print str(i).rjust(10), ' jpeg:',  file_to_remove
            remove(target_dir, file_to_remove)

            dcm_url = result[2]
            file_to_remove = dcm_url[dcm_url.find('/group1/M00/') + 12 :]
            print str(i).rjust(10), ' dcm :',  file_to_remove
            remove(target_dir, file_to_remove)
        print
        print '.......... end remove files ..........'
        print
    else:
        print 'Results : no'
    return

if __name__ == '__main__':
    if len(REMOVE_STUDY_LIST) > 0:
        for study in REMOVE_STUDY_LIST:
            print
            print 'Remove hospital_id : ', study['hospital_id'], ', study_id : ', study['study_id']
            print
            removefromfdfs(study['hospital_id'], study['study_id'])
            removefromdb(study['hospital_id'], study['study_id'])
    else:
        print 'No study in config to remove. Please input study list in remove_config.py ...'

    """
    files_to_remove = [
        '00/00/wKgBzVqXcg2AKIO-AAKZ8ONXUBo152.jpg',
        '00/00/wKgBzVqXchCAA5JqAAKZ8ONXUBo287.jpg',
        '00/00/wKgBzVqXcg-AZ1jAAAL3KHHX1I8460.jpg',
        '00/00/wKgBzVqXcg2AMOgIAB7jwOLmgJQ78.jpeg',
        '00/00/wKgBzVqXchCAfbh5AB7jwOHQc6g11.jpeg',
        '00/00/wKgBzVqXcg-ATs0pADXmvMTpd0c33.jpeg',
        '00/00/wKgBzVqXcg2AcOhJAPwjYhTxF_g309.dcm',
        '00/00/wKgBzVqXchCAU72UAPwjYinZf2Y567.dcm',
        '00/00/wKgBzVqXcg-AOqvEAPwjWG1j0SY987.dcm',
        '00/7D/wKgBzVqXo9iAd8hfAAflkfV2ZNo694.jpg',
        '00/7D/wKgBzVqXo9iAcI-BAFZJnLp7Nr037.jpeg',
        '00/7D/wKgBzVqXo9eAXPJhALPtPM3U_jA575.dcm'
    ]
    target_dir = '/data/fdfs_data/data/'
    #target_dir = '/home/huiying/Documents/ttt/'
    print
    print '.......... start remove files ..........'
    print

    i = 0 
    for file_to_remove in files_to_remove:
        i += 1
        print str(i).rjust(10), ':',  file_to_remove
        remove(target_dir, file_to_remove)

    print
    print '.......... end remove files ..........'
    """
