"""
Created on Wed Feb 20 08:07:03 2013

@author: nick
"""
import urllib
import re
import nltk
from bs4 import BeautifulSoup
from urllib2 import urlopen
import datetime, time
from time import  strftime

today = datetime.date.today()
todayd = today.strftime('%m/%d/%y')
todaylong = strftime('%Y-%m-%d %H:%M:%S +0000')
print todayd, todaylong


safetymaster = ''
bibmaster = ''

def nl():
    return '\n'
def t():
    return '\t'

def cleanstr(string):
    """Remove whitespace, and extra spaces."""
    string = string.strip()
    string = " ".join(string.split())
    return string

def formatsafety(appearance, name, citekey, peyes, pskin, pcloth, presp, eyes, skin, ingestion, inhalation, feyes, fskin, fingestion, finhalation ):
    o='\subsection{'+name+'} \n'
    o += cleanstr(appearance) +'\cite{'+citekey+'}'+nl()
    o += '\subsubsection{Hazards}' + nl()
    o += eyes +'\\\\'+ nl() + skin +'\\\\'+ nl() + ingestion +'\\\\'+ nl() + inhalation +'\\\\'+ nl()
    o += '\subsubsection{First Aid}' + nl()
    o += feyes +'\\\\'+ nl() + fskin +'\\\\'+ nl() + fingestion +'\\\\'+ nl() + finhalation + '\\\\'+ nl()
    o += '\subsubsection{PPE}' + nl()
    o += peyes +'\\\\'+ nl() + pskin +'\\\\'+ nl() + pcloth +'\\\\'+ nl() + presp+'\\\\' + nl()
    return o

def gettextbetween(textin, beginning, end):
    split1 = textin.split(beginning)
    if len(split1) ==0:
        return 'error'

    split2 = split1[1].split(end)
    if len(split2)==0:
        return 'error'

    return split2[0]

def getmsds(lookfor):
    """Perform a search for lookfor msds."""
    #lookfor='potassium chromate'
    url = "http://hazard.com/msds/gn.cgi"

    query_args = { 'query':lookfor}
    encoded_args = urllib.urlencode(query_args)

    handle = urlopen(url, encoded_args).read()



    soup = BeautifulSoup(handle)

    #search for msds docs from Fisher.
    merp = soup.find_all('a', text=re.compile("Fisher"))
    if len(merp) ==0:
        print lookfor + ' Not Found'
        return

    #First item that matches our query
    resurl = merp[0].get('href')
    print 'URL= ', resurl
    msdsurl = merp[0].get('href')

    parsefisher(lookfor, msdsurl)

def makebib(lookfor, msdsurl, citekey):
    global todayd
    o= '@electronic{'+citekey+',' + nl()
    o += t() + 'Date-Added = {'+todaylong+'},'+ nl()
    o += t() + 'Date-Modified = {'+todaylong+'},'+ nl()
    o += t() +  'Lastchecked = {'+todayd+'},'+ nl()
    o += t() + 'Note = {Accessed '+todayd+'},'+ nl()
    o += t() + 'Title = {'+lookfor+'},'+ nl()
    o += t() + 'Url = {'+msdsurl+'}' + nl()
    o += t() + '}'+ nl()

    return o


def parsefisher(lookfor, msdsurl):
    """ Parse out the desired information from a fisher msds """
    global safetymaster, bibmaster
    msdshtml = urlopen(msdsurl).read()
    #print msdshtml

    msdssoup = BeautifulSoup(msdshtml)
    name = cleanstr(msdssoup.select("big center")[2].get_text())
    print name
    appearance = cleanstr(msdssoup.find_all(text=re.compile("Appearance*"))[0])
    print appearance

    #Get PPE
    temp = msdshtml.split("Personal Protective Equipment")[1].split("Section 9")[0]
    temp = nltk.clean_html(temp)

   # print temp, len(temp)
    if len(temp) !=0:
        peyes = 'PPE EYES: ' + cleanstr(temp.split('Eyes:')[1].split('Skin:')[0])
        pskin = 'PPE Skin: ' + cleanstr(temp.split('Skin:')[1].split('Clothing:')[0])
        pcloth = 'PPE Clothing: ' + cleanstr(temp.split('Clothing:')[1].split('Respirators:')[0])
        presp = 'PPE Resp: ' + cleanstr(temp.split('Respirators:')[1])
    else:
        peyes = 'PPE EYES: ' + 'not available'
        pskin = 'PPE Skin: ' + 'not available'
        pcloth = 'PPE Clothing: ' + 'not available'
        presp = 'PPE Resp: ' + 'not available'

    # Get Saftey
    temp = msdshtml.split("Health Effects")[1].split("Section 4 - First Aid Measures")[0]
    temp = nltk.clean_html(temp)
    if len(temp) !=0:
        #Now cut out the content we need - a bit messy, but the html isn't pretty so whatever...
        eyes = 'Eyes: '+ cleanstr(temp.split('Eye:')[1].split('Skin:')[0])
        skin = 'Skin: '+cleanstr(temp.split('Skin:')[1].split('Ingestion:')[0])
        ingestion = 'Ingestion: '+cleanstr(temp.split('Ingestion:')[1].split('Inhalation:')[0])
        inhalation = 'Inhalation: '+cleanstr(temp.split('Inhalation:')[1].split('Chronic:')[0])
    else:
        eyes = 'Eyes: ' + 'not available'
        skin = 'Skin: ' + 'not available'
        ingestion = 'Ingestion: ' + 'not available'
        inhalation = 'Inhalation: ' + 'not available'


    #Get First Aid
    temp = msdshtml.split("Section 4 - First Aid Measures")[1].split("Section 5 - Fire Fighting Measures")[0]
    temp = nltk.clean_html(temp)


    feyes = 'First aid Eyes: '+ cleanstr(temp.split('Eyes:')[1].split('Skin:')[0])
    fskin = 'First aid Skin: '+cleanstr(temp.split('Skin:')[1].split('Ingestion:')[0])
    fingestion = 'First aid Ingestion: '+cleanstr(temp.split('Ingestion:')[1].split('Inhalation:')[0])
    finhalation = 'First aid Inhalation: '+cleanstr(temp.split('Inhalation:')[1].split('Chronic:')[0])


    #make a citekey
    citekey = str(time.time()).replace('.','')

    #Format into safety section, add to safety master
    safetymaster += formatsafety(appearance, name, citekey, peyes, pskin, pcloth, presp, eyes, skin, ingestion, inhalation, feyes, fskin, fingestion, finhalation )

    #Format into a bibtex key, add to bib master
    bibmaster += makebib(lookfor, msdsurl, citekey)

#########Done###############
