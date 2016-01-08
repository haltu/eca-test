#!/usr/bin/env python
# -*- coding: utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2014-2015 Haltu Oy, http://haltu.fi
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os
import time
import unittest
from selenium import webdriver

DS_USER = os.environ.get('DS_USER')
DS_PASS = os.environ.get('DS_PASS')
TRAVIS_JOB_NUMBER = os.environ.get('TRAVIS_JOB_NUMBER')
SAUCE_USERNAME = os.environ.get('SAUCE_USERNAME')
SAUCE_ACCESS_KEY = os.environ.get('SAUCE_ACCESS_KEY')
TEST_ENV = os.environ.get('TEST_ENV', 'testing')  # testing or production
if TEST_ENV == 'production':
  TEST_ENV = False
else:
  TEST_ENV = True

if TEST_ENV:
  DS_LOGIN_URL = 'https://id.dreamschool.fi/login/educloud-test/'
else:
  DS_LOGIN_URL = 'https://id.dreamschool.fi/login/educloud/'


class TestMpassLoginToDreamSchool(unittest.TestCase):

  def setUp(self):
    if TRAVIS_JOB_NUMBER and SAUCE_USERNAME and SAUCE_ACCESS_KEY:
      self.driver = webdriver.Remote(
        desired_capabilities=webdriver.DesiredCapabilities.FIREFOX,
        command_executor='http://%s:%s@ondemand.saucelabs.com:80/wd/hub' %
        (SAUCE_USERNAME, SAUCE_ACCESS_KEY)
        )
    else:
      self.driver = webdriver.Firefox()

    self.driver.implicitly_wait(10)

  def test_login_via_mpass_with_ds_credentials(self):
    d = self.driver
    d.get(DS_LOGIN_URL)

    # Should redirect to mpass-proxy
    if TEST_ENV:
      proxy_host = 'mpass-proxy-test'
    else:
      proxy_host = 'mpass-proxy'
    self.assertIn(proxy_host, d.current_url)

    # Choose Dreamschool
    d.find_element_by_class_name('dreamschool').click()

    # Should be redirected to dreamschool login page
    self.assertIn('id.dreamschool.fi', d.current_url)

    # Enter credentials
    username = d.find_element_by_id('id_username')
    username.send_keys(DS_USER)

    password = d.find_element_by_id('id_password')
    password.send_keys(DS_PASS)

    password.submit()

    # After few redirects we should end up into dreamschool desktop
    time.sleep(2)
    self.assertIn('my.dreamschool.fi', d.current_url)

  def tearDown(self):
    self.driver.quit()

if __name__ == "__main__":
  unittest.main(verbosity=2)

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

