#!/usr/bin/env python
# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
# The Original Code is Mozilla WebQA Selenium Tests.
#
# The Initial Developer of the Original Code is
# Mozilla.
# Portions created by the Initial Developer are Copyright (C) 2011
# the Initial Developer. All Rights Reserved.
#
# Contributor(s): Bebe <florin.strugariu@softvision.ro>
#                 Alex Rodionov <p0deje@gmail.com>
#                 Teodosia Pop <teodosia.pop@softvision.ro>
#
# Alternatively, the contents of this file may be used under the terms of
# either the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.
#
# ***** END LICENSE BLOCK *****

from page import Page


class AddonsBasePage(Page):

    _next_link_locator = "link=Next"
    _previous_link_locator = "link=Prev"
    _current_page_locator = "css=.pagination li.selected a"
    _last_page_link_locator = "css=.pagination a:not([rel]):last"
    _first_page_link_locator = "css=.pagination a:not([rel]):first"

    def page_forward(self):
        self.selenium.click(self._next_link_locator)
        self.selenium.wait_for_page_to_load(self.timeout)

    def page_back(self):
        self.selenium.click(self._previous_link_locator)
        self.selenium.wait_for_page_to_load(self.timeout)

    @property
    def is_prev_link_present(self):
        return self.selenium.is_element_present(self._previous_link_locator)

    @property
    def is_prev_link_visible(self):
        return self.selenium.is_visible(self._previous_link_locator)

    @property
    def is_next_link_present(self):
        return self.selenium.is_element_present(self._next_link_locator)

    @property
    def is_next_link_visible(self):
        return self.selenium.is_visible(self._next_link_locator)

    @property
    def current_page(self):
        return int(self.selenium.get_text(self._current_page_locator))

    def go_to_last_page(self):
        self.selenium.click(self._last_page_link_locator)
        self.selenium.wait_for_page_to_load(self.timeout)

    def go_to_first_page(self):
        self.selenium.click(self._first_page_link_locator)
        self.selenium.wait_for_page_to_load(self.timeout)

    def credentials_of_user(self, user):
        return self.parse_yaml_file(self.credentials)[user]

    @property
    def header(self):
        return AddonsBasePage.HeaderRegion(self.testsetup)

    class HeaderRegion(Page):

        #other applications
        _other_applications_locator = "css=#other-apps"
        _app_thunderbird = "css=#app-thunderbird a"


        _other_apps_locator = "id=other-apps"


        #Search box
        _search_button_locator = "css=input.submit"
        _search_textbox_locator = "name=q"

        #Not LogedIn
        _login_locator = "css=.amo-header .context a:nth(1)"  # Until https://bugzilla.mozilla.org/show_bug.cgi?id=669646
        _register_locator = "css=.amo-header .context a:nth(0)"

        #LogedIn
        _account_controller_locator = 'css=#aux-nav .account .controller'
        _dropdown_locator = "css=#aux-nav .account ul"

        # Impala locators
        _impala_login_locator = "css=#aux-nav a:nth(1)"
        _impala_account_controller_locator = 'css=#aux-nav .account .user'


        def click_other_applications(self):
            self.selenium.click('%s a' % self._other_applications_locator)
            self.wait_for_element_visible('%s ul' % self._other_applications_locator)

        def click_thunderbird(self):
            self.selenium.click(self._app_thunderbird)
            self.selenium.wait_for_page_to_load(self.timeout)

        def is_thunderbird_visible(self):
            return self.is_element_present(self._app_thunderbird)

        @property
        def other_applications_tooltip(self):
            return self.selenium.get_attribute("%s@title" % self._other_apps_locator)

        def search_for(self, search_term):
            self.selenium.type(self._search_textbox_locator, search_term)
            self.selenium.click(self._search_button_locator)
            self.selenium.wait_for_page_to_load(self.timeout)
            from addons_search_home_page import AddonsSearchHomePage
            return AddonsSearchHomePage(self.testsetup)

        @property
        def search_field_placeholder(self):
            return self.selenium.get_attribute(self._search_textbox_locator + '@placeholder')

        def click_my_account(self):
            self.selenium.click(self._account_controller_locator)
            self.wait_for_element_visible(self._dropdown_locator)

        def click_login(self):
            if self.site_version == '/i':
                self.selenium.click(self._impala_login_locator)
            else:
                self.selenium.click(self._login_locator)
            self.selenium.wait_for_page_to_load(self.timeout)

        def click_logout(self):
            self.click_my_account()
            if self.selenium.get_text('%s > li:nth(3) a' % self._dropdown_locator) == "Log out":  # Until the https://bugzilla.mozilla.org/show_bug.cgi?id=669650
                self.selenium.click('%s > li:nth(3) a' % self._dropdown_locator)
            else:
                self.selenium.click('%s > li:nth(4) a' % self._dropdown_locator)
            self.selenium.wait_for_page_to_load(self.timeout)

        def click_edit_profile(self):
            self.click_my_account
            self.selenium.click('%s > li:nth(1) a' % self._dropdown_locator)
            self.selenium.wait_for_page_to_load(self.timeout)

        def click_view_profile(self):
            self.click_my_account
            self.selenium.click('%s > li:nth(0) a' % self._dropdown_locator)
            self.selenium.wait_for_page_to_load(self.timeout)
            from addons_user_page import AddonsViewProfilePage
            return AddonsViewProfilePage(self.testsetup)

        @property
        def is_user_logged_in(self):
            if self.site_version == '/i':
                locator = self._impala_account_controller_locator
            else:
                locator = self._account_controller_locator
            try:
                return self.selenium.is_visible(locator)
            except:
                return False
