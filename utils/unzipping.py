import errno
import os
import shutil
import zipfile
import codecs

def convert_to_utf(path, file_name):
    f = codecs.open(os.path.join(path, file_name), 'r', 'cp1251')
    u = f.read()   # now the contents have been transformed to a Unicode string
    out = codecs.open(os.path.join(path, file_name), 'w', 'utf-8')
    out.write(u)   # and now the contents have been output as UTF-8

def convert_all_files_in_folder_to_utf(folder):
    for path, subdirs, files in os.walk(folder):
        for name in files:
            convert_to_utf(path, name)

def unzip(file, TARGETDIR):
    with open(file, "rb") as zipsrc:
        zfile = zipfile.ZipFile(zipsrc)
        for member in zfile.infolist():
           print(member)
           target_path = os.path.join(TARGETDIR, member.filename)
           if target_path.endswith('/'):  # folder entry, create
               try:
                   os.makedirs(target_path)
               except (OSError, IOError) as err:
                   # Windows may complain if the folders already exist
                   if err.errno != errno.EEXIST:
                       raise
               continue
           with open(target_path, 'wb') as outfile, zfile.open(member) as infile:
               shutil.copyfileobj(infile, outfile)

    convert_all_files_in_folder_to_utf(TARGETDIR)