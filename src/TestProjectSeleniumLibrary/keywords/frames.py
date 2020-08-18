# Copyright 2008-2011 Nokia Networks
# Copyright 2011-2016 Ryan Tomac, Ed Manlove and contributors
# Copyright 2016-     Robot Framework Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from TestProjectSeleniumLibrary.base import LibraryComponent, keyword


class FrameKeywords(LibraryComponent):

    @keyword
    def select_frame(self, locator):
        """Sets frame identified by ``locator`` as the current frame.

        See the `Locating elements` section for details about the locator
        syntax.

        Works both with frames and iframes. Use `Unselect Frame` to cancel
        the frame selection and return to the main frame.

        Example:
        | `Select Frame`   | top-frame | # Select frame with id or name 'top-frame'   |
        | `Click Link`     | example   | # Click link 'example' in the selected frame |
        | `Unselect Frame` |           | # Back to main frame.                        |
        | `Select Frame`   | //iframe[@name='xxx'] | # Select frame using xpath       |
        """
        try:
            self.info("Selecting frame '%s'." % locator)
            element = self.find_element(locator)
            self.driver.switch_to.frame(element)
            self.driver.report().step(description='Select Frame', message='Switched to frame at ' + locator + ' successfully', passed=True, screenshot=False)
        except Exception as e:
            self.driver.report().step(description='Select Frame', message='Could not switch to frame at ' + locator + '. Error:' + str(e), passed=False, screenshot=True)

    @keyword
    def unselect_frame(self):
        """Sets the main frame as the current frame.

        In practice cancels the previous `Select Frame` call.
        """
        try:
            self.driver.switch_to.default_content()
            self.driver.report().step(description='Unselect Frame', message='Switched to default content successully', passed=True, screenshot=False)
        except Exception as e:
            self.driver.report().step(description='Unselect Frame', message='Could not switch to default content. Error: ' + str(e) , passed=False, screenshot=True)


    @keyword
    def current_frame_should_contain(self, text, loglevel='TRACE'):
        """Verifies that the current frame contains ``text``.

        See `Page Should Contain` for an explanation about the ``loglevel``
        argument.

        Prior to SeleniumLibrary 3.0 this keyword was named
        `Current Frame Contains`.
        """
        if not self.is_text_present(text):
            self.log_source(loglevel)
            self.driver.report().step(description='Current Frame Should Contain', message='Current frame does not contain text ' + text, passed=False, screenshot=True)
            raise AssertionError("Frame should have contained text '%s' "
                                 "but did not." % text)
        self.driver.report().step(description='Current Frame Should Contain', message='Current frame contains text ' + text, passed=True, screenshot=False)
        self.info("Current frame contains text '%s'." % text)

    @keyword
    def current_frame_should_not_contain(self, text, loglevel='TRACE'):
        """Verifies that the current frame does not contain ``text``.

        See `Page Should Contain` for an explanation about the ``loglevel``
        argument.
        """
        if self.is_text_present(text):
            self.log_source(loglevel)
            self.driver.report().step(description='Current Frame Should Not Contain', message='Current frame contains text ' + text, passed=False, screenshot=True)
            raise AssertionError("Frame should not have contained text '%s' "
                                 "but it did." % text)
        self.driver.report().step(description='Current Frame Should Not Contain', message='Current frame does not contain text ' + text, passed=True, screenshot=False)
        self.info("Current frame did not contain text '%s'." % text)

    @keyword
    def frame_should_contain(self, locator, text, loglevel='TRACE'):
        """Verifies that frame identified by ``locator`` contains ``text``.

        See the `Locating elements` section for details about the locator
        syntax.

        See `Page Should Contain` for an explanation about the ``loglevel``
        argument.
        """
        try:
            element = self.find_element(locator)
            self.driver.switch_to.frame(element)
        except:
            self.driver.report().step(description='Frame Should Contain',
                                      message='Could not find frame at ' + locator, passed=False,
                                      screenshot=True)
            raise AssertionError("Frame does not exist.")
        self.info("Searching for text from frame '%s'." % locator)
        found = self.is_text_present(text)
        self.driver.switch_to.default_content()
        if not found:
            self.driver.report().step(description='Frame Should Contain', message='Frame at ' + locator + ' Does not contain text ' + text, passed=False, screenshot=True)
            raise AssertionError("Frame does not contain text.")
        self.driver.report().step(description='Frame Should Contain', message='Frame at ' + locator + ' contains text ' + text, passed=True, screenshot=False)
        self.info("Frame '%s' contains text '%s'." % (locator, text))
