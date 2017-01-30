#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import re
import cgi

page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>User Signup</title>
    <style type="text/css">
        .error {
            color: red;
        }
    </style>
</head>
<body>
"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)



# test
class MainHandler(webapp2.RequestHandler):
    def get(self):

        header = "<h1>Signup</h1>"
        username_label = "<label>Username</label>"
        username_input = "<input name='username' value='%(username)s'/>"
        password_label = "<label>Password</label>"
        password_input = "<input type='password' name='password'/>"
        verify_label = "<label>Verify Password</label>"
        verify_input = "<input type='password' name='verify'/>"
        email_label = "<label>Email (optional)</label>"
        email_input = "<input name='email' value='%(email)s'/>"
        submit = "<input type='submit'/>"
        username = ""
        email = ""

        # if we have an error, make a <span> to display it
        error = self.request.get("error")
        error_element = ("<span class='error'>" + cgi.escape(error, quote=True) +
                        "</span>" if error else "")

        form = ("<form method='post'>" +
                header +
                username_label + username_input + error_element + "<br>" +
                password_label + password_input + error_element + "<br>" +
                verify_label + verify_input + error_element + "<br>" +
                email_label + email_input + error_element + "<br>" +
                submit + "</form>")

        content = page_header + form + page_footer
        self.response.write(content % {"username": username, "email":email})


    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        if password != verify:
            error = " Your passwords didn't match."
            error_num = 3
            error_escaped = cgi.escape(error, quote=True)
            self.redirect("/?error=" + error_escaped)
        else:
            self.redirect('/welcome?username=' + username)


class Welcome(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        content = page_header + "<h1>Welcome, " + username + "!</h1>" + page_footer
        self.response.write(content)



app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', Welcome)
], debug=True)
