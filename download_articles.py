import urllib2
import lxml.html.soupparser
import os
import glob
import contextlib

def dl_source_from_arxiv(arxiv_id):
    arxiv = "http://arxiv.org"
    paper = urllib2.urlopen("%s/abs/%s"%(arxiv, arxiv_id)).read()
    paperpage = lxml.html.soupparser.fromstring(paper)
    fullpath = paperpage.xpath(".//a[text()='Other formats']/@href")[0]
    full = urllib2.urlopen("%s%s"%(arxiv, fullpath)).read()
    fullpage = lxml.html.soupparser.fromstring(full)
    sourcepath = fullpage.xpath(".//a[text()='Download source']/@href")[0]
    sourcefile = "%s%s"%(arxiv, sourcepath)
    return sourcefile

def extract_tex_from_arxiv(arxiv_id, tex_destination):
    path = arxiv_id
    os.mkdir(path)
    sourcefile = dl_source_from_arxiv(arxiv_id)
    with contextlib.closing(urllib2.urlopen("%s"%(sourcefile))) as fullarxiv:
        with open("%s/%s.tar.gzip"%(path, arxiv_id), "w") as f:
            f.write(fullarxiv.read())
    #Check the alternative of "tar" in Python, instead of using "os"
    os.system("cd %s; tar -xvf %s.tar.gzip"%(path, arxiv_id))
    texfile = glob.glob("%s/*.tex"%(path))[0]
    os.system("mv %s %s/%s.tex"%(texfile, tex_destination, arxiv_id))
    print "%s downloaded!"%(arxiv_id)

extract_tex_from_arxiv("1411.6628v2", "texs")
