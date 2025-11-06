import zipfile
from urllib.request import urlretrieve
import os

def unzip(path: str, outpath: str|bool = False):
    """Unzip/extract csv files"""
    with zipfile.ZipFile(path) as archive:
        
        # Print info
        print("Archive contents: \n")
        archive.printdir()
        
        # Get conf
        conf = input("Continue with extraction? Y/n: ")

        if outpath:
            if conf in ['Y', 'y']:
                archive.extractall(outpath)
        elif not outpath:
            archive.extractall()
        else:
            print("Invalid input.")


def download(url: str, outpath: str):
    """Download from url"""
    urlretrieve(url, outpath)


def cleanup(path: str):
    """Delete zip file"""
    os.rmdir(path)
