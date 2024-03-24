import json

with open('annual_report.json','r',encoding='UTF-8') as f:
    data = json.load(f)

#print 所有类型
typelist = []
keys = ['title','unit','header','key_index','values']

titlemark = ['%d)'%i for i in range(10)]
titlemark += ['%d.'%i for i in range(10)]
titlemark += ['一、','二、','三、','四、','五、','六、','七、','八、','九、','十、']


unitmark = '单位'

# def del(txt,str):
#     if '\n' in txt:
#         txtlist = txt.split('\n')
#         tmp = ''
#         for i in range(len(txtlist)):
#             tmp = tmp + txtlist[i]
#         return tmp
#     else:
#         return txt

def replace(txt):
    txt = txt.replace(',','')
    txt = txt.replace('.','')
    return txt
def istitle(txt):
    j = 0
    for mark in titlemark:
        if mark in txt:
            j += 1
    if j == 1:
        return True
    else:
        return False

def isunit(txt):
    if unitmark in txt:
        return True
    else:
        return False

def isspread(page):
    nexttable_id = table_id(page+1)
    firsttable = tablelist[nexttable_id[0]]
    for cell in firsttable:
        if cell['start_row'] == 0 and replace(cell['text']).isdigit():
            return True
    return False




# def table_id(page_i):
#     page = '%03d.png' % (page_i)
#     pagedata = data[page][0]
#
#     result = pagedata['result']
#     tablelist = result['tables']
#     table_id = []
#     for table_i in range(len(tablelist)):
#         if tablelist[table_i]['type'] == 'table_with_line':
#             table_id.append(table_i)
#     return table_id
#
# def getfirsttable(page_i):
#     page = '%03d.png' % (page_i)
#     pagedata = data[page][0]
#
#     result = pagedata['result']
#     tablelist = result['tables']
#     firstid = table_id(page_i)[0]
#     return tablelist[firstid]
class page():

    def __init__(self, page_id):
        self.page_id = page_id

    def table_all_list(self):
        pagestr = '%03d.png' % (self.page_id)
        pagedata = data[pagestr][0]
        result = pagedata['result']
        return result['tables']

    def table_id(self):
        table_id = []
        for table_i in range(len(self.table_all_list())):
            if self.table_all_list()[table_i]['type'] == 'table_with_line':
                table_id.append(table_i)
        return table_id

    def tablelist(self):
        return [self.table_all_list()[i] for i in self.table_id() ]

    def getfirsttable(self):
        if self.table_id() == []:
            print('%d have no tables.'%self.page_id)
            return None
        return self.table_all_list()[self.table_id()[0]]

    def getlasttable_id(self):
        return self.table_id()[-1]

    def isspread(self):
        nextpage = page(self.page_id + 1)
        firsttable = nextpage.getfirsttable()
        if firsttable == None:
            return False
        for cell in firsttable['table_cells']:
            if cell['start_row'] == 0 and replace(cell['text']).isdigit():
                return True
        return False

def biaoge(page_id):
    firstpage = page(page_id)

    if firstpage.isspread():
        last_table_id = firstpage.getlasttable_id()

    for i in range(len(firstpage.table_all_list())-1):

        if firstpage.isspread():
            if i + 1 == last_table_id:
                dic = dict.fromkeys(keys, None)
                header = []
                key_index = []
                values = []

                lineslist = firstpage.table_all_list()[i]['lines']

                for line in lineslist:
                    text = line['text'].replace('\n','')
                    if istitle(text):
                        dic['title'] = text
                    elif isunit(text):
                        dic['unit'] = text

                for cell in firstpage.table_all_list()[i + 1]['table_cells']:
                    txt = cell['text'].replace('\n', '')
                    if cell['start_row'] == 0:
                        header.append(txt)
                    elif cell['start_col'] == 0:
                        key_index.append(txt)
                    else:
                        values.append(txt)

                nextpage = page(page_id+1)
                firsttable = nextpage.getfirsttable()
                for cell in firsttable['table_cells']:
                    txt = cell['text'].replace('\n', '')
                    if cell['start_col'] == 0:
                        key_index.append(txt)
                    else:
                        values.append(txt)

                dic['header'] = header
                dic['key_index'] = key_index
                dic['values'] = values
                print(dic)

            elif firstpage.table_all_list()[i + 1]['type'] == 'table_with_line':

                dic = dict.fromkeys(keys, None)
                header = []
                key_index = []
                values = []

                lineslist = firstpage.table_all_list()[i]['lines']

                for line in lineslist:
                    text = line['text'].replace('\n','')
                    if istitle(text):
                        dic['title'] = text
                    elif isunit(text):
                        dic['unit'] = text

                for cell in firstpage.table_all_list()[i + 1]['table_cells']:
                    txt = cell['text'].replace('\n', '')
                    if cell['start_row'] == 0:
                        header.append(txt)
                    elif cell['start_col'] == 0:
                        key_index.append(txt)
                    else:
                        values.append(txt)

                dic['header'] = header
                dic['key_index'] = key_index
                dic['values'] = values
                print(dic)

        else:
            if firstpage.table_all_list()[i + 1]['type'] == 'table_with_line':

                dic = dict.fromkeys(keys, None)
                header = []
                key_index = []
                values = []

                lineslist = firstpage.table_all_list()[i]['lines']

                for line in lineslist:
                    text = line['text'].replace('\n','')
                    if istitle(text):
                        dic['title'] = text
                    elif isunit(text):
                        dic['unit'] = text

                for cell in firstpage.table_all_list()[i + 1]['table_cells']:
                    txt = cell['text'].replace('\n', '')
                    if cell['start_row'] == 0:
                        header.append(txt)
                    elif cell['start_col'] == 0:
                        key_index.append(txt)
                    else:
                        values.append(txt)

                dic['header'] = header
                dic['key_index'] = key_index
                dic['values'] = values
                print(dic)


if __name__ == '__main__':
    biaoge(33)
