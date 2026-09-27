# -*- coding: utf-8 -*-
import re, io, os
p = r"D:\想法\sbti\cards\人物卡片.html"
s = io.open(p, encoding="utf-8").read()
uris = re.findall(r"data:image/[a-z]+;base64,", s)
names = re.findall(r'"name":\s*"([^"]+)"', s)
out = []
out.append("data-uri count = %d" % len(uris))
out.append("card names = " + ", ".join(names))
out.append("has __IMGS__ placeholder left = %s" % ("/*__IMGS__*/" in s))
out.append("has __DATA__ placeholder left = %s" % ("/*__DATA__*/" in s))
io.open(r"D:\想法\sbti\_check2.txt", "w", encoding="utf-8").write("\n".join(out))
print("\n".join(out))
