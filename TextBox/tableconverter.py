import numpy

x = r"""
PU & 39.0 & 43.0 & 47.0 & 51.0 & 55.0 & 59.0 \\
\hline
Full path & 10.7813 $ \pm $1.4879 & 11.3816 $ \pm $1.5208 & 11.6901 $ \pm $1.2477 & 13.1872 $ \pm $1.8040 & 14.0358 $ \pm $1.5867 & 11.5998 $ \pm $0.7920 \\
Control path & 2.5085 $ \pm $0.0428 & 2.5961 $ \pm $0.0464 & 2.7127 $ \pm $0.0469 & 2.8010 $ \pm $0.0473 & 2.9393 $ \pm $0.0513 & 3.0623 $ \pm $0.0502 \\
"""

x = x.replace(r'\hline', '')
tableRows = x.split(r'\\')
table = None
for i, t in enumerate(tableRows):
 if t != '\n':
  if table is None:
   table = numpy.array(t.split('&'))
  else:
   table = numpy.vstack((table, numpy.array(t.split('&'))))

tableTrans = table.T.tolist()

tNew = ''
for row in tableTrans:
 for col in row:
  tNew += col.strip() + ' & '
 tNew = tNew[:-2] + r' \\' + '\n'
print tNew
