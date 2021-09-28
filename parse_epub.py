import ebooklib
import os
from ebooklib import epub
from bs4 import BeautifulSoup
import codecs
import re
os.chdir('C:\\Users\\apple\\Desktop')

def epub2thtml(epub_path):
    book = epub.read_epub(epub_path)
    chapters = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            chapters.append(item.get_content())
    return chapters

goodlist = ['indent', 'nonindent', 'bl_extract', 'bl_nonindent', 'bl_indent',
            'bl_nonindent1', 'bl_center', 'hanging2']

def chap2text(chap):
    output = ''
    soup = BeautifulSoup(chap, 'html.parser')
    text = soup.body
    #text.find_all('p')
    #list(soup.p.children)
    for t in text:
        if t == '\n':
            output += '&*&'
        elif t.name == 'div' and t['class'][0] == 'block':
            output = output[:-3]
            for i in t:
                if i == '\n':
                    output += i
                elif i.name == 'p' and i['class'][0] in goodlist:
                    lz = i.contents
                    output += ''.join([str(i) for i in lz])
        elif t.name =='p' and t['class'][0] in goodlist:
            lz = t.contents
            output += ''.join([str(i) for i in lz])
    output = output.split('&*&')
    output = [integr_foo(i) for i in output if i != '']
    output = '&*&'.join(output)
    output = output.replace('\n&*&', '&*&')
    output = output.replace('&*&\n', '&*&')
    return output

def integr_foo(string):
    tags = ['sup', 'a', 'br']
    for tag in tags:
        funk = makefoo(tag)
        string = funk(string)
    return string

def makefoo(tag):
    def foo(string):
        if tag == 'br':
            template = fr'<{tag}/>'
            kit = re.findall(template, string)
            for i in kit:
                string = string.replace(i, '\n')
        else:
            template = fr'<{tag}.*?<\/{tag}>'
            kit = re.findall(template, string)
            for i in kit:
                string = string.replace(i, '')
        return string
    return foo

def thtm(thtml):
    output = ''
    for html in thtml:
        text = chap2text(html)
        output += text + '\n'
    return output

def epub2text():
    chapters = epub2thtml('56.epub')
    ct = thtm(chapters[:-2])
    with codecs.open('tet.txt', 'w', 'utf-8') as f:
        f.write(ct)
    return ct

def writer():
    ch = epub2thtml()
    ct = chap2text(ch[11])
    with codecs.open('tet.txt', 'w', 'utf-8') as f:
        f.write(ct)
    return ct

