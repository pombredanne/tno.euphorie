from tno.euphorie import testing

class CompanyBrowserTests(testing.TnoEuphorieFunctionalTestCase):
    BASE_URL = "http://nohost/plone/client/nl?language=nl-NL"

    def createSurvey(self):
        from euphorie.content.tests.utils import BASIC_SURVEY
        from euphorie.client.tests.utils import addSurvey
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)

    def startSurveySession(self):
        from Products.Five.testbrowser import Browser
        browser=Browser()
        browser.open(self.BASE_URL)
        # Register a new user
        testing.registerUserInClient(browser)
        # Create a new survey session
        browser.getControl(name="title:utf8:ustring").value="Test session"
        browser.getControl(name="next", index=1).click()
        # Start the survey
        browser.getForm().submit()
        return browser

    def testDutchCompanyFormUsed(self):
        self.createSurvey()
        browser=self.startSurveySession()
        # Jump to the report phase
        browser.getLink("Rapport").click()
        browser.getControl(name="next").click()
        # We should now be at the company form
        self.assertEqual(browser.url,
                "http://nohost/plone/client/nl/ict/software-development/report/company")
        self.assertTrue("Bezoekadres bedrijf" in browser.contents)

    def testDutchCompanyReportViewUsed(self):
        self.createSurvey()
        browser=self.startSurveySession()
        browser.open("http://nohost/plone/client/nl/ict/software-development/report/view")
        self.assertTrue("Bezoekadres bedrijf" in browser.contents)

    def testDutchCompanyReportDownloadUsed(self):
        self.createSurvey()
        browser=self.startSurveySession()
        browser.handleErrors=False
        browser.open("http://nohost/plone/client/nl/ict/software-development/report/download")
        self.assertTrue("Bezoekadres bedrijf" in browser.contents)

    def testDecimalAbsenteePercentage(self):
        self.createSurvey()
        browser=self.startSurveySession()
        browser.open("http://nohost/plone/client/nl/ict/software-development/report/company")
        browser.getControl(name="absentee_percentage").value="50,1"
        browser.getControl(name="next", index=1).click()
        self.assertEqual(browser.url,
                "http://nohost/plone/client/nl/ict/software-development/report/view")

    def testDecimalAbsenteePercentage_EnglishNotation(self):
        self.createSurvey()
        browser=self.startSurveySession()
        browser.open("http://nohost/plone/client/nl/ict/software-development/report/company")
        browser.getControl(name="absentee_percentage").value="40.1"
        browser.getControl(name="next", index=1).click()
        self.assertEqual(browser.url,
                "http://nohost/plone/client/nl/ict/software-development/report/view")

    def testInvalidAbsenteePercentageGetsErrorMessage(self):
        self.createSurvey()
        browser=self.startSurveySession()
        browser.open("http://nohost/plone/client/nl/ict/software-development/report/company")
        browser.getControl(name="absentee_percentage").value="4.0.1"
        browser.getControl(name="next", index=1).click()
        self.assertTrue("Vul een percentage in" in browser.contents)
