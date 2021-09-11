from settings.constants import *

import os
import ntpath
import xml.etree.ElementTree as ET

import codecs

from utils.aws import upload_to_aws


def split_and_upload(FILE_NAME, count_by_file):
    print(FILE_NAME)
    header = open(FILE_NAME, errors='ignore').readline()
    print(header)
    context = ET.iterparse(FILE_NAME, events=('start', 'end'), parser=ET.XMLParser(encoding='utf-8'))
    count = 0
    elements = []
    chunk = 0
    for event, elem in context:
        if elem.tag == 'SUBJECT' and event == 'start':
            # print(count)
            elements.append(elem)
            count += 1
            if count == count_by_file:
                chunk += 1
                filee = "%s__%s.xml" % (os.path.splitext(FILE_NAME)[0], chunk)
                with open(filee, 'wb') as f:
                    f.write(header.encode())
                    for i in elements:
                        # print(i, ET.tostring(i))
                        f.write(ET.tostring(i))
                count = 0
                print('uploading to aws ', chunk)
                upload_to_aws(filee, BUCKET_NAME, '%s/%s/%s' % (BUCKET_FOLDER, os.path.splitext(os.path.basename(FILE_NAME))[0], os.path.basename(filee)))
                os.remove(filee)
                elements.clear()