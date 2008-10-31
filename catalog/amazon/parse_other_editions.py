import os, re, sys
from BeautifulSoup import BeautifulSoup

re_link = re.compile('^http://www\.amazon\.com/(.*)/dp/(\d{9}[\dX]|B[A-Z0-9]+)$')

def read_bucket_table(f):
    html = ''
    bucket = False
    table = False
    for line in f:
        if line[:-1] == '<div class="bucket">':
            bucket = True
            continue
        if bucket and line[:-1] == '   <table border="0" cellpadding="2" cellspacing="0">':
            table = True
        if table:
            html += line
            if line[:-1] == '   </table>':
                break
    return html

def parse(f):
    html = read_bucket_table(f)
    if not html:
        return None
    soup = BeautifulSoup(html)
    for tr in soup('tr')[2:]:
        td = tr('td')
        assert len(td) == 3
        td0 = td[0]
        assert td0['class'] == 'small'
        assert len(td0) == 3
        (nl, link, desc) = td0
        assert nl == '\n'
        href = link['href']
        if href.startswith("http://www.amazon.com:80/gp/redirect.html"):
            # audio book
            continue
        m = re_link.match(link['href'])
        if not m:
            print link['href']
        print `m.groups(), desc.strip()`
    print

for filename in os.listdir(sys.argv[1]):
    if not filename[0].isdigit():
        continue
    f = open(filename)
    print filename
    parse(f)
    f.close()