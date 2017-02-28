	class GetFbToken(webapp.RequestHandler):
    def get(self):
        acctDoc = uBrowserAuthAcctDoc(self)
        if acctDoc is None:
            lp = LoginPageNoAuth()
            lp.get(self)
            return


        try:
            import urlparse

            fb_short_token = self.request.get('short_token')
            page_id = self.request.get('pageID')

            if page_id != 'undefined':
                fb_url = 'https://graph.facebook.com/me/accounts?access_token=' + acctDoc.fb_access_token
                fb_payload = ''
                fb_headers = {}

                resp1 = ''
                resp1 = monkeypatched_http_call(self, fb_url, "GET", data=fb_payload, headers=fb_headers)
                resp0 = json.loads(resp1)
                logging.info(resp0)
                for item in resp0["data"]:
                    if item["id"] == page_id:
                        fb_long_token = item["access_token"]
                        acctDoc.fb_access_token = fb_long_token
                        feat = acctDoc.social_active
                        if "facebook" not in feat:
                            feat.append('facebook')
                            acctDoc.social_active = feat

                        acctDoc.put()

                        deleteAcctDocMemCache(self)
                        if acctDoc.fb_access_token == fb_long_token:
                            self.response.write('2')
                        else:
                            self.response.write('0')
            else:

                fb_long_token_url = 'https://graph.facebook.com/oauth/access_token?client_id='+fb_app_id+'&client_secret='+fb_app_secret+'&grant_type=fb_exchange_token&fb_exchange_token='+fb_short_token

                resp = urllib2.urlopen(fb_long_token_url)

                url = 'path?' + resp.read()
                parsed = urlparse.urlparse(url)
                fb_long_token = urlparse.parse_qs(parsed.query)['access_token'][0]

                acctDoc.fb_access_token = fb_long_token
                feat = acctDoc.social_active
                if "facebook" not in feat:
                    feat.append('facebook')
                    acctDoc.social_active = feat

                acctDoc.put()

                deleteAcctDocMemCache(self)

                if acctDoc.fb_access_token == fb_long_token:
                    self.response.write('1')
                else:
                    self.response.write('0')

        except Exception as e:
            logging.error('ERROR: Couldnt find account ' + e.message)
            self.response.write('0')
			
	class GetLiToken(webapp.RequestHandler):
    def get(self):
        acctDoc = uBrowserAuthAcctDoc(self)
        if acctDoc is None:
            lp = LoginPageNoAuth()
            lp.get(self)
            return
        if self.request.get('error') != "":
            error_redirect = str('http://www.________.com/rm_account.html?error=' +  self.request.get('error'))
            self.redirect(error_redirect)
            return
        try:
            import urlparse
            import urllib
            import urllib2

            li_short_token = self.request.get('code')
            acctDoc.li_short_token = li_short_token
            acctDoc.put()

            req = urllib2.Request('https://www.linkedin.com/oauth/v2/accessToken?grant_type=authorization_code&code=' + li_short_token + '&redirect_uri=http%3A%2F%2Fwww.________.com%2Frm_get_li_token&client_id=' + li_app_id + '&client_secret=' + li_app_secret)
            response = urllib2.urlopen(req)
            data = json.load(response)
            li_long_token = data["access_token"]

            acctDoc.li_access_token = li_long_token
            feat = acctDoc.social_active
            if "linkedin" not in feat:
                feat.append('linkedin')
                acctDoc.social_active = feat

            acctDoc.put()

            deleteAcctDocMemCache(self)

            self.redirect('rm_account.html')

        except Exception as e:
            logging.error('ERROR: Couldnt find account ' + e.message)
			
			class GetTwToken(webapp.RequestHandler):
    def get(self):
        acctDoc = uBrowserAuthAcctDoc(self)
        if acctDoc is None:
            lp = LoginPageNoAuth()
            lp.get(self)
            return
        try:
            import requests
            import urlparse
            import urllib
            import urllib2
            from requests_oauthlib import OAuth1
            from urlparse import parse_qs

            REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
            AUTHORIZE_URL = "https://api.twitter.com/oauth/authorize?oauth_token="
            ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"

            CONSUMER_KEY = "qjw7GAC8WQuuAkBQnt04KXej0"
            CONSUMER_SECRET = "3FpFoubONGhf7vR4TGffbTNzRYC1XK2CVoGZhCCLMxFmbQUFzW"

            OAUTH_TOKEN = ""
            OAUTH_TOKEN_SECRET = ""

            oauth = OAuth1(CONSUMER_KEY, client_secret=CONSUMER_SECRET)
            r = requests.post(url=REQUEST_TOKEN_URL, auth=oauth)
            credentials = parse_qs(r.content)

            resource_owner_key = credentials.get('oauth_token')[0]
            resource_owner_secret = credentials.get('oauth_token_secret')[0]

            check_token = self.request.get('oauth_token')
            check_verifier = self.request.get('oauth_verifier')

            if len(check_token) == 0 and len(check_verifier) == 0:
                # Authorize
                authorize_url = AUTHORIZE_URL + resource_owner_key
                self.redirect(authorize_url)

            else:

                verifier = self.request.get('oauth_verifier')
                oauth = OAuth1(CONSUMER_KEY,
                                   client_secret=CONSUMER_SECRET,
                                   resource_owner_key=check_token,
                                   resource_owner_secret=resource_owner_secret,
                                   verifier=verifier)

                # Finally, Obtain the Access Token
                r = requests.post(url=ACCESS_TOKEN_URL, auth=oauth)
                credentials = parse_qs(r.content)
                token = credentials.get('oauth_token')[0]
                secret = credentials.get('oauth_token_secret')[0]
                username = credentials.get('screen_name')[0]

                acctDoc.tw_access_token = token
                acctDoc.tw_secret = secret
                acctDoc.tw_user = username
                feat = acctDoc.social_active
                if "twitter" not in feat:
                    feat.append('twitter')
                    acctDoc.social_active = feat

                acctDoc.put()

                deleteAcctDocMemCache(self)

                self.redirect('/rm_account.html')

        except Exception as e:
            logging.error('ERROR: Couldnt find account ' + e.message)

	
	
	('/rm_get_fb_token', GetFbToken),
    ('/rm_get_li_token', GetLiToken),
    ('/rm_get_tw_token', GetTwToken),