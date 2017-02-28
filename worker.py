class PostToFacebook(webapp2.RequestHandler):
    def post(self):

        good = 0
        bad = 0
        customer = 'unknown'
        resp1 = 'unknown'
        artTitle = 'unknown'

        fb_instructions = """<a href="#">Watch the Instructional Video</a><br /><br />

        When logged into the _________, in the top right, near the red Logout button is a link to your account page.<br ><br >

        On your account page in the left column is a Facebook Login button.  Click that and then select where you would like your articles posted.<br ><br >

        You will get a confirmation that everything's set up.<br ><br >

        Then please click on the Social tab and then Errors.  Go into any articles that didn't post and click the "Reset article" checkbox.<br ><br >

        Let us know if you have any trouble.<br ><br >"""

        error_sent = []

        try:

            aa_key = self.request.get('aa_key')

            aaDoc = getDocByKey(aa_key)
            if aaDoc:
                aaDoc.fbstatus = "working"
                aaDoc.put()
            else:
                err_mess = 'error_social_facebook_badkey: ' + aa_key
                logging.error(err_mess)
                return err_mess

            artTitle = aaDoc.title

            acctDoc = getAccountDoc(aaDoc.account_id)
            try:
                customer = acctDoc.company_name + ": "
            except:
                customer = "error get account: "

            fb_access_token = acctDoc.fb_access_token

            if fb_access_token != '':

                user_message = ""

                try:
                    if aaDoc.user_message != '':
                        user_message = "&message=" + urllib.quote_plus(aaDoc.user_message)
                except Exception as e:
                    user_message = ''

                fb_url = 'https://graph.facebook.com/v2.5/me/feed?access_token=' + fb_access_token
                fb_payload = 'link=' + aaDoc.content_url + "&bs=" + generateSecurityKey() + user_message

                fb_headers = {
                    'cache-control': "no-cache"
                }

                self = webapp2.RequestHandler

                resp1 = ''
                resp1 = monkeypatched_http_call(self, fb_url, "POST", data=fb_payload, headers=fb_headers)
                resp0 = str(resp1)
                logging.info('fb response: ' + resp0)
                if resp0 == '':

                    kwargs = {
                        'subject': 'Facebook timed out',
                        'body':    'Facebook timed out.... again.'
                    }
                    sendEmailGeneric(**kwargs)

                elif "error" in resp0:
                    try:
                        aaDoc.fbstatus_note = "Error: " + customer + json.loads(resp1)['error']['message']
                    except:
                        aaDoc.fbstatus_note = "Error: " + customer + resp1
                    # json.loads(resp1)['error']['message']
                    aaDoc.fbstatus = "error"
                    aaDoc.put()
                    bad += 1

                    logging.info('fb failed: ' + customer + aaDoc.title)

                    if not aaDoc.account_id in error_sent:
                        eml = {
                            'to_email':  acctDoc.account_email,
                            'body':      'Please login to your _________ account and refresh your Facebook login on the Account page.<br /><br />' + fb_instructions + aaDoc.fbstatus_note,
                            'subject':   '_________ needs your attention',
                            'title':     'Expired Connection',
                            'bcc_email': '_____@_______.com'
                        }

                        #KDH Removed to stop annoying customers 11/23/16
                        #sendEmailGenericSG(**eml)

                        error_sent.append(aaDoc.account_id)

                elif 'id' in resp0:
                    aaDoc.fbstatus_note = "Posted: " + customer + str(datetime.datetime.today())
                    aaDoc.fbstatus = "posted"
                    aaDoc.put()
                    good += 1
                    logging.info('fb posted: ' + customer + aaDoc.title)
                else:
                    aaDoc.fbstatus_note = "Error: " + customer + resp1
                    aaDoc.fbstatus = "error"
                    aaDoc.put()
                    bad += 1
                    logging.info('fb failed: ' + customer + aaDoc.title)

                    if not aaDoc.account_id in error_sent:
                        eml = {
                            'to_email':  acctDoc.account_email,
                            'body':      'Please login to your _________ account and refresh your Facebook login on the Account page.' + fb_instructions,
                            'subject':   '_________ needs your attention',
                            'title':     'Expired Connection',
                            'bcc_email': '_____@_______.com'
                        }

                        #KDH Removed to stop annoying customers 11/23/16
                        #sendEmailGenericSG(**eml)

                        error_sent.append(aaDoc.account_id)
            else:

                aaDoc.fbstatus_note = "Error: " + customer
                aaDoc.fbstatus = "error"
                aaDoc.put()
                bad += 1
                logging.info('fb failed: ' + customer + aaDoc.title)

                if not aaDoc.account_id in error_sent:
                    eml = {
                        'to_email':  acctDoc.account_email,
                        'body':      'Please login to your _________ account and create your Facebook connection on the Account page.<br /><br />' + fb_instructions,
                        'subject':   '_________ needs your attention',
                        'title':     'Facebook Connection',
                        'bcc_email': '_____@_______.com'
                    }

                    # KDH Removed to stop annoying customers 11/23/16
                    #sendEmailGenericSG(**eml)

                    error_sent.append(aaDoc.account_id)

        except Exception as e:
            logging.error('error_worker_342: ' + e.message)
            aaDoc.fbstatus_note = "Error: " + e.message
            aaDoc.fbstatus = "error"
            aaDoc.put()
            bad += 1

class PostToLinkedIn(webapp2.RequestHandler):
    def post(self):

        good = 0
        bad = 0
        customer = 'unknown'
        resp1 = 'unknown'
        artTitle = 'unknown'

        li_instructions = """When logged into the Rainmaker Lead System, in the top right, near the red Logout button is a link to your account page.<br ><br >

        On your account page in the left column is a LinkedIn Sign In button.  Click that and then select where you would like your articles posted.<br ><br >

        You will get a confirmation that everything's set up.<br ><br >

        Then please click on the Social tab and then Errors.  Go into any articles that didn't post and click the "Reset article" checkbox.<br ><br >

        Let us know if you have any trouble.<br ><br >"""

        error_sent = []

        try:

            aa_key = self.request.get('aa_key')

            aaDoc = getDocByKey(aa_key)
            if aaDoc:
                aaDoc.listatus = "working"
                aaDoc.put()
            else:
                err_mess = 'error_social_linkedin_badkey: ' + aa_key
                logging.error(err_mess)
                return err_mess

            artTitle = aaDoc.title

            acctDoc = getAccountDoc(aaDoc.account_id)
            try:
                customer = acctDoc.company_name + ": "
            except:
                customer = "error get account: "

            li_access_token = acctDoc.li_access_token

            if li_access_token != '':

                user_message = ""

                try:
                    if aaDoc.user_message != '':
                        user_message = aaDoc.user_message
                except Exception as e:
                    user_message = ''

                li_auth = "Bearer " + li_access_token
                li_url = "https://api.linkedin.com/v1/people/~/shares?format=json"
                data = {"comment": user_message, "content": {"title": aaDoc.title, "description": aaDoc.teaser,
                                                             "submitted-url": aaDoc.content_url,
                                                             "submitted-image-url": "http://www.erainmaker.com" + aaDoc.image_url},
                        "visibility": {"code": "anyone"}}
                li_payload = json.dumps(data)
                li_headers = {"Content-Type": "application/json", "x - li - format": "json", "Authorization": li_auth}
                logging.info(li_payload)
                self = webapp2.RequestHandler

                resp1 = ''
                resp1 = monkeypatched_http_call(self, li_url, "POST", data=li_payload, headers=li_headers)
                resp0 = str(resp1)
                logging.info('li response: ' + resp0)
                if resp0 == '':

                    kwargs = {
                        'subject': 'LinkedIn timed out',
                        'body':    'LinkedIn timed out.... again.'
                    }
                    sendEmailGeneric(**kwargs)


                elif "errorCode" in resp0:

                    try:

                        aaDoc.listatus_note = "Error: " + customer + json.loads(resp1)['errorCode']['message']

                    except:

                        aaDoc.listatus_note = "Error: " + customer + resp1

                    # json.loads(resp1)['error']['message']

                    aaDoc.listatus = "error"

                    aaDoc.put()

                    bad += 1

                    logging.info('LinkedIn failed: ' + customer + aaDoc.title)

                    if not aaDoc.account_id in error_sent:
                        eml = {

                            'to_email': acctDoc.account_email,

                            'body': 'Please login to your _________ account and refresh your LinkedIn login on the Account page.<br /><br />' + li_instructions + aaDoc.listatus_note,

                            'subject': '_________ needs your attention',

                            'title': 'Expired Connection',

                            'bcc_email': '_____@_______.com'

                        }

                        #KDH Removed to stop annoying customers 11/23/16
                        #sendEmailGenericSG(**eml)

                        error_sent.append(aaDoc.account_id)


                elif 'updateKey' in resp0:

                    aaDoc.listatus_note = "Posted: " + customer + str(datetime.datetime.today())

                    aaDoc.listatus = "posted"

                    aaDoc.put()

                    good += 1

                    logging.info('LinkedIn posted: ' + customer + aaDoc.title)

                else:

                    aaDoc.listatus_note = "Error: " + customer + resp1

                    aaDoc.listatus = "error"

                    aaDoc.put()

                    bad += 1

                    logging.info('LinkedIN failed: ' + customer + aaDoc.title)

                    if not aaDoc.account_id in error_sent:
                        eml = {

                            'to_email': acctDoc.account_email,

                            'body': 'Please login to your _________ account and refresh your LinkedIn login on the Account page.' + li_instructions,

                            'subject': '_________ needs your attention',

                            'title': 'Expired Connection',

                            'bcc_email': '_____@_______.com'

                        }

                        #KDH Removed to stop annoying customers 11/23/16
                        #sendEmailGenericSG(**eml)

                        error_sent.append(aaDoc.account_id)

            else:

                aaDoc.listatus_note = "Error: " + customer

                aaDoc.listatus = "error"

                aaDoc.put()

                bad += 1

                logging.info('LinkedIn failed: ' + customer + aaDoc.title)

                if not aaDoc.account_id in error_sent:
                    eml = {

                        'to_email': acctDoc.account_email,

                        'body': 'Please login to your _________ account and create your LinkedIn connection on the Account page.<br /><br />' + li_instructions,

                        'subject': '_________ needs your attention',

                        'title': 'LinkedIn Connection',

                        'bcc_email': '_____@_______.com'

                    }

                    # KDH Removed to stop annoying customers 11/23/16
                    #sendEmailGenericSG(**eml)

                    error_sent.append(aaDoc.account_id)

        except Exception as e:
            logging.error('error_worker_342: ' + e.message)
            aaDoc.listatus_note = "Error: " +  e.message
            aaDoc.listatus = "error"
            aaDoc.put()
            bad += 1

class PostToTwitter(webapp2.RequestHandler):
                def post(self):

                    good = 0
                    bad = 0
                    customer = 'unknown'
                    resp1 = 'unknown'
                    artTitle = 'unknown'

                    tw_instructions = """When logged into the Rainmaker Lead System, in the top right, near the red Logout button is a link to your account page.<br ><br >

                    On your account page in the left column is a Twitter Login button.  Click that and then select where you would like your articles posted.<br ><br >

                    You will get a confirmation that everything's set up.<br ><br >

                    Then please click on the Social tab and then Errors.  Go into any articles that didn't post and click the "Reset article" checkbox.<br ><br >

                    Let us know if you have any trouble.<br ><br >"""

                    error_sent = []

                    try:


                        aa_key = self.request.get('aa_key')

                        aaDoc = getDocByKey(aa_key)
                        if aaDoc:
                            aaDoc.twstatus = "working"
                            aaDoc.put()
                        else:
                            err_mess = 'error_social_twitter_badkey: ' + aa_key
                            logging.error(err_mess)
                            return err_mess

                        acctDoc = getAccountDoc(aaDoc.account_id)
                        tw_access_token = acctDoc.tw_access_token

                        if tw_access_token != '':

                            user_message = ""
                            custom_tweet = ""

                            try:
                                if aaDoc.user_message != '':
                                    custom_tweet = (aaDoc.user_message[:114] + '.. ') if len(aaDoc.user_message) > 116 else aaDoc.user_message
                            except Exception as e:
                                user_message = ''

                            from birdy.twitter import UserClient

                            CONSUMER_KEY = "qjw7GAC8WQuuAkBQnt04KXej0"
                            CONSUMER_SECRET = "3FpFoubONGhf7vR4TGffbTNzRYC1XK2CVoGZhCCLMxFmbQUFzW"
                            ACCESS_TOKEN = acctDoc.tw_access_token
                            ACCESS_TOKEN_SECRET = acctDoc.tw_secret

                            client = UserClient(CONSUMER_KEY,
                                                CONSUMER_SECRET,
                                                ACCESS_TOKEN,
                                                ACCESS_TOKEN_SECRET)
                            if custom_tweet != "":
                                response = client.api.statuses.update.post(
                                    status=custom_tweet + aaDoc.content_url)
                            else:
                                response = client.api.statuses.update.post(
                                    status=aaDoc.title + ": " + aaDoc.subtitle + " " + aaDoc.content_url)

                            resp0 = response.data

                            logging.info(resp0)

                            if "code" in resp0:
                                try:
                                    aaDoc.twstatus_note = "Error: " + customer + json.loads(resp0)['error']['message']
                                except:
                                    aaDoc.twstatus_note = "Error: " + customer + resp0
                                # json.loads(resp1)['error']['message']
                                aaDoc.twstatus = "error"
                                aaDoc.put()
                                bad += 1

                                logging.info('tw failed: ' + customer + aaDoc.title)

                                eml = {
                                    'to_email': acctDoc.account_email,
                                    'body': 'Please login to your _________ account and refresh your Twitter login on the Account page.<br /><br />' + aaDoc.twstatus_note,
                                    'subject': '_________ needs your attention',
                                    'title': 'Expired Connection',
                                    'bcc_email': '_____@_______.com'
                                }

                                sendEmailGenericSG(**eml)

                            elif 'id' in resp0:
                                aaDoc.twstatus_note = "Posted: " + customer + str(datetime.datetime.today())
                                aaDoc.twstatus = "posted"
                                aaDoc.put()
                                good += 1
                                logging.info('tw posted: ' + customer + aaDoc.title)
                            else:
                                aaDoc.twstatus_note = "Error: " + customer + resp1
                                aaDoc.twstatus = "error"
                                aaDoc.put()
                                bad += 1
                                logging.info('tw failed: ' + customer + aaDoc.title)

                                if not aaDoc.account_id in error_sent:
                                    eml = {

                                        'to_email': acctDoc.account_email,

                                        'body': 'Please login to your _________ account and refresh your Twitter login on the Account page.' + tw_instructions,

                                        'subject': '_________ needs your attention',

                                        'title': 'Expired Connection',

                                        'bcc_email': '_____@_______.com'

                                    }

                                    sendEmailGenericSG(**eml)

                                    error_sent.append(aaDoc.account_id)

                        else:

                            aaDoc.twstatus_note = "Error: " + customer

                            aaDoc.twstatus = "error"

                            aaDoc.put()

                            bad += 1

                            logging.info('Twitter failed: ' + customer + aaDoc.title)

                            if not aaDoc.account_id in error_sent:
                                eml = {

                                    'to_email': acctDoc.account_email,

                                    'body': 'Please login to your _________ account and create your Twitter connection on the Account page.<br /><br />' + tw_instructions,

                                    'subject': '_________ needs your attention',

                                    'title': 'Twitter Connection',

                                    'bcc_email': '_____@_______.com'

                                }

                                sendEmailGenericSG(**eml)

                                error_sent.append(aaDoc.account_id)

                    except Exception as e:
                        logging.error('error_worker_342: ' + e.message )
                        aaDoc.twstatus_note = "Error: " + e.message
                        aaDoc.twstatus = "error"
                        aaDoc.put()
                        bad += 1