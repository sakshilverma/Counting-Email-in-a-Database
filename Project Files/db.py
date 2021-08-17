import sqlite3
con=sqlite3.connect('db.sqlite')
cur=con.cursor()

fname=input('Enter file name - ')
f=open(fname)

cur.execute('DROP TABLE IF EXISTS Counts')
cur.execute('CREATE TABLE Counts (org TEXT, count INTEGER)')

for line in f:
    if not line.startswith('From: '):
        continue
    s=line.strip()
    s=line.split()
    email=s[1]
    pos=email.find('@')
    domain=email[pos+1:]
    cur.execute('SELECT count FROM Counts WHERE org=?',(domain,))
    row=cur.fetchone()
    if row is None:
        cur.execute('INSERT INTO Counts (org, count) VALUES (?, 1)',(domain,))
    else:
        cur.execute('UPDATE Counts SET count=count+1 WHERE org=?',(domain,))
    con.commit()

display='SELECT org,count FROM Counts ORDER BY count DESC'

for row in cur.execute(display):
    print((row[0],row[1]))
cur.close()
