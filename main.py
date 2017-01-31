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
        username_input = "<input name='username' value='%(username_esc)s'/>"
        password_label = "<label>Password</label>"
        password_input = "<input type='password' name='password'/>"
        verify_label = "<label>Verify Password</label>"
        verify_input = "<input type='password' name='verify'/>"
        email_label = "<label>Email (optional)</label>"
        email_input = "<input name='email' value='%(email_esc)s'/>"
        submit = "<input type='submit'/>"
        username = ""
        email = ""

        # if we have an error, make a <span> to display it
        error1 = self.request.get("error1")
        error_element1 = ("<span class='error'>" + error1 +
                        "</span>" if error1 else "")
        error2 = self.request.get("error2")
        error_element2 = ("<span class='error'>" + error2 +
                        "</span>" if error2 else "")
        error3 = self.request.get("error3")
        error_element3 = ("<span class='error'>" + error3 +
                        "</span>" if error3 else "")
        error4 = self.request.get("error4")
        error_element4 = ("<span class='error'>" + error4 +
                        "</span>" if error4 else "")

        form = ("<form method='post'>" +
                header +
                username_label + username_input + error_element1 + "<br>" +
                password_label + password_input + error_element2 + "<br>" +
                verify_label + verify_input + error_element3 + "<br>" +
                email_label + email_input + error_element4 + "<br>" +
                submit + "</form>")

        username = self.request.get("username")
        username_esc = cgi.escape(username, quote=True)
        email = self.request.get("email")
        email_esc = cgi.escape(email, quote=True)

        content = page_header + form + page_footer
        self.response.write(content % {"username_esc": username_esc, "email_esc": email_esc})


    def post(self):
        username = self.request.get("username")
        username_esc = cgi.escape(username, quote=True)
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")
        email_esc = cgi.escape(email, quote=True)
        are_errors = False
        error_num = 0
        errors = ""

        if not valid_username(username):
            are_errors = True
            error1 = " That's not a valid username"
            if error_num == 0:
                errors = ("/?error1=" + error1)
                error_num += 1
            else:
                errors = errors + "&error1=" + error1

        if not valid_password(password):
            are_errors = True
            error2 = " That wasn't a valid password"
            if error_num == 0:
                errors = ("/?error2=" + error2)
                error_num += 1
            else:
                errors = errors + "&error2=" + error2

        if password != verify:
            are_errors = True
            error3 = " Your passwords didn't match"
            if error_num == 0:
                errors = ("/?error3=" + error3)
                error_num += 1
            else:
                errors = errors + "&error3=" + error3

        if not valid_email(email):
            are_errors = True
            error4 = " That's not a valid email"
            if error_num == 0:
                errors = ("/?error4=" + error4)
                error_num += 1
            else:
                errors = errors + "&error4=" + error4


        if are_errors == True:
            #self.redirect(errors % {"username": username, "email": email})
            self.redirect(errors + "&username=" + username + "&email=" + email)
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
