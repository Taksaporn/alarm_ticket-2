#!/usr/bin/python -u

import urllib
import httplib2
import collections
import re
import json
import AdvancedHTMLParser
import time
import datetime

httplib2.debuglevel = 0


class TTS_Path(object):
    login = "/sm/ess.do"
    preload = "/sm/loginPreload.jsp"
    search = "/sm/detail.do"


class TTS(object):
    login_state = False
    cookie = None
    username = ''
    password = ''
    headers = {}
    host = ''
    csrfValue = None
    csrfName = None

    def __init__(self, username=None, password=None, hostip="127.0.0.1", cookie=None):
        self.host = hostip
        self.username = username
        self.password = password
        self.cookie = collections.OrderedDict()
        self.cookie['JSESSIONID'] = ''
        self.cookie['mode'] = 'ess.do'
        self.cookie['lang'] = 'en'
        self.cookie['BIGipServerHP_SM_WEB01_POOL'] = '1476634816.36895.0000'

        if cookie:
            self.cookie['JSESSIONID'] = cookie
            self.login_state = True
            self.SetCookieHeader()

    def Auth(self):
        if not self.login_state:
            self.Login()
        self.GetCSRF()

    def FirstPage(self):
        self.Auth()
        path = TTS_Path.login
        resp = self.SendData(path)
        self.DebugPrint(resp[0])
        self.DebugPrint(resp[1])

    def Get_TicketInfo(self, ticketNo):
        self.Auth()
        data = collections.OrderedDict()
        url = '/sm/cwc/nav.menu?name=navStart&id=ROOT%2FSearch%20Ticket&{0}={1}'.format(
            self.csrfName, self.csrfValue)
        resp = self.SendData(url)
        self.DebugPrint(resp[0])
        m = re.search('thread=([0-9]+)', resp[0]['content-location'])

        if m:
            threadid = m.group(1)
        resp = self.SendData('{0}?thread={3}&{1}={2}'.format(TTS_Path.search, self.csrfName, self.csrfValue, threadid),
                             save_referer=True)
        self.DebugPrint(resp[0])
        self.DebugPrint(resp[1])
        data["row"] = ""
        data["__x"] = ""
        data["thread"] = threadid
        data["resetnotebook"] = ""
        data["event"] = "10"
        data["transaction"] = "0"
        data["type"] = "detail"
        data["focus"] = "instance%2Fcatid"
        data["focusContents"] = ticketNo
        data["focusId"] = "X16"
        data["focusReadOnly"] = "FALSE"
        data["start"] = ""
        data["count"] = ""
        data["more"] = ""
        data["tablename"] = ""
        data["window"] = ""
        data["close"] = ""
        data["_blankFields"] = ""
        data["_uncheckedBoxes"] = ""
        data["_tpzEventSource"] = ""
        data["formchanged"] = ""
        data["formname"] = "FilterAdvFind"
        data[self.csrfName] = self.csrfValue
        data["_multiSelection"] = ""
        data["_multiSelection_tableId"] = ""
        data["_multiSelection_selectionField"] = ""
        data["clientWidth"] = "1595"
        data["var%2FL.tablename"] = "probsummary"
        data["var%2FL.view.name"] = ""
        data["instance%2Fincident.id"] = ticketNo
        data["instance%2Foss.source"] = ""
        data["instance%2Fcatid"] = ""
        data["instance%2Foss.destination"] = ""
        data["instance%2Fnumber"] = ""
        data["instance%2Foss.contact.telephone"] = ""
        data["instance%2Fproblem.status"] = ""
        data["instance%2Fcarrier.name"] = ""
        data["instance%2Fstatus"] = ""
        data["instance%2Fcarrier.ticket"] = ""
        data["instance%2Fcontact.name"] = ""
        data["instance%2Fowner.group"] = ""
        data["instance%2Faffected.item"] = ""
        data["instance%2Fassignment"] = ""
        data["instance%2Flogical.name"] = ""
        data["instance%2Frepairteam"] = ""
        data["instance%2Fendtoend.group"] = ""
        data["var%2Fdown.time.start"] = ""
        data["var%2Fdown.time.end"] = ""
        data["instance%2Fcategory"] = ""
        data["var%2Fdown.end.start"] = ""
        data["var%2Fdown.end.end"] = ""
        data["instance%2Fsubcategory"] = ""
        data["var%2Fnext.breach.start"] = ""
        data["var%2Fnext.breach.end"] = ""
        data["instance%2Fproduct.type"] = ""
        data["var%2Fadv.open.start"] = ""
        data["var%2Fadv.open.end"] = ""
        data["instance%2Finitial.impact"] = ""
        data["instance%2Fopened.by"] = ""
        data["instance%2Fseverity"] = ""
        data["instance%2Fpriority.code"] = ""
        data["var%2Fpmc.update.start"] = ""
        data["var%2Fpmc.update.end"] = ""
        data["instance%2Fupdated.by"] = ""
        data["var%2Fchoices%2FdynamicFormDef"] = "%3Cform%3E%3Ccheckbox+id%3D%22open%22+label%3D%22Open%22%2F%3E%3Ccheckbox+id%3D%22closed%22+label%3D%22Closed%22%2F%3E%3Ccheckbox+id%3D%22assigned%22+label%3D%22Assigned+to+me%22%2F%3E%3Ccheckbox+id%3D%22highpriority%22+label%3D%22High+Priority%22%2F%3E%3Ccheckbox+id%3D%22tl%22+label%3D%22Total+Loss+of+Service%22%2F%3E%3Ccheckbox+id%3D%22ucmdb%22+label%3D%22Generated+by+UCMDB+Integration%22%2F%3E%3C%2Fform%3E"
        data["dynamicFormRef%2FF1373192486"] = "var%2Fchoices"
        data["var%2Fadv.close.start"] = ""
        data["var%2Fadv.close.end"] = ""
        data["instance%2Fclosed.by"] = ""
        data["instance%2Fresolution.code"] = ""
        data["instance%2Fdescription"] = ""
        data["instance%2Fcomments"] = ""
        data["instance%2Faction%2Faction"] = ""
        data["instance%2Fnotes"] = ""
        data["var%2Firspread"] = "4"
        data["var%2Fextend"] = "0"

        url = "/sm/L10N/recordlist.jsp"
        resp = self.SendData(url)
        self.DebugPrint(resp[0])
        self.DebugPrint(resp[1])
        resp = self.SendData(TTS_Path.search, data,
                             AutoParseHTMLCharector=False)
        url = '''/sm/list.do?thread={2}&{0}={1}'''.format(
            self.csrfName, self.csrfValue, threadid)
        resp = self.SendData(url)
        self.DebugPrint(resp[1])

        data = resp[1]

        lst_name = ['instance/oss.address/oss.address',
                    'instance/brief.description',
                    'instance/action/action']
        info = collections.OrderedDict()
        parser = AdvancedHTMLParser.AdvancedHTMLParser()
        parser.parseStr(data)

        for l in lst_name:
            infoname = parser.getElementsByName(str(l))
            infodvdvar = parser.getElementsByAttr('dvdvar', str(l))
            # if status closed get variable dvdvar or ref
            lem = str(infodvdvar).split('TagCollection([AdvancedTag(u\'')[1].split('\',')[0]
            if lem == 'textarea':
                # print infoname.all()[0].innerHTML.strip()
                info[l] = infodvdvar.all()[0].innerHTML.strip()
            elif lem == 'input':
                # print str(infoname).split('u\'value\', u\'')[1].split('\')')[0].encode('utf-8')
                info[l] = str(infodvdvar).split('u\'value\', u\'')[1].split('\')')[0].encode('utf-8')

        parserTableNormalRow = parser.getElementsByAttr('class', 'TableNormalRow')
        id_activity_table = str(parserTableNormalRow).split('dtlr_')[1].split('_')[0]
        row_count = len(str(parserTableNormalRow).split('dtlr_' + id_activity_table))

        # var/running/running[1]
        # var/datestamp/datestamp[1]
        # var/operator.name/operator.name[1]
        # var/division/division[1]
        # var/description/description[1]
        # var/type/type[1]
        datas = []
        for x in range(1, row_count + 1):
            id = 'dtlr_' + id_activity_table + '_' + str(x)
            tr = parser.getElementById(id)
            span_timestamp = tr[1].getElementsByName('var/datestamp/datestamp[' + str(x) + ']')[0]
            span_operator = tr[2].getElementsByName('var/operator.name/operator.name[' + str(x) + ']')[0]
            span_division = tr[3].getElementsByName('var/division/division[' + str(x) + ']')[0]
            span_description = tr[4].getElementsByName('var/description/description[' + str(x) + ']')[0]
            span_type = tr[5].getElementsByName('var/type/type[' + str(x) + ']')[0]

            data = collections.OrderedDict()
            data['number'] = x
            data['datestamp'] = span_timestamp.innerHTML.strip()
            data['operator'] = span_operator.innerHTML.strip()
            data['division'] = span_division.innerHTML.strip()
            data['description'] = span_description.innerHTML.strip()
            data['type'] = span_type.innerHTML.strip()
            datas.append(data)
        info['activity_table'] = datas
        return info

    def startdowntime(self, timerange):
        datetimemk = "01/01/2018 00:00:00"
        str_date = timerange[-1]
        a_month = 2629746 # sec
        a_yaer = 31556952 # sec

        datetimenow = datetime.datetime.now()
        time_left = timerange[1:-1]
        if str_date == 'y':
            timemk = time.mktime(datetimenow.timetuple()) - (a_yaer * int(time_left))
            datetimemk = datetime.datetime.fromtimestamp(timemk).strftime('%d/%m/%Y %H:%M:%S')
        else:
            timemk = time.mktime(datetimenow.timetuple()) - (a_month * int(time_left))
            datetimemk = datetime.datetime.fromtimestamp(timemk).strftime('%d/%m/%Y %H:%M:%S')
        return datetimemk

    def Search(self, id, timerange="-6m"):
        self.Auth()
        data = collections.OrderedDict()
        url = '/sm/cwc/nav.menu?name=navStart&id=ROOT%2FSearch%20Ticket&{0}={1}'.format(
            self.csrfName, self.csrfValue)
        resp = self.SendData(url)
        self.DebugPrint(resp[0])
        self.DebugPrint(resp[1])
        if 'content-location' not in resp[0]:
            self.login_state = False
            self.Auth()
            data = collections.OrderedDict()
            url = '/sm/cwc/nav.menu?name=navStart&id=ROOT%2FSearch%20Ticket&{0}={1}'.format(
                self.csrfName, self.csrfValue)
            resp = self.SendData(url)
            self.DebugPrint(resp[0])
            self.DebugPrint(resp[1])
            m = re.search('thread=([0-9]+)', resp[0]['content-location'])
        else:
            m = re.search('thread=([0-9]+)', resp[0]['content-location'])
        if m:
            threadid = m.group(1)

        resp = self.SendData('{0}?thread={3}&{1}={2}'.format(TTS_Path.search, self.csrfName, self.csrfValue, threadid),
                             save_referer=True)
        self.DebugPrint(resp[0])
        self.DebugPrint(resp[1])

        data["row"] = ""
        data["__x"] = ""
        data["thread"] = threadid
        data["resetnotebook"] = ""
        data["event"] = "10"
        data["transaction"] = "0"
        data["type"] = "detail"
        data["focus"] = "instance%2Fcatid"
        data["focusContents"] = id
        data["focusId"] = "X16"
        data["focusReadOnly"] = "FALSE"
        data["start"] = ""
        data["count"] = ""
        data["more"] = ""
        data["tablename"] = ""
        data["window"] = ""
        data["close"] = ""
        data["_blankFields"] = ""
        data["_uncheckedBoxes"] = ""
        data["_tpzEventSource"] = ""
        data["formchanged"] = ""
        data["formname"] = "FilterAdvFind"
        data[self.csrfName] = self.csrfValue
        data["_multiSelection"] = ""
        data["_multiSelection_tableId"] = ""
        data["_multiSelection_selectionField"] = ""
        data["clientWidth"] = "1595"
        data["var%2FL.tablename"] = "probsummary"
        data["var%2FL.view.name"] = ""
        data["instance%2Fincident.id"] = ""
        data["instance%2Foss.source"] = ""
        data["instance%2Fcatid"] = id
        data["instance%2Foss.destination"] = ""
        data["instance%2Fnumber"] = ""
        data["instance%2Foss.contact.telephone"] = ""
        data["instance%2Fproblem.status"] = ""
        data["instance%2Fcarrier.name"] = ""
        data["instance%2Fstatus"] = ""
        data["instance%2Fcarrier.ticket"] = ""
        data["instance%2Fcontact.name"] = ""
        data["instance%2Fowner.group"] = ""
        data["instance%2Faffected.item"] = ""
        data["instance%2Fassignment"] = ""
        data["instance%2Flogical.name"] = ""
        data["instance%2Frepairteam"] = ""
        data["instance%2Fendtoend.group"] = ""
        data["var%2Fdown.time.start"] = self.startdowntime(timerange)
        data["var%2Fdown.time.end"] = ""
        data["instance%2Fcategory"] = ""
        data["var%2Fdown.end.start"] = ""
        data["var%2Fdown.end.end"] = ""
        data["instance%2Fsubcategory"] = ""
        data["var%2Fnext.breach.start"] = ""
        data["var%2Fnext.breach.end"] = ""
        data["instance%2Fproduct.type"] = ""
        data["var%2Fadv.open.start"] = ""
        data["var%2Fadv.open.end"] = ""
        data["instance%2Finitial.impact"] = ""
        data["instance%2Fopened.by"] = ""
        data["instance%2Fseverity"] = ""
        data["instance%2Fpriority.code"] = ""
        data["var%2Fpmc.update.start"] = ""
        data["var%2Fpmc.update.end"] = ""
        data["instance%2Fupdated.by"] = ""
        data["var%2Fchoices%2FdynamicFormDef"] = "%3Cform%3E%3Ccheckbox+id%3D%22open%22+label%3D%22Open%22%2F%3E%3Ccheckbox+id%3D%22closed%22+label%3D%22Closed%22%2F%3E%3Ccheckbox+id%3D%22assigned%22+label%3D%22Assigned+to+me%22%2F%3E%3Ccheckbox+id%3D%22highpriority%22+label%3D%22High+Priority%22%2F%3E%3Ccheckbox+id%3D%22tl%22+label%3D%22Total+Loss+of+Service%22%2F%3E%3Ccheckbox+id%3D%22ucmdb%22+label%3D%22Generated+by+UCMDB+Integration%22%2F%3E%3C%2Fform%3E"
        data["dynamicFormRef%2FF1373192486"] = "var%2Fchoices"
        data["var%2Fadv.close.start"] = ""
        data["var%2Fadv.close.end"] = ""
        data["instance%2Fclosed.by"] = ""
        data["instance%2Fresolution.code"] = ""
        data["instance%2Fdescription"] = ""
        data["instance%2Fcomments"] = ""
        data["instance%2Faction%2Faction"] = ""
        data["instance%2Fnotes"] = ""
        data["var%2Firspread"] = "4"
        data["var%2Fextend"] = "0"

        url = "/sm/L10N/recordlist.jsp"
        resp = self.SendData(url)
        self.DebugPrint(resp[0])
        self.DebugPrint(resp[1])
        resp = self.SendData(TTS_Path.search, data,
                             AutoParseHTMLCharector=False)
        url = '''/sm/list.do?thread={2}&{0}={1}'''.format(
            self.csrfName, self.csrfValue, threadid)
        resp = self.SendData(url)

        '''
        key
        [u'status', u'incident_id', u'affected_item', u'___rowid', u'catid', u'downtime_start', u'number', u'___forecolor', u'___bold', u'problem_status', u'downtime', u'oss_source', u'oss_destination', u'___italic', u'owner_group', u'repairteam']
        '''
        data = resp[1]
        m = re.search('data:(.*)', data)

        lst = None
        if m:
            j = m.group(1)
            j = j.strip()[:-1]
            d = json.loads(j)
            lst = d['model']['instance']
        '''
        {u'status': u'closed', u'incident_id': u'SD030860', u'affected_item': u'\u0e1a\u0e23\u0e34\u0e01\u0e32\u0e23 CAT EPL - Domestic', u'___rowid': 0, u'catid': u'TBB145014', u'downtime_start': u'29/11/2015 13:50:40', u'number': u'IM030725', u'___forecolor': u'#000000', u'___bold': u'false', u'problem_status': u'Closed', u'downtime': u'01:34:55', u'oss_source': u'\u0e28\u0e17.\u0e19\u0e19\u0e17\u0e1a\u0e38\u0e23\u0e35 (\u0e42\u0e04\u0e23\u0e07\u0e01\u0e32\u0e23 IP Core 100G Over DWDM)_\u0e40\u0e21\u0e37\u0e2d\u0e07\u0e19\u0e19\u0e17\u0e1a\u0e38\u0e23\u0e35', u'oss_destination': u'\u0e2a\u0e04.\u0e19\u0e04\u0e23\u0e2a\u0e27\u0e23\u0e23\u0e04\u0e4c (\u0e42\u0e04\u0e23\u0e07\u0e01\u0e32\u0e23 IP Core 100G Over DWDM)_\u0e40\u0e21\u0e37\u0e2d\u0e07\u0e19\u0e04\u0e23\u0e2a\u0e27\u0e23\u0e23\u0e04\u0e4c', u'___italic': u'false', u'owner_group': u'\u0e21\u0e02. THAIPAK', u'repairteam': u'\u0e2a\u0e02.(\u0e01) \u0e2a\u0e04.\u0e2a\u0e34\u0e07\u0e2b\u0e4c\u0e1a\u0e38\u0e23\u0e35'}
        {u'status': u'closed', u'incident_id': u'SD043570', u'affected_item': u'\u0e1a\u0e23\u0e34\u0e01\u0e32\u0e23 CAT EPL - Domestic', u'___rowid': 1, u'catid': u'TBB145014', u'downtime_start': u'23/12/2015 17:16:39', u'number': u'IM043432', u'___forecolor': u'#000000', u'___bold': u'false', u'problem_status': u'Closed', u'downtime': u'02:29:44', u'oss_source': u'\u0e28\u0e17.\u0e19\u0e19\u0e17\u0e1a\u0e38\u0e23\u0e35 (\u0e42\u0e04\u0e23\u0e07\u0e01\u0e32\u0e23 IP Core 100G Over DWDM)_\u0e40\u0e21\u0e37\u0e2d\u0e07\u0e19\u0e19\u0e17\u0e1a\u0e38\u0e23\u0e35', u'oss_destination': u'\u0e2a\u0e04.\u0e19\u0e04\u0e23\u0e2a\u0e27\u0e23\u0e23\u0e04\u0e4c (\u0e42\u0e04\u0e23\u0e07\u0e01\u0e32\u0e23 IP Core 100G Over DWDM)_\u0e40\u0e21\u0e37\u0e2d\u0e07\u0e19\u0e04\u0e23\u0e2a\u0e27\u0e23\u0e23\u0e04\u0e4c', u'___italic': u'false', u'owner_group': u'\u0e21\u0e02. THAIPAK', u'repairteam': u'\u0e2a\u0e02.(\u0e01) \u0e2a\u0e04.\u0e2a\u0e34\u0e07\u0e2b\u0e4c\u0e1a\u0e38\u0e23\u0e35'}
        '''
        if isinstance(lst, list) and len(lst) != 0 and lst is not None:
            return lst[-1]

    def Login(self):
        data = collections.OrderedDict()
        data['user.id'] = self.username
        data['L.language'] = 'en'
        data['type'] = 'login'
        data['xHtoken'] = ''
        data['old.password'] = self.password
        data['event'] = '0'
        resp = self.SendData(TTS_Path.login, data, save_referer=True)
        self.GetCSRF()
        self.login_state = True
        self.DebugPrint(resp[0])
        self.DebugPrint(resp[1])

        print 'Loged In!!'

    def Logout(self):
        self.login_state = False

        resp = self.SendData('/sm/cwc/logoutcleanup.jsp', save_referer=True)
        resp = self.SendData('/sm/cwc/shortenSessionTimeout.jsp', save_referer=True)
        resp = self.SendData('/sm/goodbye.jsp', save_referer=True)
        self.DebugPrint(resp[0])
        self.DebugPrint(resp[1])

        print 'Loged out!!'

    def GetCSRF(self):
        if not self.csrfName:
            resp = self.SendData(TTS_Path.login, save_referer=True)
            if len(resp) > 1:
                m = re.search("cwc.csrfTokenName[ ]?=[ ]?'([^\']*)';", resp[1])
                if m:
                    self.csrfName = m.group(1)
                m = re.search(
                    "cwc.csrfTokenValue[ ]?=[ ]?'([^\']*)';", resp[1])
                if m:
                    self.csrfValue = m.group(1)
                self.DebugPrint("csrf {0}={1}".format(
                    self.csrfName, self.csrfValue))

    def SendData(self, path, data=None, save_referer=False, AutoParseHTMLCharector=True):
        self.DebugPrint('=' * 100)
        url = "http://{0}{1}".format(self.host, path)
        self.DebugPrint("url {2}\nrequest_path {0}\nheader{1}".format(
            path, str(self.headers), url))
        headers = self.headers
        if data:
            if AutoParseHTMLCharector:
                data = urllib.urlencode(data)
            else:
                datas = []
                for k in data.keys():
                    datas.append("{0}={1}".format(k, data[k]))
                data = '&'.join(datas)
            self.DebugPrint(data)
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
            resp = httplib2.Http().request(url, 'POST', headers=self.headers, body=data)
        else:
            resp = httplib2.Http().request(url, 'GET', headers=self.headers)
        if save_referer:
            self.headers['Referer'] = url
        if type(resp) == type(()):
            self.HeaderHandle(resp[0])
        return resp

    def HeaderHandle(self, response_header):
        if response_header.has_key('set-cookie'):
            cookie = response_header['set-cookie']
            self.DebugPrint("cookie : {0}".format(cookie))
            matchobj = re.search('JSESSIONID=([^\;]*)', cookie)
            if matchobj:
                self.cookie['JSESSIONID'] = matchobj.group(1)
            self.DebugPrint("cookie : {0}".format(self.cookie))
            self.SetCookieHeader()

    def SetCookieHeader(self):
        ncookies = []
        for k in self.cookie.keys():
            ncookies.append(" {0}={1}".format(k, self.cookie[k]))
        self.headers['Cookie'] = ';'.join(ncookies)

    def DebugPrint(self, msg):
        if False:
            print msg
