# -*- coding: utf-8 -*-


from difflib import SequenceMatcher
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import io, os


def convert_pdf_to_txt(path):
    
    rsrcmgr     = PDFResourceManager()
    retstr      = io.StringIO()
    laparams    = LAParams()
    device      = TextConverter(rsrcmgr, retstr, laparams=laparams)
    fp          = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    maxpages    = 0
    caching     = True
    pagenos     = set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages,
                                  caching=caching,
                                  check_extractable=True):
        interpreter.process_page(page)

    fp.close    ()
    device.close()
    text = retstr.getvalue()
    retstr.close()
    
    return text


def wordPositions(splitted):
    return {w: [i for i in range(len(splitted)) if splitted[i] == w]
                for w in set(splitted)}


def Get_files(folder,end_with = r'.pdf'):
    return [root + '\\' + file for root, dirs, files in os.walk(folder)\
                     for file in files if file.endswith(end_with)]


def similar(a,b):
    return SequenceMatcher(None, a, b).ratio()


def printer(message,True_false):
    if True_false:
        print (message)

def Find_Word_in_Pdfs(folder,search_Word,tolerance = 1,print_me = True):
    paths         = Get_files(folder)
    alread_exists = []
    words_exists  = []
    dict_out_put  = {}
    
    for path in paths:
        path_name = os.path.basename(path)
        try:
            if path_name not in alread_exists:
                printer(" # # # Working on: {} # # #".format(path_name),print_me)
                text      = convert_pdf_to_txt(path)
                splitted  = text.split()            
                values    = set([i  for i in splitted if similar(i.upper(),search_Word.upper()) > tolerance])  
                if len(values) > 0:
                    printer  (path,print_me)
                    printer  ("Found: {} ,matching words for: {}".format(str(len(values)),search_Word),print_me)
                    if len(values) > 1:
                        printer  ("searching words are: {}".format(str(values)),print_me)
                    dict_out_put[path] = []
                    alread_exists.append(path_name)
                    my_dict   = wordPositions(splitted)
                    for search in values:
                        value = my_dict.get(search, "")
                        printer  ("count: {}, word: {}".format(str(len(value)),search),print_me)
                        for i in value:
                            seq_text = ' '.join(splitted[i-5:i+5])
                            if seq_text not in words_exists:
                                words_exists.append(seq_text)
                                dict_out_put[path] += [seq_text]
                                printer(seq_text,print_me)
                else:
                    printer("No match words found",print_me)
                    pass
        except:
            print (" # # # Coudnt read: {} # # #".format(path_name) )
                
    del alread_exists
    del words_exists
    
    return dict_out_put


# # # # INPUTS # # # #
folder          = r'C:\Users\medad\Work\Project_argi\References'
search_Word     = "affected"
tolerance       = 0.90

# Main
dict_all_values = Find_Word_in_Pdfs(folder,search_Word,tolerance,print_me = True)



