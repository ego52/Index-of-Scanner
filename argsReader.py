#Libs
import argparse
#Files
import common

common.clear()
common.banner()

parser = argparse.ArgumentParser(
    prog='idxScanner.py',
    description='Scan index of pages')

parser.add_argument('-U', '--url', required=True)
parser.add_argument('-S', '--save', help="file to save information to", required=True)
parser.add_argument('-D', '--depth', default=3) 

args = parser.parse_args()