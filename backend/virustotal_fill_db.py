import os

from util.dbg import dbg
from .virustotal import Virustotal
from sampledb import Sampledb

vt  = Virustotal()
sdb = Sampledb()

# Engines on vt providing good results
engines = ["DrWeb", "Kaspersky", "ESET-NOD32"]

def getName(r):
	if r["scans"]:
		for e in engines:
			if r["scans"][e] and r["scans"][e]["detected"]:
				return r["scans"][e]["result"]
		for e,x in r["scans"].items():
			if x["detected"]:
				return x["result"]
		return None
	else:
		return None

#sdb.sql.execute('ALTER TABLE samples ADD COLUMN result TEXT')
#sdb.sql.commit()
for row in sdb.sql.execute('SELECT id, sha256 FROM samples WHERE result is NULL'):
	r   = vt.query_hash_sha256(row[1])
	res = str(getName(r))
	print((row[1] + ": " + res))
	sdb.sql.execute('UPDATE samples SET result = ? WHERE id = ?', (res, row[0]))
	sdb.sql.commit()

