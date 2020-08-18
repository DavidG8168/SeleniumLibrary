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

from selenium.webdriver.support.ui import Select

from TestProjectSeleniumLibrary.base import LibraryComponent, keyword
from TestProjectSeleniumLibrary.utils import is_truthy, plural_or_not as s


class SelectElementKeywords(LibraryComponent):

    @keyword
    def get_list_items(self, locator, values=False):
        """Returns all labels or values of selection list ``locator``.

        See the `Locating elements` section for details about the locator
        syntax.

        Returns visible labels by default, but values can be returned by
        setting the ``values`` argument to a true value (see `Boolean
        arguments`).

        Example:
        | ${labels} = | `Get List Items` | mylist              |             |
        | ${values} = | `Get List Items` | css:#example select | values=True |

        Support to return values is new in SeleniumLibrary 3.0.
        """
        try:
            options = self._get_options(locator)
            if is_truthy(values):
                self.driver.report().step(description="Get List Items values of" + locator,
                                          message="Got list items values succsefully ", passed=True,
                                          screenshot=False)
                return self._get_values(options)
            else:
                self.driver.report().step(description="Get List Items labels of" + locator,
                                          message="Got list items labels succsefully ", passed=True,
                                          screenshot=False)
                return self._get_labels(options)
        except Exception as e:
            self.driver.report().step(description='Failed to get list items of ' + locator,
                                      message='Could not get list items. Error: ' + str(e), passed=False,
                                      screenshot=True)
            raise AssertionError



    @keyword
    def get_selected_list_label(self, locator):
        """Returns the label of selected option from selection list ``locator``.

        If there are multiple selected options, the label of the first option
        is returned.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        select = self._get_select_list(locator)
        self.driver.report().step(description="Get selected list label of " + locator,
                                  message="Got the selected list label", passed=True,
                                  screenshot=False)
        return select.first_selected_option.text

    @keyword
    def get_selected_list_labels(self, locator):
        """Returns labels of selected options from selection list ``locator``.

        Starting from SeleniumLibrary 3.0, returns an empty list if there
        are no selections. In earlier versions, this caused an error.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        try:
            options = self._get_selected_options(locator)
            self.driver.report().step(description="Get selected list labels of " + locator,
                                      message="Got the selected list labels", passed=True,
                                      screenshot=False)
            return self._get_labels(options)
        except Exception as e:
            self.driver.report().step(description="Get selected list value of " + locator,
                                      message='Could not get list item value. Error: ' + str(e), passed=False,
                                      screenshot=True)
            raise AssertionError

    @keyword
    def get_selected_list_value(self, locator):
        """Returns the value of selected option from selection list ``locator``.

        If there are multiple selected options, the value of the first option
        is returned.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        try:
            select = self._get_select_list(locator)
            self.driver.report().step(description="Get selected list value of " + locator,
                                      message="Got the selected list value", passed=True,
                                      screenshot=False)
            return select.first_selected_option.get_attribute('value')
        except Exception as e:
            self.driver.report().step(description="Get selected list value of " + locator,
                                      message='Could not get list item value. Error: ' + str(e), passed=False,
                                      screenshot=True)
            raise AssertionError

    @keyword
    def get_selected_list_values(self, locator):
        """Returns values of selected options from selection list ``locator``.

        Starting from SeleniumLibrary 3.0, returns an empty list if there
        are no selections. In earlier versions, this caused an error.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        try:
            self.driver.report().step(description="Get selected list value of " + locator,
                                      message="Got the selected list value", passed=True,
                                      screenshot=False)
            options = self._get_selected_options(locator)
            return self._get_values(options)
        except Exception as e:
            self.driver.report().step(description="Get selected option list value of " + locator,
                                      message='Could not get list item option. Error: ' + str(e), passed=False,
                                      screenshot=True)
            raise AssertionError

    @keyword
    def list_selection_should_be(self, locator, *expected):
        """Verifies selection list ``locator`` has ``expected`` options selected.

        It is possible to give expected options both as visible labels and
        as values. Starting from SeleniumLibrary 3.0, mixing labels and
        values is not possible. Order of the selected options is not
        validated.

        If no expected options are given, validates that the list has
        no selections. A more explicit alternative is using `List Should
        Have No Selections`.

        See the `Locating elements` section for details about the locator
        syntax.

        Examples:
        | `List Selection Should Be` | gender    | Female          |        |
        | `List Selection Should Be` | interests | Test Automation | Python |
        """
        self.info("Verifying list '%s' has option%s [ %s ] selected."
                  % (locator, s(expected), ' | '.join(expected)))
        self.page_should_contain_list(locator)
        options = self._get_selected_options(locator)
        labels = self._get_labels(options)
        values = self._get_values(options)
        if sorted(expected) not in [sorted(labels), sorted(values)]:
            self.driver.report().step(description="Verify if list has options selected",
                                      message="List '%s' should have had selection [ %s ] "
                                              "but selection was [ %s ]."
                                 % (locator, ' | '.join(expected),self._format_selection(labels, values)),
                                      passed=False,
                                      screenshot=True)
            raise AssertionError("List '%s' should have had selection [ %s ] "
                                 "but selection was [ %s ]."
                                 % (locator, ' | '.join(expected),
                                    self._format_selection(labels, values)))

    def _format_selection(self, labels, values):
        return ' | '.join('%s (%s)' % (label, value)
                          for label, value in zip(labels, values))

    @keyword
    def list_should_have_no_selections(self, locator):
        """Verifies selection list ``locator`` has no options selected.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        self.info("Verifying list '%s' has no selections." % locator)
        options = self._get_selected_options(locator)
        if options:
            selection = self._format_selection(self._get_labels(options),
                                               self._get_values(options))
            raise AssertionError("List '%s' should have had no selection "
                                 "but selection was [ %s ]."
                                 % (locator, selection))

    @keyword
    def page_should_contain_list(self, locator, message=None, loglevel='TRACE'):
        """Verifies selection list ``locator`` is found from current page.

        See `Page Should Contain Element` for an explanation about ``message``
        and ``loglevel`` arguments.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        try:

            self.assert_page_contains(locator, 'list', message, loglevel)
            self.driver.report().step(description="Page should contain list at locator " + locator,
                                      message="The page does contain the list", passed=True,
                                      screenshot=False)
        except Exception as e:
            self.driver.report().step(description="Page should contain list at locator " + locator,
                                      message='List was not found in page. Error: ' + str(e), passed=False,
                                      screenshot=True)
            raise AssertionError

    @keyword
    def page_should_not_contain_list(self, locator, message=None, loglevel='TRACE'):
        """Verifies selection list ``locator`` is not found from current page.

        See `Page Should Contain Element` for an explanation about ``message``
        and ``loglevel`` arguments.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        try:
            self.assert_page_not_contains(locator, 'list', message, loglevel)
            self.driver.report().step(description="Page should not contain list at locator " + locator,
                                      message="The page does not contain the list", passed=True,
                                      screenshot=False)
        except Exception as e:
            self.driver.report().step(description="Page should not contain list at locator " + locator,
                                      message='List was found in page. Error: ' + str(e), passed=False,
                                      screenshot=True)
            raise AssertionError

    @keyword
    def select_all_from_list(self, locator):
        """Selects all options from multi-selection list ``locator``.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        self.info("Selecting all options from list '%s'." % locator)
        select = self._get_select_list(locator)
        if not select.is_multiple:
            self.driver.report().step(description="Select all from list at locator" + locator,
                                      message="'Select All From List' works only with multi-selection lists.",
                                      passed=False,
                                      screenshot=True)
            raise RuntimeError("'Select All From List' works only with "
                               "multi-selection lists.")
        for i in range(len(select.options)):
            select.select_by_index(i)

    @keyword
    def select_from_list_by_index(self, locator, *indexes):
        """Selects options from selection list ``locator`` by ``indexes``.

        Indexes of list options start from 0.

        If more than one option is given for a single-selection list,
        the last value will be selected. With multi-selection lists all
        specified options are selected, but possible old selections are
        not cleared.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        if not indexes:
            self.driver.report().step(description="Select all from list at locator" + locator,
                                      message="No indexes given.",
                                      passed=False,
                                      screenshot=True)
            raise ValueError("No indexes given.")
        self.info("Selecting options from selection list '%s' by index%s %s."
                  % (locator, '' if len(indexes) == 1 else 'es',
                     ', '.join(indexes)))
        select = self._get_select_list(locator)
        for index in indexes:
            select.select_by_index(int(index))

    @keyword
    def select_from_list_by_value(self, locator, *values):
        """Selects options from selection list ``locator`` by ``values``.

        If more than one option is given for a single-selection list,
        the last value will be selected. With multi-selection lists all
        specified options are selected, but possible old selections are
        not cleared.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        if not values:
            self.driver.report().step(description="Select from list by value at locator " + locator,
                                      message='No values given.', passed=False,
                                      screenshot=True)
            raise ValueError("No values given.")
        self.info("Selecting options from selection list '%s' by value%s %s."
                  % (locator, s(values), ', '.join(values)))
        select = self._get_select_list(locator)
        for value in values:
            select.select_by_value(value)

    @keyword
    def select_from_list_by_label(self, locator, *labels):
        """Selects options from selection list ``locator`` by ``labels``.

        If more than one option is given for a single-selection list,
        the last value will be selected. With multi-selection lists all
        specified options are selected, but possible old selections are
        not cleared.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        if not labels:
            self.driver.report().step(description="Select from list by label at locator " + locator,
                                      message='No labels given.', passed=False,
                                      screenshot=True)
            raise ValueError("No labels given.")
        self.info("Selecting options from selection list '%s' by label%s %s."
                  % (locator, s(labels), ', '.join(labels)))
        select = self._get_select_list(locator)
        for label in labels:
            select.select_by_visible_text(label)

    @keyword
    def unselect_all_from_list(self, locator):
        """Unselects all options from multi-selection list ``locator``.

        See the `Locating elements` section for details about the locator
        syntax.

        New in SeleniumLibrary 3.0.
        """
        self.info("Unselecting all options from list '%s'." % locator)
        select = self._get_select_list(locator)
        if not select.is_multiple:
            self.driver.report().step(description="Unselect all at locator " + locator,
                                      message="Un-selecting options works only with multi-selection lists.", passed=False,
                                      screenshot=True)
            raise RuntimeError("Un-selecting options works only with "
                               "multi-selection lists.")
        select.deselect_all()

    @keyword
    def unselect_from_list_by_index(self, locator, *indexes):
        """Unselects options from selection list ``locator`` by ``indexes``.

        Indexes of list options start from 0. This keyword works only with
        multi-selection lists.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        if not indexes:
            self.driver.report().step(description="Unselect frpm list by index at " + locator,
                                      message="No indexes given.",
                                      passed=False,
                                      screenshot=True)
            raise ValueError("No indexes given.")
        self.info("Un-selecting options from selection list '%s' by index%s "
                  "%s." % (locator, '' if len(indexes) == 1 else 'es',
                           ', '.join(indexes)))
        select = self._get_select_list(locator)

        if not select.is_multiple:
            self.driver.report().step(description="Unselect from list by index at " + locator,
                                      message="Un-selecting options works only with multi-selection lists.",
                                      passed=False,
                                      screenshot=True)
            raise RuntimeError("Un-selecting options works only with "
                               "multi-selection lists.")
        for index in indexes:
            select.deselect_by_index(int(index))

    @keyword
    def unselect_from_list_by_value(self, locator, *values):
        """Unselects options from selection list ``locator`` by ``values``.

        This keyword works only with multi-selection lists.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        if not values:
            self.driver.report().step(description="Un select from list by value at locator " + locator,
                                      message='No values given.', passed=False,
                                      screenshot=True)
            raise ValueError("No values given.")
        self.info("Un-selecting options from selection list '%s' by value%s "
                  "%s." % (locator, s(values), ', '.join(values)))
        select = self._get_select_list(locator)
        if not select.is_multiple:
            self.driver.report().step(description="Unselect from list by value at " + locator,
                                      message="Un-selecting options works only with multi-selection lists.",
                                      passed=False,
                                      screenshot=True)
            raise RuntimeError("Un-selecting options works only with "
                               "multi-selection lists.")
        for value in values:
            select.deselect_by_value(value)

    @keyword
    def unselect_from_list_by_label(self, locator, *labels):
        """Unselects options from selection list ``locator`` by ``labels``.

        This keyword works only with multi-selection lists.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        if not labels:
            self.driver.report().step(description="Un select from list by label at locator " + locator,
                                      message='No labels given.', passed=False,
                                      screenshot=True)
            raise ValueError("No labels given.")
        self.info("Un-selecting options from selection list '%s' by label%s "
                  "%s." % (locator, s(labels), ', '.join(labels)))
        select = self._get_select_list(locator)
        if not select.is_multiple:
            self.driver.report().step(description="Unselect from list by label at " + locator,
                                      message="Un-selecting options works only with multi-selection lists.",
                                      passed=False,
                                      screenshot=True)
            raise RuntimeError("Un-selecting options works only with "
                               "multi-selection lists.")
        for label in labels:
            select.deselect_by_visible_text(label)

    def _get_select_list(self, locator):
        try:
            el = self.find_element(locator, tag='list')
            self.driver.report().step(description="Get select list at locator " + locator,
                                      message="List was retrieved sucsesfully", passed=True,
                                      screenshot=False)
            return Select(el)
        except Exception as e:
            self.driver.report().step(description="Get select list at locator " + locator,
                                      message='Could not get select list. Error: ' + str(e), passed=False,
                                      screenshot=True)
            raise AssertionError

    def _get_options(self, locator):
        try:
            self.driver.report().step(description="Get options at locator " + locator,
                                      message="Options list was retrieved sucsesfully", passed=True,
                                      screenshot=False)
            return self._get_select_list(locator).options
        except Exception as e:
            self.driver.report().step(description="Get options at locator " + locator,
                                      message='Could not get options list. Error: ' + str(e), passed=False,
                                      screenshot=True)
            raise AssertionError

    def _get_selected_options(self, locator):
        try:
            self.driver.report().step(description="Get selected options at locator " + locator,
                                      message="selected options list was retrieved sucsesfully", passed=True,
                                      screenshot=False)
            return self._get_select_list(locator).all_selected_options
        except Exception as e:
            self.driver.report().step(description="Get selected options at locator " + locator,
                                      message='Could not get selected options list. Error: ' + str(e), passed=False,
                                      screenshot=True)
            raise AssertionError

    def _get_labels(self, options):
        try:
            self.driver.report().step(description="Get labels at locator " + locator,
                                      message="Labels list was retrieved sucsesfully", passed=True,
                                      screenshot=False)
            return [opt.text for opt in options]
        except Exception as e:
            self.driver.report().step(description="Get labels at locator " + locator,
                                      message='Could not get labels list. Error: ' + str(e), passed=False,
                                      screenshot=True)
            raise AssertionError

    def _get_values(self, options):
        try:
            self.driver.report().step(description="Get values at locator " + locator,
                                      message="Values list was retrieved sucsesfully", passed=True,
                                      screenshot=False)
            return [opt.get_attribute('value') for opt in options]
        except Exception as e:
            self.driver.report().step(description="Get values at locator " + locator,
                                      message='Could not get values list. Error: ' + str(e), passed=False,
                                      screenshot=True)
            raise AssertionError
