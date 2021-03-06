"""helper program for Rst2HTML tests: interpreting differences
"""
from bs4 import BeautifulSoup
from test_dml import list_site_contents
sitename = 'testsite'


class Comparer:
    """Methods and state for comparing data between subsequent tests
    """
    def __init__(self):
        self.namelist = []
        self.dbdatalist = []
        self.htmldatalist = []

    def analyze_db_data(self, name):
        "convert text dump to datastructure"
        # let's use the original stuff instead


    def get_db_diff(self, old, new, olddata, newdata):
        """compare site data dumps
        """
        result = []
        # because we never remove stuff, we can concentrate on what's new
        oldsite, olddocs = olddata
        newsite, newdocs = newdata
        if newsite == oldsite:
            result.append('site data has not changed')
            return result
        if newdocs == olddocs:
            result.append('site docs have not changed')
        ## print(newsite, oldsite)
        ## print(olddocs, newdocs)
        if oldsite == {}:
            result.append('new site has been added')
            return result
        for setting in newsite['settings']:
            if setting not in oldsite['settings']:
                result.append('new setting: {} {}'.format(setting, newsite['settings']))
                continue
            if newsite['settings'] != oldsite['settings']:
                result.append('setting {} changed from {} to {}'.format(
                    setting, oldsite['settings'], newsite['settings']))
        for subdir in list(newsite['docs']):
            if subdir not in oldsite['docs']:
                result.append('new subdir: {}'.format(subdir))
                continue
            olddir = oldsite['docs'][subdir]
            for doc in newsite['docs'][subdir]:
                if doc not in olddir:
                    result.append('new doc in subdir {}: {}'.format(subdir, doc))
                    continue
                olddoc = olddir[doc]
                for doctype in newsite['docs'][subdir][doc]:
                    if doctype not in olddoc:
                        result.append('new doctype for doc {} in {}: {}'.format(
                            doc, subdir, doctype))
                    else:
                        test = newsite['docs'][subdir][doc][doctype]['updated']
                        if test != olddoc[doctype]['updated']:
                            if doctype != 'mirror':
                                result.append('{} {} {} was changed'.format(
                                    subdir, doc, doctype))
                            else:
                                result.append('{} {} was copied to mirror (again)'
                                              ''.format(subdir, doc))
        # document ids are sorted, but not necessarily in creation order
        oldids = [x['_id'] for x in olddocs]
        newids = [x['_id'] for x in newdocs]
        allids = set(oldids + newids)
        for _id in allids:
            if _id in oldids and _id not in newids:
                result.append('doc {} is removed'.format(_id))
            elif _id in newids and _id not in oldids:
                result.append('doc {} is new'.format(_id))
            else:
                for doc in olddocs:
                    if doc['_id'] == _id:
                        olddoc = doc
                        break
                for doc in newdocs:
                    if doc['_id'] == _id:
                        newdoc = doc
                        break
                if (newdoc['current'] != olddoc['current'] or
                        newdoc['previous'] != olddoc['previous']):
                    result.append('doc {} is changed'.format(_id))
                    ## result.append('doc {} is changed'.format(doc['_id']))
        ## for ix, newdoc in enumerate(newdocs):
            ## if ix < len(olddocs):
                ## if (doc['current'] != olddocs[ix]['current'] or
                        ## doc['previous'] != olddocs[ix]['previous']):
                    ## result.append('doc {} is changed'.format(doc['_id']))
            ## else:
                ## result.append('doc {} is new'.format(doc['_id']))
        return result


    def analyze_html_data(self, name):
        "convert HTML to datastructure"
        result = {}
        with open(name) as _in:
            # try:
            soup = BeautifulSoup(_in, 'lxml')
            # except ???:
            # soup = BeautifulSoup(_in)
        for btn in soup.find_all('button'):
            test = btn.parent
            if (''.join(x for x in btn.stripped_strings) == 'Back to editor' and
                    test.name == 'a' and
                    'href' in test.attrs and
                    (test['href'].startswith('loadrst?rstfile=') or
                     test['href'].startswith('loadhtml?htmlfile=') or
                     test['href'].startswith('/loadconf?settings='))):
                return
        for selector in soup.find_all('select'):
            options = []
            selected = ''
            for option in selector.find_all('option'):
                options.append(option.string)
                if 'selected' in option.attrs:
                    selected = option.string
            result[selector["name"] + '_list'] = options
            result[selector["name"] + '_name'] = selected
        for inp in soup.find_all('input'):
            if inp.get("name", '') == 'newfile':
                result["newfile_name"] = inp["value"]
                break
        else:
            result['newfile_name'] = ''
        result["mld_text"] = soup.find('strong').string
        result["textdata"] = soup.find('textarea').string or ''
        return result


    def get_html_diff(self, old, new, olddata, newdata):
        "compare html output"
        diff = []
        ## olddata = analyze_html_data('/tmp/{}.html'.format(old))
        ## newdata = analyze_html_data('/tmp/{}.html'.format(new))
        for key in olddata:
            if olddata[key] != newdata[key]:
                if key.endswith('_list'):
                    for value in olddata[key]:
                        if value not in newdata[key]:
                            diff.append('{}: removed value "{}"'.format(key, value))
                    for value in newdata[key]:
                        if value not in olddata[key]:
                            diff.append('{}: added value "{}"'.format(key, value))
                elif key == 'textdata':
                    if newdata[key]:
                        diff.append('{} changed'.format(key))
                    else:
                        diff.append('{} cleared'.format(key))
                elif key == 'mld_text':
                    diff.append('{} is "{}"'.format(key, newdata[key]))
                else:
                    diff.append('{}: value was "{}", is now "{}"'.format(
                        key, olddata[key], newdata[key]))
        return diff


    def dump_data_and_compare(self, data, name):
        """main processing"""
        print("---- {} ----".format(name))
        fname = '/tmp/{}.html'.format(name)
        with open(fname, 'w') as _out:
            _out.write(data)
        htmldata = self.analyze_html_data(fname)

        fname = '/tmp/db_{}'.format(name)
        db_data = list_site_contents(sitename, fname)

        if self.namelist:
            old, new = self.namelist[-1], name

            # print('in dump_data_and_compare: getting db diff')
            # print('old =', old)
            # print('new =', new)
            # print('db_data old =', self.dbdatalist[-1])
            # print('db_data new =', db_data)
            dbresult = self.get_db_diff(old, new, self.dbdatalist[-1], db_data)

            if htmldata:
                cmpold, cmpnew = self.htmldatalist[-1], htmldata
            else:
                cmpold, cmpnew = self.htmldatalist[-2:]
            htmlresult = sorted(self.get_html_diff(old, new, cmpold, cmpnew))
            ## htmlresult = []
            ## for hname, olddata, newdata in get_html_diff(old, new, cmpold, cmpnew):
                ## print('difference in {}'.format(hname), end='')
                ## if hname == 'textdata':
                    ## print()
                ## else:
                    ## print(':')
                    ## print('  {}: {}'.format(old, olddata))
                    ## print('  {}: {}'.format(new, newdata))
                ## htmlresult.append((hname, old, olddata, new, newdata))
        else:
            dbresult = db_data  # {}
            htmlresult = htmldata  # []
        self.namelist.append(name)
        self.dbdatalist.append(db_data)
        if htmldata:
            self.htmldatalist.append(htmldata)
        return dbresult, htmlresult
