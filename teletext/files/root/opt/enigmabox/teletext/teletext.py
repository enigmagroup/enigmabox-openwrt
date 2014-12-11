#!/usr/bin/python

import beanstalkc
import sqlite3
from gevent import spawn, sleep, monkey; monkey.patch_all()
from bottle import route, error, run, static_file, template, request, abort, redirect, debug, default_app, html_escape
from urllib import quote
from urllib2 import urlopen
from datetime import datetime, timedelta
from time import timezone, strptime, strftime, mktime
from json import loads as json_loads, dumps as json_dumps
from re import compile as re_compile



################################################################################
# utils
################################################################################

# internal decorator

def internal(fn):
    def check_ip(**kwargs):
        remote_ip = get_real_ip()

        if ':' in remote_ip:
            return '404'
        return fn(**kwargs)

    return check_ip

def get_real_ip():
    try:
        remote_ip = request.environ['HTTP_X_FORWARDED_FOR']
    except Exception:
        try:
            remote_ip = request.environ['HTTP_X_REAL_IP']
        except Exception:
            remote_ip = '::1'
    return remote_ip

def pad_ipv6(ipv6):
    splitter = ipv6.strip().split(':')
    return ':'.join([ str(block).zfill(4) for block in splitter ])

def format_datestring(date):
    dt = datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
    epoch = mktime(dt.timetuple())
    offset = datetime.fromtimestamp(epoch) - datetime.utcfromtimestamp(epoch)
    dt = dt + offset
    return dt.strftime('%H:%M - %d. %B %Y')

def format_text(text):
    text = html_escape(text)
    text = text.replace('\n', '<br />\n')
    r = re_compile(r"(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)")
    text = r.sub('<a target="_blank" href="\\1">\\1</a>', text)
    return text



################################################################################
# data class
################################################################################

class Data():
    def __init__(self, db_file):
        self.db = sqlite3.connect(db_file)
        self.c = self.db.cursor()
        try:
            self.c.execute("""SELECT value
            FROM meta
            WHERE key = 'dbversion'""")
            dbversion = self.c.fetchone()[0]
            self.migrate_db(dbversion)
        except:
            print 'initializing database'
            self.migrate_db(0)

    def migrate_db(self, version):
        version = int(version)
        if version < 1:
            print 'migrating to version 1'
            self.db.execute("""CREATE TABLE meta (
                id INTEGER PRIMARY KEY,
                key char(50) NOT NULL,
                value char(100) NOT NULL
            )""")
            self.db.execute("""CREATE TABLE telegrams (
                id INTEGER PRIMARY KEY,
                text char(256) NOT NULL,
                user_id INTEGER NULL,
                created_at datetime NOT NULL,
                retransmission_from char(39) NULL,
                retransmission_original_time datetime NULL,
                imported INTEGER DEFAULT 0
            )""")
            self.db.execute("""CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                ipv6 char(39) NOT NULL,
                name char(30) DEFAULT '',
                bio char(256) DEFAULT '',
                transmissions INTEGER DEFAULT 0,
                subscribers INTEGER DEFAULT 0,
                subscriptions INTEGER DEFAULT 0,
                updated_at datetime NULL
            )""")
            self.db.execute("""CREATE TABLE subscribers (
                id INTEGER PRIMARY KEY,
                ipv6 char(39) NOT NULL
            )""")
            self.db.execute("""CREATE TABLE subscriptions (
                id INTEGER PRIMARY KEY,
                ipv6 char(39) NOT NULL
            )""")

            self.db.execute("""INSERT INTO meta (key,value)
            VALUES ('dbversion','1')""")
            self.db.commit()
        if version < 2:
            print 'migrating to version 2'
            self.db.execute("""CREATE TABLE requests (
                id INTEGER PRIMARY KEY,
                direction char(10) NOT NULL,
                ipv6 char(39) NOT NULL,
                comments char(256) DEFAULT ''
            )""")

            self.db.execute("""UPDATE meta
            SET value = '2'
            WHERE key = 'dbversion'""")
            self.db.commit()
        #if version < 3:
        #    print 'migrating to version 3'
        #
        #    self.db.execute("""UPDATE meta
        #    SET value = '2'
        #    WHERE key = 'dbversion'""")
        #    self.db.commit()

    def get_meta(self, option_key, default=None):
        try:
            self.c.execute("""SELECT value
            FROM meta
            WHERE key = ?""", (option_key,))

            return self.c.fetchone()[0]

        except:
            return default

    def set_meta(self, option_key, option_value):
        try:
            self.c.execute("""UPDATE meta
            SET value = ?
            WHERE key = ?""", (option_value,option_key))
            if self.c.rowcount <= 0:
                raise
        except:
            self.db.execute("""INSERT INTO meta (key,value)
            VALUES (?,?)""", (option_key,option_value))

        self.db.commit()

    def set_user_attr(self, user_id, key, value):
        now = str(datetime.utcnow())
        self.c.execute("""UPDATE users
        SET """ + key + """ = ?, updated_at = ?
        WHERE id = ?""", (value,now,user_id))

        self.db.commit()

    def _get_or_create_userid(self, ipv6):
        try:
            self.c.execute("""SELECT id
            FROM users
            WHERE ipv6 = ?""", (ipv6,))
            user_id = self.c.fetchone()[0]

            return user_id

        except:
            self.c.execute("""INSERT INTO users (ipv6)
            VALUES (?)""", (ipv6,))
            user_id = self.c.lastrowid
            self.db.commit()

            return user_id

    def ghost_profile(self):
        return {
            'ipv6': '0000:0000:0000:0000:0000:0000:0000:0000',
            'name': 'Nobody',
            'bio': 'Offline. No Teletext.',
            'transmissions': '0',
            'subscribers': '0',
            'subscriptions': '0',
            'updated_at': datetime.utcnow(),
        }

    def get_profile(self, ipv6):
        my_ipv6 = self.get_meta('ipv6')
        user_id = self._get_or_create_userid(ipv6)

        self.c.execute("""SELECT ipv6, name, bio, transmissions, subscribers, subscriptions, updated_at
        FROM users
        WHERE id = ?""", (user_id,))

        result = self.c.fetchone()

        profile = {}
        profile['ipv6'] = result[0]
        profile['name'] = result[1]
        profile['bio'] = format_text(result[2])
        profile['bio_unescaped'] = result[2]
        profile['transmissions'] = result[3]
        profile['subscribers'] = result[4]
        profile['subscriptions'] = result[5]
        profile['updated_at'] = result[6]

        db_time = profile['updated_at']
        one_hour_ago = datetime.utcnow() - timedelta(hours = 1 - (1 + timezone/60/60))
        try:
            t = strptime(db_time, '%Y-%m-%d %H:%M:%S.%f')
            db_time = datetime(t[0], t[1], t[2], t[3], t[4], t[5])
        except:
            pass

        if db_time == None:
            #print 'no db time found, new profile, waiting for fetch...'
            profile = self._fetch_remote_profile(ipv6)

        elif db_time < one_hour_ago:
            if my_ipv6 == ipv6:
                self.refresh_counters()
            else:
                #print 'profile outdated, fetching...'
                queue = Queue()

                json = {
                    'job_desc': 'fetch_remote_profile',
                    'ipv6': ipv6
                }

                json = json_dumps(json)
                queue.add('write', json)

                queue.close()

        return profile

    def _fetch_remote_profile(self, ipv6):
        try:
            # bio
            response = urlopen(url='http://[' + ipv6 + ']:3838/api/v1/get_profile.json', timeout = 5)
            content = response.read()
            profile = json_loads(content)['profile']
            profile['ipv6'] = ipv6.strip()

            queue = Queue()

            json = {
                'job_desc': 'save_profile',
                'profile': profile
            }

            json = json_dumps(json)
            queue.add('write', json)

            queue.close()

            # avatar
            response = urlopen(url='http://[' + ipv6 + ']:3838/avatar.png', timeout = 5)
            content = response.read()
            f = open('./public/img/profile/' + ipv6 + '.png', 'wb')
            f.write(content)
            f.close()

        except:
            profile = self.ghost_profile()

        return profile

    def refresh_counters(self):
        queue = Queue()

        json = {
            'job_desc': 'refresh_counters',
        }

        json = json_dumps(json)
        queue.add('write', json)

        queue.close()

    def get_telegrams(self, author = False, no_imported = False, step = 0, since = False, fetch_external = False):

        step = str(step)
        my_ipv6 = self.get_meta('ipv6')

        if not author and not no_imported:

            if not since:
                since = '1970-01-01 00:00:00.000000'

            self.c.execute("""SELECT text, users.name as username, users.ipv6 as ipv6, created_at, retransmission_from, retransmission_original_time
            FROM telegrams
            LEFT JOIN users
            ON telegrams.user_id = users.id
            WHERE created_at > ?
            ORDER BY created_at DESC
            LIMIT 10 OFFSET ? """, (since,step))

        elif author and no_imported:

            if not since:
                since = '1970-01-01 00:00:00.000000'

            self.c.execute("""SELECT text, users.name as username, users.ipv6 as ipv6, created_at, retransmission_from, retransmission_original_time
            FROM telegrams
            LEFT JOIN users
            ON telegrams.user_id = users.id
            WHERE users.ipv6 = ?
            AND imported = 0
            AND created_at > ?
            ORDER BY created_at DESC
            LIMIT 10 OFFSET ? """, (author,since,step))

        elif not author and no_imported:
            self.c.execute("""SELECT text, users.name as username, users.ipv6 as ipv6, created_at, retransmission_from, retransmission_original_time
            FROM telegrams
            LEFT JOIN users
            ON telegrams.user_id = users.id
            WHERE imported = 0
            ORDER BY created_at DESC
            LIMIT 10 OFFSET ?""", (step,))

        elif author and not no_imported:
            self.c.execute("""SELECT text, users.name as username, users.ipv6 as ipv6, created_at, retransmission_from, retransmission_original_time
            FROM telegrams
            LEFT JOIN users
            ON telegrams.user_id = users.id
            WHERE users.ipv6 = ?
            ORDER BY created_at DESC
            LIMIT 10 OFFSET ?""", (author,step))

        result = self.c.fetchall()

        if len(result) == 0 and fetch_external and author != my_ipv6:
            try:
                profile = self.get_profile(author)
                response = urlopen(url='http://[' + author + ']:3838/api/v1/get_telegrams.json?step=' + str(step), timeout = 5)
                content = response.read()
                telegrams = json_loads(content)['telegrams']

                result = []
                for t in telegrams:
                    try:
                        result.append((t['text'], profile['name'], author, t['created_at'], t['retransmission_from'], t['retransmission_original_time']))
                    except:
                        result.append((t['text'], profile['name'], author, t['created_at']))
            except:
                pass

        telegrams = []

        for res in result:
            text = format_text(res[0])
            text_unescaped = res[0]
            author = res[1]
            ipv6 = res[2]
            created_at = res[3]
            created_at_formatted = format_datestring(res[3])

            if len(res) > 4 and res[4] != None:
                retransmission_from = res[4]

                try:
                    rt_profile = self.get_profile(retransmission_from)
                    rt_name = rt_profile['name']
                except:
                    rt_name = '[Offline]'

                retransmission_from_author = rt_name
                retransmission_original_time = res[5]
                retransmission_original_time_formatted = format_datestring(res[5])
            else:
                retransmission_from = None
                retransmission_from_author = None
                retransmission_original_time = None
                retransmission_original_time_formatted = None

            telegrams.append({
                'text': text,
                'text_unescaped': text_unescaped,
                'author': author,
                'ipv6': ipv6,
                'created_at': created_at,
                'created_at_formatted': created_at_formatted,
                'retransmission_from': retransmission_from,
                'retransmission_from_author': retransmission_from_author,
                'retransmission_original_time': retransmission_original_time,
                'retransmission_original_time_formatted': retransmission_original_time_formatted,
            })

        return telegrams

    def get_single_telegram(self, ipv6, created_at):

        my_ipv6 = self.get_meta('ipv6')

        self.c.execute("""SELECT text, users.name as username, users.ipv6 as ipv6, created_at, retransmission_from, retransmission_original_time
        FROM telegrams
        LEFT JOIN users
        ON telegrams.user_id = users.id
        WHERE users.ipv6 = ?
        AND created_at = ?
        ORDER BY created_at DESC
        LIMIT 1""", (ipv6,created_at))

        result = self.c.fetchone()

        if (result == None or len(result) == 0) and ipv6 != my_ipv6:
            try:
                response = urlopen(url='http://[' + ipv6 + ']:3838/api/v1/get_single_telegram.json?created_at=' + quote(created_at), timeout = 5)
                content = response.read()
                telegram = json_loads(content)['telegram']

                profile = self.get_profile(ipv6)
                try:
                    result = (telegram['text'], profile['name'], ipv6, telegram['created_at'], telegram['retransmission_from'], telegram['retransmission_original_time'])
                except:
                    result = (telegram['text'], profile['name'], ipv6, telegram['created_at'])
            except:
                pass

        if result != None:
            text = format_text(result[0])
            text_unescaped = result[0]
            author = result[1]
            ipv6 = result[2]
            created_at = result[3]
            created_at_formatted = format_datestring(result[3])

            if len(result) > 4 and result[4] != None:
                retransmission_from = result[4]

                try:
                    rt_profile = self.get_profile(retransmission_from)
                    rt_name = rt_profile['name']
                except:
                    rt_name = '[Offline]'

                retransmission_from_author = rt_name
                retransmission_original_time = result[5]
                retransmission_original_time_formatted = format_datestring(result[5])
            else:
                retransmission_from = None
                retransmission_from_author = None
                retransmission_original_time = None
                retransmission_original_time_formatted = None

            telegram = {
                'text': text,
                'text_unescaped': text_unescaped,
                'author': author,
                'ipv6': ipv6,
                'created_at': created_at,
                'created_at_formatted': created_at_formatted,
                'retransmission_from': retransmission_from,
                'retransmission_from_author': retransmission_from_author,
                'retransmission_original_time': retransmission_original_time,
                'retransmission_original_time_formatted': retransmission_original_time_formatted,
            }

        else:
            telegram = None

        return telegram

    def get_latest_telegram(self, author):
        self.c.execute("""SELECT created_at
        FROM telegrams
        LEFT JOIN users
        ON telegrams.user_id = users.id
        WHERE users.ipv6 = ?
        ORDER BY created_at DESC
        LIMIT 1""", (author,))

        result = self.c.fetchone()

        try:
            created_at = result[0]
        except:
            created_at = '1970-01-01 00:00:00.000000'

        return created_at

    def telegram_exists(self, author, created_at):
        user_id = self._get_or_create_userid(author)
        self.c.execute("""SELECT id
        FROM telegrams
        WHERE user_id = ?
        AND created_at = ?""", (user_id, created_at))

        return len(self.c.fetchall()) > 0

    def retransmission_exists(self, retransmission_from, retransmission_original_time):
        self.c.execute("""SELECT id
        FROM telegrams
        WHERE retransmission_from = ?
        AND retransmission_original_time = ?""", (retransmission_from, retransmission_original_time))

        return len(self.c.fetchall()) > 0

    def add_telegram(self, text, author, created_at, imported = '0', retransmission_from = None, retransmission_original_time = None):
        text = text[:256]
        user_id = self._get_or_create_userid(author)
        self.db.execute("""INSERT INTO telegrams (text,user_id,created_at,imported,retransmission_from,retransmission_original_time)
        VALUES (?,?,?,?,?,?)""", (text,user_id,created_at,imported,retransmission_from,retransmission_original_time))
        self.db.commit()
        self.refresh_counters()

    def retransmit_telegram(self, author, created_at):
        try:
            queue = Queue()
            telegram = self.get_single_telegram(author, created_at)
            my_ipv6 = self.get_meta('ipv6')
            now = str(datetime.utcnow())
            self.add_telegram(telegram['text_unescaped'], my_ipv6, now, 0, telegram['ipv6'], telegram['created_at'])

            # notify subscribers
            json = {
                'job_desc': 'notify_all_subscribers',
                'telegram': {
                    'text': telegram['text_unescaped'],
                    'created_at': now,
                    'retransmission_from': telegram['ipv6'],
                    'retransmission_original_time': telegram['created_at'],
                }
            }

            json = json_dumps(json)
            queue.add('notification', json)
            queue.close()

        except:
            print 'retransmission failed'

    def delete_telegram(self, ipv6, created_at):
        user_id = self._get_or_create_userid(ipv6)
        self.db.execute("""DELETE FROM telegrams
        WHERE user_id = ?
        AND created_at = ?
        LIMIT 1""", (user_id,created_at))
        self.db.commit()

    def get_userlist(self, subscription_type, ipv6 = False, step = 0):
        my_ipv6 = data.get_meta('ipv6')
        step = str(step)
        if subscription_type == 'subscribers':
            subscription_type = 'subscribers'
        elif subscription_type == 'subscriptions':
            subscription_type = 'subscriptions'

        if ipv6 == False or ipv6 == my_ipv6:
            self.c.execute("""SELECT """ + subscription_type + """.ipv6, users.name
            FROM """ + subscription_type + """
            LEFT JOIN users
            ON """ + subscription_type + """.ipv6 = users.ipv6
            ORDER BY """ + subscription_type + """.id DESC
            LIMIT 10 OFFSET ?""", (step,))

            result = self.c.fetchall()
        else:
            try:
                params = '?type=' + subscription_type + '&step=' + step
                response = urlopen(url='http://[' + ipv6 + ']:3838/api/v1/get_subscription.json' + params, timeout = 5)
                content = response.read()
                user_list = json_loads(content)['user_list']
                result = []
                for u in user_list:
                    result.append((u['ipv6'], u['name']))
            except:
                result = []

        user_list = []
        for res in result:
            ipv6 = res[0]
            name = res[1]
            subscribed = self.is_in_subscriptions(ipv6)

            user_list.append({
                'ipv6': ipv6,
                'name': name,
                'subscribed': subscribed,
            })

        return user_list

    def get_all_subscribers(self):
        self.c.execute("""SELECT subscribers.ipv6
        FROM subscribers
        ORDER BY id ASC""")

        result = self.c.fetchall()

        user_list = []
        for res in result:
            ipv6 = res[0]

            user_list.append({
                'ipv6': ipv6,
            })

        return user_list

    def add_subscriber(self, ipv6):
        if self.is_in_subscribers(ipv6):
            return False

        self.db.execute("""INSERT INTO subscribers (ipv6)
        VALUES (?)""", (ipv6,))
        self.db.commit()
        self.refresh_counters()
        spawn(data.get_profile, ipv6)
        return True

    def remove_subscriber(self, ipv6):
        self.db.execute("""DELETE FROM subscribers
        WHERE ipv6 = ?""", (ipv6,))
        self.db.commit()
        self.refresh_counters()

    def add_subscription(self, ipv6):
        self.db.execute("""INSERT INTO subscriptions (ipv6)
        VALUES (?)""", (ipv6,))
        self.db.commit()
        self.refresh_counters()
        spawn(get_transmissions, ipv6)

    def remove_subscription(self, ipv6):
        self.db.execute("""DELETE FROM subscriptions
        WHERE ipv6 = ?""", (ipv6,))
        self.db.commit()
        self.refresh_counters()

    def is_in_subscriptions(self, ipv6):
        self.c.execute("""SELECT id
        FROM subscriptions
        WHERE ipv6 = ?""", (ipv6,))

        return len(self.c.fetchall()) > 0

    def is_in_subscribers(self, ipv6):
        self.c.execute("""SELECT id
        FROM subscribers
        WHERE ipv6 = ?""", (ipv6,))

        return len(self.c.fetchall()) > 0

    def addr_get_requests(self, direction):
        self.c.execute("""SELECT requests.ipv6, requests.comments, users.name
        FROM requests
        LEFT JOIN users
        ON users.ipv6 = requests.ipv6
        WHERE requests.direction = ?
        ORDER BY requests.id ASC""", (direction,))

        result = self.c.fetchall()

        requests = []
        for res in result:
            ipv6 = res[0]
            comments = res[1]
            name = res[2]

            requests.append({
                'ipv6': ipv6,
                'comments': comments,
                'name': name,
            })

        return requests

    def pending_requests_exist(self):
        self.c.execute("""SELECT id
        FROM requests
        WHERE direction = 'from'""")

        return len(self.c.fetchall()) > 0

    # send or receive
    def addr_add_request(self, direction, ipv6, comments):
        comments = comments.decode('utf-8')
        if self.addr_is_in_requests(direction, ipv6):
            return False

        self.db.execute("""INSERT INTO requests (direction, ipv6, comments)
        VALUES (?,?,?)""", (direction,ipv6,comments))
        self.db.commit()

    # decline or confirm
    def addr_remove_request(self, direction, ipv6):
        self.db.execute("""DELETE FROM requests
        WHERE ipv6 = ?
        AND direction = ?""", (ipv6,direction))
        self.db.commit()

    def addr_is_in_requests(self, direction, ipv6):
        self.c.execute("""SELECT id
        FROM requests
        WHERE ipv6 = ?
        AND direction = ?""", (ipv6,direction))

        return len(self.c.fetchall()) > 0

data = Data('/box/teletext.db')



################################################################################
# routes
################################################################################

@route('/')
@internal
def root():
    username = data.get_meta('username', '')
    if username == '':
        redirect('/settings')

    check_new_transmissions()
    telegrams = data.get_telegrams()

    return template('home',
        telegrams = telegrams,
        xhr_url = '/xhr/timeline',
        my_ipv6 = data.get_meta('ipv6'),
        pending_requests = data.pending_requests_exist(),
    )



@route('/new_telegram', method = 'POST')
@internal
def new_telegram():
    text = request.POST.get('telegram', '').strip()

    if text != '':
        text = text.decode('utf-8')
        ipv6 = data.get_meta('ipv6')
        now = str(datetime.utcnow())

        queue = Queue()

        json = {
            'job_desc': 'add_telegram',
            'telegram': {
                'text': text,
                'author': ipv6,
                'created_at': now,
                'imported': 0,
            }
        }

        json = json_dumps(json)
        queue.add('write', json)

        json = {
            'job_desc': 'notify_all_subscribers',
            'telegram': {
                'text': text,
                'created_at': now,
            }
        }

        json = json_dumps(json)
        queue.add('notification', json)

        queue.close()

    redirect('/')



@route('/<ipv6:re:.{4}:.{4}:.{4}:.{4}:.{4}:.{4}:.{4}:.{4}>')
@internal
def profile_page(ipv6):
    username = data.get_meta('username', '')
    if username == '':
        redirect('/settings')

    my_ipv6 = data.get_meta('ipv6')
    profile = data.get_profile(ipv6)
    telegrams = data.get_telegrams(author = ipv6, fetch_external = True)
    subscribed = data.is_in_subscriptions(ipv6)

    return template('me',
        template = 'timeline',
        telegrams = telegrams,
        xhr_url = '/xhr/timeline?ipv6=' + ipv6,
        ipv6 = ipv6,
        username = profile['name'],
        bio = profile['bio'],
        transmissions = profile['transmissions'],
        subscribers = profile['subscribers'],
        subscriptions = profile['subscriptions'],
        my_ipv6 = my_ipv6,
        pending_requests = data.pending_requests_exist(),
        subscribed = subscribed,
    )



@route('/<ipv6:re:.{4}:.{4}:.{4}:.{4}:.{4}:.{4}:.{4}:.{4}>/<subscription_type:re:(subscribers|subscriptions)>')
@internal
def me(ipv6, subscription_type):

    my_ipv6 = data.get_meta('ipv6')
    profile = data.get_profile(ipv6)
    user_list = data.get_userlist(subscription_type, ipv6 = ipv6)
    subscribed = data.is_in_subscriptions(ipv6)

    return template('me',
        template = 'user_list',
        user_list = user_list,
        xhr_url = '/xhr/user_list/' + ipv6 + '/' + subscription_type,
        ipv6 = ipv6,
        username = profile['name'],
        bio = profile['bio'],
        transmissions = profile['transmissions'],
        subscribers = profile['subscribers'],
        subscriptions = profile['subscriptions'],
        my_ipv6 = my_ipv6,
        pending_requests = data.pending_requests_exist(),
        subscribed = subscribed,
    )



@route('/<ipv6:re:.{4}:.{4}:.{4}:.{4}:.{4}:.{4}:.{4}:.{4}>/<created_at>')
@internal
def single_telegram(ipv6, created_at):

    my_ipv6 = data.get_meta('ipv6')
    telegram = data.get_single_telegram(ipv6, created_at)

    if telegram == None:
        abort(404, 'Telegram does not exist')

    return template('telegram',
        telegram = telegram,
        my_ipv6 = my_ipv6,
        pending_requests = data.pending_requests_exist(),
    )



@route('/addressbook')
@internal
def addressbook():
    username = data.get_meta('username', '')
    if username == '':
        redirect('/settings')

    try:
        response = urlopen(url='http://127.0.0.1:8000/api/v1/get_contacts', timeout = 5)
        content = response.read()
        user_list = json_loads(content)['value']
    except:
        user_list = {}

    for i, user in enumerate(user_list):
        ipv6 = pad_ipv6(user_list[i]['ipv6'])
        user_list[i]['ipv6'] = ipv6
        user_list[i]['subscribed'] = data.is_in_subscriptions(ipv6)
        user_list[i]['name'] = user_list[i]['display_name']

    return template('addressbook',
        user_list = user_list,
        my_ipv6 = data.get_meta('ipv6'),
        pending_requests = data.pending_requests_exist(),
    )



@route('/addressbook/requests', method = ['GET', 'POST'])
@internal
def addressbook_requests():

    addrbook_url = ''

    if request.POST.get('confirm_request'):
        ipv6 = request.POST.get('confirm_request')
        profile = data.get_profile(ipv6)
        username = profile['name'].encode('utf-8')

        #TODO: remove print statements
        print 'making request to 127...'
        response = urlopen(url='http://127.0.0.1:8000/api/v1/add_contact',
            data = 'ipv6=' + ipv6 + '&hostname=' + quote(username),
            timeout = 5,
        )
        content = response.read()
        addrbook_url = json_loads(content)['addrbook_url']
        print 'making request to ' + ipv6
        urlopen(url='http://[' + ipv6 + ']:3838/api/v1/contact_request',
            data = 'what=confirm',
            timeout = 5,
        )
        data.addr_remove_request('from', ipv6)
        print 'done.'

    if request.POST.get('decline_request'):
        ipv6 = request.POST.get('decline_request')
        print 'making request to ' + ipv6
        urlopen(url='http://[' + ipv6 + ']:3838/api/v1/contact_request',
            data = 'what=decline',
            timeout = 5,
        )
        data.addr_remove_request('from', ipv6)
        print 'done.'

    requests_list = data.addr_get_requests('from')

    return template('addressbook_requests',
        requests_list = requests_list,
        addrbook_url = addrbook_url,
        my_ipv6 = data.get_meta('ipv6'),
        pending_requests = data.pending_requests_exist(),
    )



@route('/addressbook/requests/<ipv6:re:.{4}:.{4}:.{4}:.{4}:.{4}:.{4}:.{4}:.{4}>', method = ['GET', 'POST'])
@internal
def addressbook_new_request(ipv6):

    addrbook_url = ''
    profile = data.get_profile(ipv6)
    username = profile['name'].encode('utf-8')
    comments = request.POST.get('comments', '')[:256]

    if request.POST.get('send_request') and ipv6 != '':
        #TODO: remove printies
        print 'making request to 127...'
        response = urlopen(url='http://127.0.0.1:8000/api/v1/add_contact',
            data = 'ipv6=' + ipv6 + '&hostname=' + quote(username),
            timeout = 5,
        )
        content = response.read()
        addrbook_url = json_loads(content)['addrbook_url']
        print 'making request to ' + ipv6
        urlopen(url='http://[' + ipv6 + ']:3838/api/v1/contact_request',
            data = 'what=new&comments=' + quote(comments),
            timeout = 5,
        )
        data.addr_add_request('to', ipv6, comments)
        print 'done.'
        message = 'Request sent.'

    return template('addressbook_new_request',
        ipv6 = ipv6,
        addrbook_url = addrbook_url,
        my_ipv6 = data.get_meta('ipv6'),
        pending_requests = data.pending_requests_exist(),
    )



@route('/settings', method = ['GET', 'POST'])
@internal
def settings():

    ipv6 = data.get_meta('ipv6', False)

    if not ipv6:
        try:
            response = urlopen(url='http://127.0.0.1:8000/api/v1/get_option',
                data = 'key=ipv6',
                timeout = 5,
            )
            content = response.read()
            ipv6 = json_loads(content)['value'].strip()

        except:
            ipv6 = '0000:0000:0000:0000:0000:0000:0000:0000' #TODO

    user_id = data._get_or_create_userid(ipv6)
    data.set_meta('ipv6', ipv6)

    message = ('', '')

    # prefetch all profiles from the address book in the background
    try:
        response = urlopen(url='http://127.0.0.1:8000/api/v1/get_contacts', timeout = 5)
        content = response.read()
        user_list = json_loads(content)['value']
        for u in user_list:
            spawn(data.get_profile, u['ipv6'])
    except:
        pass

    if request.POST.get('save'):
        username = request.POST.get('username', '')[:30].decode('utf-8')
        bio = request.POST.get('bio', '')[:256].decode('utf-8')
        show_subscribers = request.POST.get('show_subscribers', '0')
        show_subscriptions = request.POST.get('show_subscriptions', '0')

        if username != '':
            data.set_meta('username', username)
            data.set_meta('bio', bio)
            data.set_meta('show_subscribers', show_subscribers)
            data.set_meta('show_subscriptions', show_subscriptions)

            image = request.files.get('image', False)

            if image:
                from PIL import Image
                img = Image.open(image.file)
                img.thumbnail((75, 75), Image.ANTIALIAS)
                img.save('./public/img/profile/' + ipv6 + '.png')

            data.set_user_attr(user_id, 'name', username)
            data.set_user_attr(user_id, 'bio', bio)

            message = ('success', 'Data successfully saved.')

        else:
            message = ('error', 'Error: Username must no be blank')

    return template('settings',
        username = data.get_meta('username', ''),
        bio = data.get_meta('bio', ''),
        show_subscribers = data.get_meta('show_subscribers', '1'),
        show_subscriptions = data.get_meta('show_subscriptions', '1'),
        message = message,
        my_ipv6 = data.get_meta('ipv6'),
        pending_requests = data.pending_requests_exist(),
    )



@route('/static/<filepath:path>')
@internal
def server_static(filepath):
    return static_file(filepath, root = './public')



@route('/xhr/timeline')
@internal
def xhr_timeline():

    step = request.GET.get('step', 0)
    since = request.GET.get('since', False)
    ipv6 = request.GET.get('ipv6', False)

    if ipv6:
        telegrams = data.get_telegrams(author = ipv6, step = step, since = since, fetch_external = True)
    else:
        telegrams = data.get_telegrams(step = step, since = since)

    return template('timeline',
        telegrams = telegrams,
        xhr = True,
        my_ipv6 = data.get_meta('ipv6'),
        pending_requests = data.pending_requests_exist(),
    )



@route('/xhr/user_list/<ipv6:re:.{4}:.{4}:.{4}:.{4}:.{4}:.{4}:.{4}:.{4}>/<subscription_type>')
@internal
def xhr_userlist(ipv6, subscription_type):

    step = request.GET.get('step', 0)
    user_list = data.get_userlist(subscription_type, ipv6, step)

    return template('user_list',
        user_list = user_list,
        xhr = True,
    )



@route('/xhr/subscribe', method = 'POST')
@internal
def xhr_subscribe():

    what = request.POST.get('what')
    ipv6 = request.POST.get('ipv6')

    if what == 'subscribe':
        try:
            response = urlopen(url='http://[' + ipv6 + ']:3838/api/v1/subscribe',
                data = 'ipv6=' + ipv6,
                timeout = 5,
            )
            content = response.read()
            result = json_loads(content)['result']
        except:
            result = 'failed'

        if result == 'success':
            data.add_subscription(ipv6)

        return {"result": result}

    elif what == 'unsubscribe':
        try:
            # just send a notification, but don't care for the result
            # unsubscribed guys will be checked with the next push notification
            response = urlopen(url='http://[' + ipv6 + ']:3838/api/v1/unsubscribe',
                data = 'ipv6=' + ipv6,
                timeout = 5,
            )
        except:
            pass

        data.remove_subscription(ipv6)
        return {"result": "success"}



@route('/xhr/retransmit', method = 'POST')
@internal
def xhr_retransmit():
    ipv6 = request.POST.get('ipv6')
    created_at = request.POST.get('created_at')

    queue = Queue()

    json = {
        'job_desc': 'retransmit_telegram',
        'telegram': {
            'ipv6': ipv6,
            'created_at': created_at,
        }
    }

    json = json_dumps(json)
    queue.add('write', json)

    # retransmit_telegram() handles the notification

    queue.close()

    return {"result": "success"}



@route('/xhr/delete', method = 'POST')
@internal
def xhr_delete():
    #ipv6 = request.POST.get('ipv6')
    my_ipv6 = data.get_meta('ipv6')
    created_at = request.POST.get('created_at')

    queue = Queue()

    json = {
        'job_desc': 'delete_telegram',
        'telegram': {
            'ipv6': my_ipv6,
            'created_at': created_at,
        }
    }

    json = json_dumps(json)
    queue.add('write', json)

    queue.close()

    return {"result": "success"}



@route('/xhr/check_status')
@internal
def xhr_check_status():
    ipv6 = request.GET.get('ipv6')
    try:
        response = urlopen(url='http://[' + ipv6 + ']:3838/api/v1/ping',
            timeout = 5,
        )
        content = response.read()
        result = json_loads(content)['result']
    except:
        result = 'failed'

    return {"result": result}



################################################################################
# API
################################################################################

@route('/api/v1/ping')
def api_ping():
    return {"result": "pong"}



@route('/api/v1/get_telegrams.json')
def telegrams_json():
    step = request.GET.get('step', 0)
    since = request.GET.get('since', False)
    ipv6 = data.get_meta('ipv6')
    telegrams = data.get_telegrams(author = ipv6, no_imported = True, step = step, since = since)

    for key, val in enumerate(telegrams):
        telegrams[key]['text'] = telegrams[key]['text_unescaped']
        del(telegrams[key]['text_unescaped'])
        del(telegrams[key]['author'])
        del(telegrams[key]['ipv6'])
        del(telegrams[key]['created_at_formatted'])
        del(telegrams[key]['retransmission_from_author'])
        del(telegrams[key]['retransmission_original_time_formatted'])

        if telegrams[key]['retransmission_from'] == None:
            del(telegrams[key]['retransmission_from'])
            del(telegrams[key]['retransmission_original_time'])

    return {"telegrams": telegrams}



@route('/api/v1/get_single_telegram.json')
def single_telegram_json():
    my_ipv6 = data.get_meta('ipv6')
    created_at = request.GET.get('created_at')
    telegram = data.get_single_telegram(my_ipv6, created_at)

    if telegram:
        telegram['text'] = telegram['text_unescaped']
        del(telegram['text_unescaped'])
        del(telegram['author'])
        del(telegram['ipv6'])
        del(telegram['created_at_formatted'])

        if telegram['retransmission_from'] == None:
            del(telegram['retransmission_from'])
            del(telegram['retransmission_from_author'])
            del(telegram['retransmission_original_time'])
            del(telegram['retransmission_original_time_formatted'])

    return {"telegram": telegram}



@route('/api/v1/new_telegram', method = 'POST')
def api_new_telegram():
    result = 'failed'

    telegram = request.POST.get('telegram', '').strip()

    if telegram != '':
        try:
            telegram = json_loads(telegram)
            text = telegram['text']
            ipv6 = pad_ipv6(get_real_ip())
            created_at = telegram['created_at']

            if not data.is_in_subscriptions(ipv6):
                return {"result": "unsubscribed"}

            try:
                # retransmission

                retransmission_from = telegram['retransmission_from']
                retransmission_original_time = telegram['retransmission_original_time']

                if data.retransmission_exists(retransmission_from, retransmission_original_time):
                    return {"result": "failed"}

                json = {
                    'job_desc': 'add_telegram',
                    'telegram': {
                        'text': text,
                        'author': ipv6,
                        'created_at': created_at,
                        'retransmission_from': retransmission_from,
                        'retransmission_original_time': retransmission_original_time,
                        'imported': 1,
                    }
                }

                json = json_dumps(json)

                queue = Queue()
                queue.add('write', json)
                queue.close()

                result = 'success'

            except:
                # regular telegram

                json = {
                    'job_desc': 'add_telegram',
                    'telegram': {
                        'text': text,
                        'author': ipv6,
                        'created_at': created_at,
                        'imported': 1,
                    }
                }

                json = json_dumps(json)

                queue = Queue()
                queue.add('write', json)
                queue.close()

                result = 'success'

        except:
            pass

    return {"result": result}



@route('/api/v1/get_profile.json')
def profile_json():
    my_ipv6 = data.get_meta('ipv6')
    profile = data.get_profile(my_ipv6)

    del(profile['ipv6'])
    del(profile['updated_at'])
    profile['bio'] = profile['bio_unescaped']
    del(profile['bio_unescaped'])

    return {"profile": profile}



@route('/avatar.png')
def external_profile_image():
    ipv6 = data.get_meta('ipv6')
    return static_file('/img/profile/' + ipv6 + '.png', root = './public')



@route('/api/v1/get_subscription.json')
def profile_json():

    subscription_type = request.GET.get('type')
    step = request.GET.get('step', 0)

    if subscription_type == 'subscribers':
        show_subscribers = data.get_meta('show_subscribers', '0')
        if show_subscribers == '1':
            user_list = data.get_userlist(subscription_type = 'subscribers', step = step),

    elif subscription_type == 'subscriptions':
        show_subscriptions = data.get_meta('show_subscriptions', '0')
        if show_subscriptions == '1':
            user_list = data.get_userlist(subscription_type = 'subscriptions', step = step),

    try:
        user_list = user_list[0]
    except:
        user_list = {}

    # kick unnecessary fields
    for key, val in enumerate(user_list):
        del(user_list[key]['subscribed'])

    return {"user_list": user_list}



@route('/api/v1/subscribe', method = 'POST')
def external_subscribe():
    try:
        ipv6 = pad_ipv6(get_real_ip())
        data.add_subscriber(ipv6)
        result = 'success'
    except:
        result = 'failed'

    return {"result": result}



@route('/api/v1/unsubscribe', method = 'POST')
def external_unsubscribe():
    try:
        ipv6 = pad_ipv6(get_real_ip())
        data.remove_subscriber(ipv6)
        result = 'success'
    except:
        result = 'failed'

    return {"result": result}



@route('/api/v1/contact_request', method = 'POST')
def contact_request():
    try:
        ipv6 = pad_ipv6(get_real_ip())
        what = request.POST.get('what', False)
        comments = request.POST.get('comments', '')

        if what == 'new':
            print 'receiving new request'
            data.get_profile(ipv6)
            data.addr_add_request('from', ipv6, comments)
            print 'done.'
        elif what == 'confirm':
            print 'receiving confirmation from ' + ipv6
            data.addr_remove_request('to', ipv6)
            print 'done.'
        elif what == 'decline':
            print 'receiving declination from ' + ipv6
            data.addr_remove_request('to', ipv6)
        else:
            raise

        result = 'success'

    except:
        result = 'failed'

    return {"result": result}



@error(404)
def error404(error):
    return '404'

@error(405)
def error405(error):
    return '405'



################################################################################
# queue class
################################################################################

class Queue():
    def __init__(self):
        self.bs = beanstalkc.Connection()

    def add(self, queue, value):
        self.bs.use(queue)
        self.bs.put(value)

    def get_job(self, queue):
        self.bs.watch(queue)
        return self.bs.reserve()

    def close(self):
        self.bs.close()



################################################################################
# workers
################################################################################

def check_new_transmissions():
    db_time = data.get_meta('last_transmission_check')
    one_hour_ago = datetime.utcnow() - timedelta(minutes = 60 - (60 + timezone/60))
    try:
        t = strptime(db_time, '%Y-%m-%d %H:%M:%S.%f')
        db_time = datetime(t[0], t[1], t[2], t[3], t[4], t[5])
    except:
        pass

    if db_time == None or db_time < one_hour_ago:
        #print 'checking for new transmissions'
        subscriptions = data.get_userlist('subscriptions')
        for s in subscriptions:
            spawn(get_transmissions, s['ipv6'])

        data.set_meta('last_transmission_check', datetime.utcnow())



def get_transmissions(ipv6):
    queue = Queue()
    since = data.get_latest_telegram(ipv6)
    step = 0
    data.get_profile(ipv6)

    while True:

        try:
            params = '?since=' + since.replace(' ', '%20') + '&step=' + str(step)
            response = urlopen(url='http://[' + ipv6 + ']:3838/api/v1/get_telegrams.json' + params, timeout = 5)
            content = response.read()
            telegrams = json_loads(content)['telegrams']

            if len(telegrams) == 0:
                break

            step = step + 10

        except:
            return False

        for telegram in telegrams:
            text = telegram['text']
            created_at = telegram['created_at']

            try:
                # retransmission
                #print 'importing ' + text.encode('utf-8')

                retransmission_from = telegram['retransmission_from']
                retransmission_original_time = telegram['retransmission_original_time']

                if data.retransmission_exists(retransmission_from, retransmission_original_time):
                    continue

                json = {
                    'job_desc': 'add_telegram',
                    'telegram': {
                        'text': text,
                        'author': ipv6,
                        'created_at': created_at,
                        'retransmission_from': retransmission_from,
                        'retransmission_original_time': retransmission_original_time,
                        'imported': 1,
                    }
                }

                json = json_dumps(json)
                queue.add('write', json)

            except:
                # regular telegram
                #print 'importing ' + text.encode('utf-8')

                # import the telegram
                json = {
                    'job_desc': 'add_telegram',
                    'telegram': {
                        'text': text,
                        'author': ipv6,
                        'created_at': created_at,
                        'imported': 1,
                    }
                }

                json = json_dumps(json)
                queue.add('write', json)

    queue.close()



def write_worker():
    queue = Queue()
    while True:
        job = queue.get_job('write')
        #print 'got job'

        try:
            job_body = json_loads(job.body)

            if job_body['job_desc'] == 'add_telegram':
                text = job_body['telegram']['text']
                author = job_body['telegram']['author']
                created_at = job_body['telegram']['created_at']
                imported = job_body['telegram']['imported']
                #print job_body

                try:
                    # retransmission
                    retransmission_from = job_body['telegram']['retransmission_from']
                    retransmission_original_time = job_body['telegram']['retransmission_original_time']
                    if not data.telegram_exists(retransmission_from, retransmission_original_time):
                        data.add_telegram(text, author, created_at, imported, retransmission_from, retransmission_original_time)
                except:
                    # regular telegram
                    if not data.telegram_exists(author, created_at):
                        data.add_telegram(text, author, created_at, imported)

            elif job_body['job_desc'] == 'retransmit_telegram':
                ipv6 = job_body['telegram']['ipv6']
                created_at = job_body['telegram']['created_at']
                data.retransmit_telegram(ipv6, created_at)

            elif job_body['job_desc'] == 'delete_telegram':
                ipv6 = job_body['telegram']['ipv6']
                created_at = job_body['telegram']['created_at']
                data.delete_telegram(ipv6, created_at)

            elif job_body['job_desc'] == 'save_profile':
                profile = job_body['profile']
                user_id = data._get_or_create_userid(profile['ipv6'])
                data.set_user_attr(user_id, 'name', profile['name'])
                data.set_user_attr(user_id, 'bio', profile['bio'])
                data.set_user_attr(user_id, 'transmissions', profile['transmissions'])
                data.set_user_attr(user_id, 'subscribers', profile['subscribers'])
                data.set_user_attr(user_id, 'subscriptions', profile['subscriptions'])

            elif job_body['job_desc'] == 'refresh_counters':
                my_ipv6 = data.get_meta('ipv6')
                user_id = data._get_or_create_userid(my_ipv6)

                # count transmissions
                data.c.execute("""SELECT Count(id)
                FROM telegrams
                WHERE user_id = ?""", (user_id,))
                transmissions_count = data.c.fetchone()[0]

                # count subscribers
                data.c.execute("""SELECT Count(id)
                FROM subscribers""")
                subscribers_count = data.c.fetchone()[0]

                # count subscriptions
                data.c.execute("""SELECT Count(id)
                FROM subscriptions""")
                subscriptions_count = data.c.fetchone()[0]

                data.set_user_attr(user_id, 'transmissions', transmissions_count)
                data.set_user_attr(user_id, 'subscribers', subscribers_count)
                data.set_user_attr(user_id, 'subscriptions', subscriptions_count)

            elif job_body['job_desc'] == 'fetch_remote_profile':
                ipv6 = job_body['ipv6']
                profile = data.get_profile(ipv6)
                db_time = profile['updated_at']
                one_hour_ago = datetime.utcnow() - timedelta(hours = 1 - (1 + timezone/60/60))
                t = strptime(db_time, '%Y-%m-%d %H:%M:%S.%f')
                db_time = datetime(t[0], t[1], t[2], t[3], t[4], t[5])

                if db_time < one_hour_ago:
                    user_id = data._get_or_create_userid(ipv6)
                    data.set_user_attr(user_id, 'name', profile['name'])    # just to refresh updated_at
                    data._fetch_remote_profile(ipv6)

        except:
            print 'error processing job'

        job.delete()
        #print 'job finished.'



def notification_worker():
    queue = Queue()
    while True:
        job = queue.get_job('notification')
        #print 'got job'

        try:
            job_body = json_loads(job.body)

            if job_body['job_desc'] == 'push_telegram':
                try:
                    # retransmission

                    receiver = job_body['telegram']['receiver']
                    text = job_body['telegram']['text']
                    created_at = job_body['telegram']['created_at']
                    retransmission_from = job_body['telegram']['retransmission_from']
                    retransmission_original_time = job_body['telegram']['retransmission_original_time']

                    json = {
                        'text': text,
                        'created_at': created_at,
                        'retransmission_from': retransmission_from,
                        'retransmission_original_time': retransmission_original_time,
                    }
                    json = json_dumps(json)

                    response = urlopen(url='http://[' + receiver + ']:3838/api/v1/new_telegram',
                        data = 'telegram=' + quote(json),
                        timeout = 60,
                    )
                    content = response.read()
                    result = json_loads(content)['result']

                except:
                    # regular telegram

                    receiver = job_body['telegram']['receiver']
                    text = job_body['telegram']['text']
                    created_at = job_body['telegram']['created_at']

                    json = {
                        'text': text,
                        'created_at': created_at,
                    }
                    json = json_dumps(json)

                    response = urlopen(url='http://[' + receiver + ']:3838/api/v1/new_telegram',
                        data = 'telegram=' + quote(json),
                        timeout = 60,
                    )
                    content = response.read()
                    result = json_loads(content)['result']


                if result == 'unsubscribed':
                    data.remove_subscriber(receiver)

            elif job_body['job_desc'] == 'notify_all_subscribers':
                try:
                    # retransmission

                    text = job_body['telegram']['text']
                    created_at = job_body['telegram']['created_at']
                    retransmission_from = job_body['telegram']['retransmission_from']
                    retransmission_original_time = job_body['telegram']['retransmission_original_time']

                    # push notification
                    subscribers = data.get_all_subscribers()

                    i = -10 #process first 10 without sleep
                    for sub in subscribers:

                        if i % 200 == 0:
                            sleep(1)

                        json = {
                            'job_desc': 'push_telegram',
                            'telegram': {
                                'text': text,
                                'created_at': created_at,
                                'retransmission_from': retransmission_from,
                                'retransmission_original_time': retransmission_original_time,
                                'receiver': sub['ipv6'],
                            }
                        }

                        json = json_dumps(json)
                        queue.add('notification', json)

                        i = i + 1

                except:
                    # regular telegram

                    text = job_body['telegram']['text']
                    created_at = job_body['telegram']['created_at']
                    #print job_body

                    # push notification
                    subscribers = data.get_all_subscribers()

                    i = -10 #process first 10 without sleep
                    for sub in subscribers:

                        if i % 200 == 0:
                            sleep(1)

                        json = {
                            'job_desc': 'push_telegram',
                            'telegram': {
                                'text': text,
                                'created_at': created_at,
                                'receiver': sub['ipv6'],
                            }
                        }

                        json = json_dumps(json)
                        queue.add('notification', json)

                        i = i + 1

        except:
            pass
            #print 'error processing job'

        job.delete()
        #print 'job finished.'



################################################################################
# startup
################################################################################

# spawn the write worker
spawn(write_worker)

# spawn 10 notification workers with some delay in between to prevent segfaults
for i in range(10):
    spawn(notification_worker)
    sleep(0.2)



if __name__ == "__main__":
    debug(True)
    run(host='127.0.0.1', port=8008, server='gevent')

app = default_app()

