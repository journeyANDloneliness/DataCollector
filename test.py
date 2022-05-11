import datetime

import re
from pymaybe import maybe
res=re.findall(r"(update\d+(?=:)): (.+)\n","""
	update1: asad
	update2: asadrtet

	""")
print(res)

print(res)
for v in res:
	print(v[0])

a="sadadad|sdd".split("|")
print(a)
rl=re.findall(r"(review\d+:)(.+)\n","""
	review1: 12
	review2: higgy
	review2: higgy

	""") or []
print(rl)
a=maybe(re.search(r"(?<=delete:).+\n","""
	delete: 

	""")).group(0) or ""
print("a"+a+"a")
print(datetime.datetime.now().strftime("%d-%m-%y;%H-%M-%S"))

y=1
if y:
	x=True
else:
	x=False
print(x)