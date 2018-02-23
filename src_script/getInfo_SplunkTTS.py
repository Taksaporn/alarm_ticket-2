#!/usr/bin/python -u
import time
from MySQL import Database
from tts_v1 import TTS
from splunk import SPLUNK

db = Database(host='127.0.0.1', username='root', password='', db='alarm_ticket')

#SPLUNK
splunk_baseurl = 'https://10.4.0.136:8089'
# splunk_baseurl = 'https://192.168.100.2:8089'
splunk = SPLUNK('admin', 'P@ssw0rd', splunk_baseurl)

#TTS
TTS_basehost = "122.155.137.214"
tts = TTS('catma', 'ait@1761', TTS_basehost)

def insert_Splunk(lst_splunk):
    for l in lst_splunk:
        splitcatid=l['cat_id'].split('_')

        insert_query = """
        INSERT INTO splunk
        (cat_id, path, port_status, src_interface, host, flap, hostname, device_time)
        VALUES
        """

        #get value for string and then insert to database
        if splitcatid[0] == 'NA':
            insert_query += "('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
                str(l['host']+l['src_interface']), str(l['cat_id']), str(l['port_status']), str(l['src_interface']), str(l['host']), str(l['flap']), str(l['hostname']), str(l['device_time']))
        else:
            insert_query += "('{[0]}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
                str(l['cat_id']).split('_'), str(l['cat_id']), str(l['port_status']), str(l['src_interface']), str(l['host']), str(l['flap']), str(l['hostname']), str(l['device_time']))
        get_status_insert_data = db.insert(insert_query)

        if not get_status_insert_data:
            sql_update_port_status = """
            UPDATE `splunk` SET `port_status`='{0}',`flap`='{1}' WHERE `cat_id`='{2}'
            """.format(l['port_status'], l['flap'], l['cat_id'])
            db.insert(sql_update_port_status)
            # print "update"
            # PrintDebug(insert_query)
            # PrintDebug(sql_update_port_status)
        else:
            print "DONE"

def insert_TTS(lst_catid):
    lst = []
    for c in lst_catid:
        lst.append(tts.Search(c['cat_id']))

    for l in lst:
        if l is not None:
            activity_table = ""
            ticket_info = tts.Get_TicketInfo(l['incident_id'])
            for t in ticket_info['activity_table']:
                date = str(t['datestamp']).split('/')
                year = date[2].split(' ')
                datetime = year[0] + '-' + date[1] + '-' + date[0] + ' ' + year[1]

                activity = '''"number": {0}, "datestamp": "{1}", "operator": "{2}", "division": "{3}", "description": "{4}", "type": "{5}"'''.format(
                    t['number'], datetime, t['operator'].encode('utf-8'), t['division'].encode('utf-8'),
                    t['description'].encode('utf-8'), t['type']
                )
                activity = '{' + activity + '},'
                activity_table = activity_table + activity
            activity_table = activity_table[:-1]
            activity_table = '[' + activity_table + ']'

            insert_query = """INSERT INTO `tts`(`ticketNo`,`incident_id`, `affected_item`, `cat_id`, `status`, `problem_status`, `downtime_start`, `downtime_time`, `owner_group`, `repairteam`, `oss_source`, `oss_destination`, `address`, `title`, `description`, `activity`) VALUES """
            value = "\n('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}')".format(
                l['incident_id'], l['number'], l['affected_item'].encode('utf-8'), l['catid'], l['status'], l['problem_status'],l['downtime_start'], l['downtime'],
                l['owner_group'].encode('utf-8'), l['repairteam'].encode('utf-8'), l['oss_source'].encode('utf-8'), l['oss_destination'].encode('utf-8'), ticket_info['instance/oss.address/oss.address'].encode('utf-8'), ticket_info['instance/brief.description'].encode('utf-8'), ticket_info['instance/action/action'].encode('utf-8'),
                activity_table
            )
            query = "{0} {1}".format(insert_query, value)
            # PrintDebug(query)
            resp_status = db.insert(query)
            if not resp_status:
                update_query = """ UPDATE `tts` SET `affected_item`='{0}',`status`='{1}',`problem_status`='{2}',`downtime_start`='{3}',`downtime_time`='{4}', `description`='{6}', `activity`='{7}' WHERE `ticketNo`='{5}' """.format(
                        l['affected_item'].encode('utf-8'), l['status'], l['problem_status'], l['downtime_start'], l['downtime'], l['incident_id'], ticket_info['instance/action/action'].encode('utf-8'), activity_table)
                db.insert(update_query)
                # PrintDebug(update_query)
                # print 'UPDATE'
            else:
                print 'DONE'

def job_SPLUNK(searchQuery):
    print 'Doing SPLUNK...'
    sid = splunk.CreateSearch(searchQuery, timerange='-72hr') #defind timerange query data
    print (sid)
    rs = splunk.GetSearchStatus(sid)
    while not rs == 'DONE':
        print rs
        time.sleep(15)
        rs = splunk.GetSearchStatus(sid)
    lst = splunk.GetSearchResult(sid)
    # print lst
    insert_Splunk(lst)  # insert list splunk data to database

def job_TTS():
    print 'Doing TTS...'
    select_catid = """ SELECT `cat_id`,`host` FROM `splunk` WHERE '1'"""
    lst_catid = db.query(select_catid)
    # run insert data
    insert_TTS(lst_catid)

def PrintDebug(msg):
    if True:
        print msg

if __name__ == "__main__":
    search_link = 'eventtype="cisco_ios-port_down" OR eventtype="cisco_ios-port_up" host="10.126.0.*" src_interface="POS*" OR "HundredGigE*" | stats count as flap,latest(device_time) AS device_time,latest(port_status) AS port_status by host,src_interface,cat_id,hostname  |sort -count '
    search_link_pe_flap_out_bangkok='eventtype="cisco_ios-port_down" OR eventtype="cisco_ios-port_up" host="10.5.*.*" host!="10.5.0.*" src_interface="TenGig*" OR "Gigabit*" port_status!="administratively down"'
    search_link_pe_flap_bangkok='eventtype="cisco_ios-port_down" OR eventtype="cisco_ios-port_up" host="10.5.0.*" OR "10.126.0.*" src_interface="TenGig*" OR "Gigabit*" port_status!="administratively down"   hostname="*" host="10.5.0.11" src_interface="*"'
    search_link_switch_layer_two='host!="10.6.*.*" host!="10.5.*.*" eventtype="cisco_ios-port_down" OR eventtype="cisco_ios-port_up" src_interface="FastE*" OR src_interface="TenGig*" OR "Gigabit*" port_status!="administratively down"  hostname=3GHSPA_NAN6519 host="10.163.27.2" src_interface="*"'
    job_SPLUNK(search_link)
    job_TTS()
