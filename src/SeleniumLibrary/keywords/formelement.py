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

import os

from robot.libraries.BuiltIn import BuiltIn

from SeleniumLibrary.base import LibraryComponent, keyword
from SeleniumLibrary.errors import ElementNotFound
from SeleniumLibrary.utils import is_noney, is_truthy


class FormElementKeywords(LibraryComponent):

    @keyword
    def submit_form(self, locator=None):
        """Submits a form identified by ``locator``.

        If ``locator`` is not given, first form on the page is submitted.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        try:
            self.info("Submitting form '%s'." % locator)
            if is_noney(locator):
                locator = 'tag:form'
            element = self.find_element(locator, tag='form')
            element.submit()
            self.driver.report().step(description='Submit Form', message='Submitted form', passed=True,
                                      screenshot=False)
        except Exception as e:
            self.driver.report().step(description='Submit Form', message='Could not submit form', passed=False, screenshot=True)
            raise AssertionError

    @keyword
    def checkbox_should_be_selected(self, locator):
        """Verifies checkbox ``locator`` is selected/checked.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        self.info("Verifying checkbox '%s' is selected." % locator)
        element = None
        try:
            element = self._get_checkbox(locator)
        except Exception as e:
            self.driver.report().step(description='Checkbox Should Be Selected', message='Error: ' + str(e), passed=False,
                                      screenshot=True)
            raise AssertionError
        if not element.is_selected():
            self.driver.report().step(description='Checkbox Should Be Selected', message='Checkbox was not selected', passed=False,
                                      screenshot=True)
            raise AssertionError("Checkbox '%s' should have been selected "
                                 "but was not." % locator)

        self.driver.report().step(description='Checkbox Should Be Selected', message='Checkbox was selected',
                                passed=True,
                                screenshot=False)


    @keyword
    def checkbox_should_not_be_selected(self, locator):
        """Verifies checkbox ``locator`` is not selected/checked.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        self.info("Verifying checkbox '%s' is not selected." % locator)
        element = None
        try:
            element = self._get_checkbox(locator)
        except Exception as e:
            self.driver.report().step(description='Checkbox Should Not Be Selected', message='Error: ' + str(e),
                                      passed=False,
                                      screenshot=True)
            raise AssertionError
        if element.is_selected():
            self.driver.report().step(description='Checkbox Should Not Be Selected', message='Element is selected',
                                      passed=False,
                                      screenshot=True)
            raise AssertionError("Checkbox '%s' should not have been "
                                 "selected." % locator)
        self.driver.report().step(description='Checkbox Should Not Be Selected', message='Element is not selected', passed=True,
                                  screenshot=False)

    @keyword
    def page_should_contain_checkbox(self, locator, message=None, loglevel='TRACE'):
        """Verifies checkbox ``locator`` is found from the current page.

        See `Page Should Contain Element` for an explanation about ``message``
        and ``loglevel`` arguments.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        try:
            self.assert_page_contains(locator, 'checkbox', message, loglevel)
            self.driver.report().step(description='Page Should Contain Checkbox', message='Page contains checkbox',
                                      passed=True,
                                      screenshot=False)
        except Exception as e:
            self.driver.report().step(description='Page Should Contain Checkbox', message='Error: ' + str(e),
                                      passed=False,
                                      screenshot=True)
            raise AssertionError


    @keyword
    def page_should_not_contain_checkbox(self, locator, message=None, loglevel='TRACE'):
        """Verifies checkbox ``locator`` is not found from the current page.

        See `Page Should Contain Element` for an explanation about ``message``
        and ``loglevel`` arguments.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        try:
            self.assert_page_not_contains(locator, 'checkbox', message, loglevel)
            self.driver.report().step(description='Page Should Not contain Checkbox', message='Page does not contain checkbox',
                                      passed=True,
                                      screenshot=False)
        except Exception as e:
            self.driver.report().step(description='Page Should Not Contain Checkox', message='Error: ' + str(e),
                                      passed=False,
                                      screenshot=True)
            raise AssertionError

    @keyword
    def select_checkbox(self, locator):
        """Selects the checkbox identified by ``locator``.

        Does nothing if checkbox is already selected.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        try:
            self.info("Selecting checkbox '%s'." % locator)
            element = self._get_checkbox(locator)
            if not element.is_selected():
                element.click()
            self.driver.report().step(description='Select Checkbox', message='Checkbox selected',
                                      passed=True,
                                      screenshot=False)
        except Exception as e:
            self.driver.report().step(description='Select Checkbox', message='Error: ' + str(e),
                                      passed=False,
                                      screenshot=True)
            raise AssertionError

    @keyword
    def unselect_checkbox(self, locator):
        """Removes the selection of checkbox identified by ``locator``.

        Does nothing if the checkbox is not selected.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        try:
            self.info("Unselecting checkbox '%s'." % locator)
            element = self._get_checkbox(locator)
            if element.is_selected():
                element.click()
            self.driver.report().step(description='Unselect Checkbox', message='Unselected checkbox',
                                      passed=True,
                                      screenshot=False)
        except Exception as e:
            self.driver.report().step(description='Unselect Checkbox', message='Error: ' + str(e),
                                      passed=False,
                                      screenshot=True)
            raise AssertionError

    @keyword
    def page_should_contain_radio_button(self, locator, message=None, loglevel='TRACE'):
        """Verifies radio button ``locator`` is found from current page.

        See `Page Should Contain Element` for an explanation about ``message``
        and ``loglevel`` arguments.

        See the `Locating elements` section for details about the locator
        syntax. When using the default locator strategy, radio buttons are
        searched using ``id``, ``name`` and ``value``.
        """
        try:
            self.assert_page_contains(locator, 'radio button', message, loglevel)
            self.driver.report().step(description='Page Should Contain Radio Button', message='Page contains radio button',
                                      passed=True,
                                      screenshot=False)
        except Exception as e:
            self.driver.report().step(description='Page Should Contain Radio Button', message='Error: ' + str(e),
                                      passed=False,
                                      screenshot=True)
            raise AssertionError



    @keyword
    def page_should_not_contain_radio_button(self, locator, message=None, loglevel='TRACE'):
        """Verifies radio button ``locator`` is not found from current page.

        See `Page Should Contain Element` for an explanation about ``message``
        and ``loglevel`` arguments.

        See the `Locating elements` section for details about the locator
        syntax. When using the default locator strategy, radio buttons are
        searched using ``id``, ``name`` and ``value``.
        """
        try:
            self.assert_page_not_contains(locator, 'radio button', message,
                                          loglevel)
            self.driver.report().step(description='Page Should Not Contain Radio Button', message='Page does not contain radio button',
                                      passed=True,
                                      screenshot=False)
        except Exception as e:
            self.driver.report().step(description='Page Should Not Contain Radio Button', message='Error: ' + str(e),
                                      passed=False,
                                      screenshot=True)
            raise AssertionError

    @keyword
    def radio_button_should_be_set_to(self, group_name, value):
        """Verifies radio button group ``group_name`` is set to ``value``.

        ``group_name`` is the ``name`` of the radio button group.
        """
        self.info("Verifying radio button '%s' has selection '%s'."
                  % (group_name, value))
        try:
            elements = self._get_radio_buttons(group_name)
            actual_value = self._get_value_from_radio_buttons(elements)
        except Exception as e:
            self.driver.report().step(description='Radio Button Should Be Set To',
                                      message='Error: ' + str(e),
                                      passed=False,
                                      screenshot=True)
            raise AssertionError
        if actual_value is None or actual_value != value:
            self.driver.report().step(description='Radio Button Should Be Set To', message='Radio button was not set to value',
                                      passed=False,
                                      screenshot=True)
            raise AssertionError("Selection of radio button '%s' should have "
                                 "been '%s' but was '%s'."
                                 % (group_name, value, actual_value))
        self.driver.report().step(description='Radio Button Should Be Set To',
                                  message='Radio was set to value',
                                  passed=True,
                                  screenshot=False)

    @keyword
    def radio_button_should_not_be_selected(self, group_name):
        """Verifies radio button group ``group_name`` has no selection.

        ``group_name`` is the ``name`` of the radio button group.
        """
        self.info("Verifying radio button '%s' has no selection." % group_name)
        try:
            elements = self._get_radio_buttons(group_name)
            actual_value = self._get_value_from_radio_buttons(elements)
        except Exception as e:
            self.driver.report().step(description='Radio Button Should Not Be Selected',
                                      message='Error: ' + str(e),
                                      passed=False,
                                      screenshot=True)
            raise AssertionError
        if actual_value is not None:
            self.driver.report().step(description='Radio Button Should Not Be Selected',
                                      message='Radio button was selected',
                                      passed=False,
                                      screenshot=True)
            raise AssertionError("Radio button group '%s' should not have "
                                 "had selection, but '%s' was selected."
                                 % (group_name, actual_value))
        self.driver.report().step(description='Radio Button Should Not Be Selected',
                                  message='Radio button was not selected',
                                  passed=True,
                                  screenshot=False)

    @keyword
    def select_radio_button(self, group_name, value):
        """Sets the radio button group ``group_name`` to ``value``.

        The radio button to be selected is located by two arguments:
        - ``group_name`` is the name of the radio button group.
        - ``value`` is the ``id`` or ``value`` attribute of the actual
          radio button.

        Examples:
        | `Select Radio Button` | size    | XL    |
        | `Select Radio Button` | contact | email |
        """
        self.info("Selecting '%s' from radio button '%s'."
                  % (value, group_name))
        try:
            element = self._get_radio_button_with_value(group_name, value)
        except Exception as e:
            self.driver.report().step(description='Select Radio Button',
                                      message='Error: ' + str(e),
                                      passed=False,
                                      screenshot=True)
            raise AssertionError
        if not element.is_selected():
            element.click()
        self.driver.report().step(description='Select Radio Button',
                                  message='Selected radio button',
                                  passed=True,
                                  screenshot=False)
    @keyword
    def choose_file(self, locator, file_path):
        """Inputs the ``file_path`` into the file input field ``locator``.

        This keyword is most often used to input files into upload forms.
        The keyword does not check ``file_path`` is the file or folder
        available on the machine where tests are executed. If the ``file_path``
        points at a file and when using Selenium Grid, Selenium will
        [https://seleniumhq.github.io/selenium/docs/api/py/webdriver_remote/selenium.webdriver.remote.command.html?highlight=upload#selenium.webdriver.remote.command.Command.UPLOAD_FILE|magically],
        transfer the file from the machine where the tests are executed
        to the Selenium Grid node where the browser is running.
        Then Selenium will send the file path, from the nodes file
        system, to the browser.

        That ``file_path`` is not checked, is new in SeleniumLibrary 4.0.

        Example:
        | `Choose File` | my_upload_field | ${CURDIR}/trades.csv |
        """
        self.ctx._running_keyword = 'choose_file'
        try:
            self.info('Sending %s to browser.' % os.path.abspath(file_path))
            self.find_element(locator).send_keys(file_path)
            self.driver.report().step(description='Choose File',
                                      message='Uploaded file',
                                      passed=True,
                                      screenshot=False)
            raise AssertionError
        except Exception as e:
            self.driver.report().step(description='Choose File',
                                      message='Error: ' + str(e),
                                      passed=False,
                                      screenshot=True)
            raise AssertionError
        finally:
            self.ctx._running_keyword = None

    @keyword
    def input_password(self, locator, password, clear=True):
        """Types the given password into the text field identified by ``locator``.

        See the `Locating elements` section for details about the locator
        syntax. See `Input Text` for ``clear`` argument details.

        Difference compared to `Input Text` is that this keyword does not
        log the given password on the INFO level. Notice that if you use
        the keyword like

        | Input Password | password_field | password |

        the password is shown as a normal keyword argument. A way to avoid
        that is using variables like

        | Input Password | password_field | ${PASSWORD} |

        Please notice that Robot Framework logs all arguments using
        the TRACE level and tests must not be executed using level below
        DEBUG if the password should not be logged in any format.

        The `clear` argument is new in SeleniumLibrary 4.0. Hiding password
        logging from Selenium logs is new in SeleniumLibrary 4.2.
        """
        try:
            self.info("Typing password into text field '%s'." % locator)
            self._input_text_into_text_field(locator, password, clear, disable_log=True)
            self.driver.report().step(description='Input Password',
                                      message='Inputted password',
                                      passed=True,
                                      screenshot=False)
        except Exception as e:
            self.driver.report().step(description='Input Password',
                                      message='Error: ' + str(e),
                                      passed=False,
                                      screenshot=True)
            raise AssertionError

    @keyword
    def input_text(self, locator, text, clear=True):
        """Types the given ``text`` into the text field identified by ``locator``.

        When ``clear`` is true, the input element is cleared before
        the text is typed into the element. When false, the previous text
        is not cleared from the element. Use `Input Password` if you
        do not want the given ``text`` to be logged.

        If [https://github.com/SeleniumHQ/selenium/wiki/Grid2|Selenium Grid]
        is used and the ``text`` argument points to a file in the file system,
        then this keyword prevents the Selenium to transfer the file to the
        Selenium Grid hub. Instead, this keyword will send the ``text`` string
        as is to the element. If a file should be transferred to the hub and
        upload should be performed, please use `Choose File` keyword.

        See the `Locating elements` section for details about the locator
        syntax. See the `Boolean arguments` section how Boolean values are
        handled.

        Disabling the file upload the Selenium Grid node and the `clear`
        argument are new in SeleniumLibrary 4.0
        """
        try:
            self.info("Typing text '%s' into text field '%s'." % (text, locator))
            self._input_text_into_text_field(locator, text, clear)
            self.driver.report().step(description='Input Text',
                                      message='Inputted text into field',
                                      passed=True,
                                      screenshot=False)
        except Exception as e:
            self.driver.report().step(description='Input Text',
                                      message='Error: ' + str(e),
                                      passed=False,
                                      screenshot=True)
            raise AssertionError

    @keyword
    def page_should_contain_textfield(self, locator, message=None, loglevel='TRACE'):
        """Verifies text field ``locator`` is found from current page.

        See `Page Should Contain Element` for an explanation about ``message``
        and ``loglevel`` arguments.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        try:
            self.assert_page_contains(locator, 'text field', message, loglevel)
            self.driver.report().step(description='Page Should Contain Textfield',
                                      message='Page contains textfield',
                                      passed=True,
                                      screenshot=False)
        except Exception as e:
            self.driver.report().step(description='Page Should Contain Textfield',
                                      message='Error: ' + str(e),
                                      passed=False,
                                      screenshot=True)
            raise AssertionError

    @keyword
    def page_should_not_contain_textfield(self, locator, message=None, loglevel='TRACE'):
        """Verifies text field ``locator`` is not found from current page.

        See `Page Should Contain Element` for an explanation about ``message``
        and ``loglevel`` arguments.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        try:
            self.assert_page_not_contains(locator, 'text field', message, loglevel)
            self.driver.report().step(description='Page Should Not Contain Textfield',
                                      message='Page does not contain textfield',
                                      passed=True,
                                      screenshot=False)
        except Exception as e:
            self.driver.report().step(description='Page Should Not Contain Textfield',
                                      message='Error: ' + str(e),
                                      passed=False,
                                      screenshot=True)
            raise AssertionError

    @keyword
    def textfield_should_contain(self, locator, expected, message=None):
        """Verifies text field ``locator`` contains text ``expected``.

        ``message`` can be used to override the default error message.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        actual = None
        try:
            actual = self._get_value(locator, 'text field')
        except Exception as e:
            self.driver.report().step(description='Textfield Should Contain',
                                      message='Error: ' + str(e),
                                      passed=False,
                                      screenshot=True)
            raise AssertionError
        if expected not in actual:
            if is_noney(message):
                message = "Text field '%s' should have contained text '%s' "\
                          "but it contained '%s'." % (locator, expected, actual)
            self.driver.report().step(description='Textfield Should Contain',
                                      message='Textfield does not contain expected',
                                      passed=False,
                                      screenshot=True)
            raise AssertionError(message)
        self.info("Text field '%s' contains text '%s'." % (locator, expected))
        self.driver.report().step(description='Textfield Should Contain',
                                  message='Textfield contains expected',
                                  passed=True,
                                  screenshot=False)

    @keyword
    def textfield_value_should_be(self, locator, expected, message=None):
        """Verifies text field ``locator`` has exactly text ``expected``.

        ``message`` can be used to override default error message.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        try:
            actual = self._get_value(locator, 'text field')
        except Exception as e:
            self.driver.report().step(description='Textfield Value Should Be',
                                      message='Error: ' + str(e),
                                      passed=False,
                                      screenshot=True)
            raise AssertionError
        if actual != expected:
            if is_noney(message):
                message = "Value of text field '%s' should have been '%s' "\
                          "but was '%s'." % (locator, expected, actual)
            self.driver.report().step(description='Textfield Value Should Be',
                                      message='Textfield value not as expected',
                                      passed=False,
                                      screenshot=True)
            raise AssertionError(message)
        self.info("Content of text field '%s' is '%s'." % (locator, expected))
        self.driver.report().step(description='Textfield Value Should Be',
                                  message='Textfield value equal to expected',
                                  passed=True,
                                  screenshot=False)

    @keyword
    def textarea_should_contain(self, locator, expected, message=None):
        """Verifies text area ``locator`` contains text ``expected``.

        ``message`` can be used to override default error message.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        actual = None
        try:
            actual = self._get_value(locator, 'text area')
        except Exception as e:
            self.driver.report().step(description='Textarea Should Contain',
                                      message='Error: ' + str(e),
                                      passed=False,
                                      screenshot=True)
            raise AssertionError
        if expected not in actual:
            if is_noney(message):
                message = "Text area '%s' should have contained text '%s' " \
                          "but it had '%s'." % (locator, expected, actual)
            self.driver.report().step(description='Textarea Should Contain',
                                      message='Textare did not contain expected text',
                                      passed=False,
                                      screenshot=True)
            raise AssertionError(message)
        self.info("Text area '%s' contains text '%s'." % (locator, expected))
        self.driver.report().step(description='Textarea Should Contain',
                                  message='Textarea contains expected text',
                                  passed=True,
                                  screenshot=False)

    @keyword
    def textarea_value_should_be(self, locator, expected, message=None):
        """Verifies text area ``locator`` has exactly text ``expected``.

        ``message`` can be used to override default error message.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        actual = None
        try:
            actual = self._get_value(locator, 'text area')
        except Exception as e:
            self.driver.report().step(description='Textarea Value Should Be',
                                      message='Error: ' + str(e),
                                      passed=False,
                                      screenshot=True)
            raise AssertionError
        if expected != actual:
            if is_noney(message):
                message = "Text area '%s' should have had text '%s' " \
                          "but it had '%s'." % (locator, expected, actual)
            self.driver.report().step(description='Textarea Value Should Be', message='Textarea value does not match expected',
                                      passed=False,
                                      screenshot=True)
            raise AssertionError(message)
        self.info("Content of text area '%s' is '%s'." % (locator, expected))
        self.driver.report().step(description='Textarea Value Should Be', message='Textarea value matches expected',
                                  passed=True,
                                  screenshot=False)

    @keyword
    def page_should_contain_button(self, locator, message=None, loglevel='TRACE'):
        """Verifies button ``locator`` is found from current page.

        See `Page Should Contain Element` for an explanation about ``message``
        and ``loglevel`` arguments.

        See the `Locating elements` section for details about the locator
        syntax. When using the default locator strategy, buttons are
        searched using ``id``, ``name``, and ``value``.
        """
        try:
            self.assert_page_contains(locator, 'input', message, loglevel)
            self.driver.report().step(description='Page Should Contain Button', message='Page should contain button',
                                      passed=True,
                                      screenshot=False)
        except AssertionError:
            self.assert_page_contains(locator, 'button', message, loglevel)
            self.driver.report().step(description='Page Should Contain Button', message='Page should contain button',
                                      passed=True,
                                      screenshot=False)
            return
        self.driver.report().step(description='Page Should Contain Button', message='Page does not contain button at locator',
                                  passed=False,
                                  screenshot=True)
        raise AssertionError

    @keyword
    def page_should_not_contain_button(self, locator, message=None, loglevel='TRACE'):
        """Verifies button ``locator`` is not found from current page.

        See `Page Should Contain Element` for an explanation about ``message``
        and ``loglevel`` arguments.

        See the `Locating elements` section for details about the locator
        syntax. When using the default locator strategy, buttons are
        searched using ``id``, ``name``, and ``value``.
        """
        try:
            self.assert_page_not_contains(locator, 'button', message, loglevel)
            self.assert_page_not_contains(locator, 'input', message, loglevel)
            self.driver.report().step(description='Page Should Not Contain Button', message='Page does not contain button', passed=True, screenshot=False)
        except Exception as e:
            self.driver.report().step(description='Page Should Not Contain Button', message='Page contains button. Error: ' + str(e), passed=False, screenshot=True)
            raise AssertionError

    def _get_value(self, locator, tag):
        return self.find_element(locator, tag).get_attribute('value')

    def _get_checkbox(self, locator):
        return self.find_element(locator, tag='checkbox')

    def _get_radio_buttons(self, group_name):
        xpath = "xpath://input[@type='radio' and @name='%s']" % group_name
        self.debug('Radio group locator: ' + xpath)
        elements = self.find_elements(xpath)
        if not elements:
            raise ElementNotFound("No radio button with name '%s' found."
                                  % group_name)
        return elements

    def _get_radio_button_with_value(self, group_name, value):
        xpath = "xpath://input[@type='radio' and @name='%s' and " \
                "(@value='%s' or @id='%s')]" % (group_name, value, value)
        self.debug('Radio group locator: ' + xpath)
        try:
            return self.find_element(xpath)
        except ElementNotFound:
            raise ElementNotFound("No radio button with name '%s' and "
                                  "value '%s' found." % (group_name, value))

    def _get_value_from_radio_buttons(self, elements):
        for element in elements:
            if element.is_selected():
                return element.get_attribute('value')
        return None

    def _input_text_into_text_field(self, locator, text, clear=True, disable_log=False):
        element = self.find_element(locator)
        if is_truthy(clear):
            element.clear()
        if disable_log:
            self.info('Temporally setting log level to: NONE')
            previous_level = BuiltIn().set_log_level('NONE')
        try:
            element.send_keys(text)
        finally:
            if disable_log:
                BuiltIn().set_log_level(previous_level)
