# Scan JSP files for custom/JSTL tags whose attribute parsing would fail like Jasper ("= expected" / unterminated)
import os
import re
import sys

if len(sys.argv) < 2:
    print("Usage: python jsp_tag_attr_check.py <target_dir>", file=sys.stderr)
    sys.exit(2)

root = sys.argv[1]
PFX = r'(?:c|fmt|fn|spring|form|tiles|jsp|x|sec|ui|tags|t|egov|tag)'
open_re = re.compile(r'<(' + PFX + r'):([\w-]+)')


def scan(s):
    errs = []
    for m in open_re.finditer(s):
        i = m.end()
        n = len(s)
        while True:
            while i < n and s[i] in ' \t\r\n':
                i += 1
            if i >= n:
                errs.append((m.start(), 'eof'))
                break
            if s.startswith('/>', i) or s[i] == '>':
                break
            a = re.match(r'[\w:.-]+', s[i:])
            if not a:
                errs.append((i, 'bad char %r' % s[i]))
                break
            i += a.end()
            while i < n and s[i] in ' \t\r\n':
                i += 1
            if i >= n or s[i] != '=':
                errs.append((i, '= expected'))
                break
            i += 1
            while i < n and s[i] in ' \t\r\n':
                i += 1
            q = s[i] if i < n else ''
            if q not in '"\'':
                errs.append((i, 'quote expected'))
                break
            i += 1
            # read until matching quote, skipping ${...}, #{...}, and <%= %>
            ok = False
            while i < n:
                if s.startswith('${', i) or s.startswith('#{', i):
                    j = s.find('}', i)
                    i = j + 1 if j > 0 else n
                    continue
                if s.startswith('<%=', i):
                    j = s.find('%>', i)
                    i = j + 2 if j > 0 else n
                    continue
                if s[i] == chr(92):
                    i += 2
                    continue
                if s[i] == q:
                    i += 1
                    ok = True
                    break
                i += 1
            if not ok:
                errs.append((i, 'unterminated'))
                break
    return errs


hits = 0
for dp, dn, fn in os.walk(root):
    for f in fn:
        if not (f.endswith('.jsp') or f.endswith('.tag') or f.endswith('.jspf')):
            continue
        p = os.path.join(dp, f)
        with open(p, encoding='utf-8', errors='ignore') as fp:
            s = fp.read()
        # strip JSP comments
        s2 = re.sub(r'<%--.*?--%>', lambda m: ' ' * len(m.group(0)), s, flags=re.S)
        for pos, why in scan(s2):
            line = s2.count('\n', 0, pos) + 1
            col = pos - s2.rfind('\n', 0, pos)
            print(f"{os.path.relpath(p, root).replace(os.sep, '/')}:{line}:{col}: {why}")
            hits += 1
print('hits', hits, file=sys.stderr)
