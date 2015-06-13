from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient
from rest_framework import status

from wallfly.models import *

class PropertyTestCases(TestCase):
    """ Tests associated with the Property model """

    factory = APIRequestFactory()
    client = APIClient()

    def setUp(self):
        u = User.objects.create(username="test", password="tom")
        
        agent = Agent.objects.create(contact_num="1234567890",
                                     real_estate="testRS",
                                     email="test@test.com")
        wfUser = WFUser.objects.create(user=u,
                                       user_level=1,
                                       agent_id=agent
        )
        prop = Property.objects.create(address='12 Test Ave, TestVille',
                                       status=1,
                                       agent_id=agent)
        
        self.propOther = Property.objects.create(address='13 Test Ave, TestVille',
                                       status=1)

    def test_01_get_prop(self):
        """ Test that a property can be returned"""
        
        c = APIClient()
        user = User.objects.get(username="test")
        tok = Token.objects.get(user=user)
        c.login(username="test", password="test")
        c.credentials(HTTP_AUTHORIZATION="Token " + tok.key)
        response = c.get("/property/1")
        name = "12 Test Ave, TestVille"

        self.assertEqual(response.data["address"], name)

    def test_02_nonexistant_retreive(self):
        """ Test that the correct error is returned when an invalid property is retrieved """

        c = APIClient()
        user = User.objects.get(username="test")
        tok = Token.objects.get(user=user)
        c.login(username="test", password="test")
        c.credentials(HTTP_AUTHORIZATION="Token " + tok.key)

        response = c.get("/property/23")
        self.assertEqual(response.data["detail"], "Not found.")
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_03_creation_with_duplicate_details(self):
        """ Test the creation of a property with a duplicate address"""
        
        c = APIClient()
        user = User.objects.get(username="test")
        tok = Token.objects.get(user=user)
        c.login(username="test", password="test")
        c.credentials(HTTP_AUTHORIZATION="Token " + tok.key)

        response = c.post("/property/", {"status": "1",
                                         "name": "test",
                                         "address": "12 Test Ave, TestVille"})

        self.assertEqual(response.data["address"], [u'This field must be unique.'])
        
    def test_04_creation_with_null_values(self):
        """ Test the creation of a property with null values for the inputs"""
        c = APIClient()
        user = User.objects.get(username="test")
        tok = Token.objects.get(user=user)
        c.login(username="test", password="test")
        c.credentials(HTTP_AUTHORIZATION="Token " + tok.key)

        response = c.post("/property/", {"address": "",
                                         "status": "",
                                         "name": ""}) 

        self.assertEqual(response.data, {'status': [u'A valid integer is required.'], 'name': [u'This field may not be blank.'], 'address': [u'This field may not be blank.']})

    def test_05_create_a_new_property(self):
        """Test that a new property can be created"""
        c = APIClient()
        user = User.objects.get(username="test")
        tok = Token.objects.get(user=user)
        c.login(username="test", password="test")
        c.credentials(HTTP_AUTHORIZATION="Token " + tok.key)

        response = c.post("/property/", {"status": "1",
                                         "name": "Test Creation",
                                         "address": "12 Unit-test Ave, TestVille"})
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_06_edit_property_name(self):
        """ Test that a property name can be edited"""
        c = APIClient()
        user = User.objects.get(username="test")
        tok = Token.objects.get(user=user)
        c.login(username="test", password="test")
        c.credentials(HTTP_AUTHORIZATION="Token " + tok.key)

        response = c.put("/property/1", {"name": "New Name"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_07_edit_property_dupliate_details(self):
        """ Test that a property cannot be changed to have a duplicate name"""
        c = APIClient()
        user = User.objects.get(username="test")
        tok = Token.objects.get(user=user)
        c.login(username="test", password="test")
        c.credentials(HTTP_AUTHORIZATION="Token " + tok.key)

        response = c.put("/property/1", {"name": "New Name"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_08_delete_property(self):
        """ Test that a property can be deleted """
        c = APIClient()
        user = User.objects.get(username="test")
        tok = Token.objects.get(user=user)
        c.login(username="test", password="test")
        c.credentials(HTTP_AUTHORIZATION="Token " + tok.key)

        response = c.delete("/property/2")

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        
    def test_09_delete_property_nonexistent(self):
        """ Test that a property that doesn't not exist cannoted be deleted """
        c = APIClient()
        user = User.objects.get(username="test")
        tok = Token.objects.get(user=user)
        c.login(username="test", password="test")
        c.credentials(HTTP_AUTHORIZATION="Token " + tok.key)
        
        response = c.delete("/property/23")

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_10_get_property_invalid_permission(self):
        """ Test attempting to access a property the user doesn't have access 
            to due to invalid permissions 
        """

        c = APIClient()
        user = User.objects.get(username="test")
        tok = Token.objects.get(user=user)
        c.login(username="test", password="test")
        c.credentials(HTTP_AUTHORIZATION="Token " + tok.key)
        response = c.get("/property/" + str(self.propOther.id))

        self.assertEquals(response.data, {"detail":"You do not have permission to perform this action."})
        
class ZIssueTests(TestCase):
    """ Tests associated with the Issue model"""
    
    def setUp(self):
        u = User.objects.create(username="test", password="test")
        
        agent = Agent.objects.create(contact_num="1234567890",
                                     real_estate="testRS",
                                     email="test@test.com")
        wfUser = WFUser.objects.create(user=u,
                                       user_level=1,
                                       agent_id=agent
        )
        prop = Property.objects.create(address='12 Test Ave, TestVille',
                                       status=1,
                                       agent_id=agent)
    
        i = Issue.objects.create(severity=1,
                                 description="Initial issue",
                                 property_id=prop)
        self.c = APIClient()
        user = User.objects.get(username="test")
        tok = Token.objects.get(user=user)
        self.c.login(username="test", password="test")
        self.c.credentials(HTTP_AUTHORIZATION="Token " + tok.key)

    def test_01_create_new_issue(self):
        """ Test that issues are created """
        p = Property.objects.all()
        response = self.c.post("/issue/" + str(p[0].id), {"severity": "1",
                                                          "description": "This is a test issue",
                                                          "property_id": str(p[0].id)})

        # Ensure that the issue is in the returned json object
        self.assertEquals(response.data["description"], "This is a test issue")

    def test_02_create_invalid_issue(self):
        """ Test that invalid issues cannot be created, in this case with insufficient information """ 
        p = Property.objects.all()
        response = self.c.post("/issue/" + str(p[0].id), {"severity": ""})
        self.assertEquals(response.data,
                          {"severity": ["A valid integer is required."]})

    def test_03_create_issue_on_invalid_property(self):
        """ Test that invalid issues cannot be created, in this case with an invalid property id"""
        response = self.c.post("/issue/32", {"severity": "1",
                                             "description": "Invalid",
                                             "property_id": "32"})
        self.assertEqual(response.data["detail"], "Not found.")

    def test_04_resolve_issue(self):
        """ Test that an issue can be resolved"""
        i = Issue.objects.all()[0]
        response = self.c.put("/issue/" + str(i.id), {"resolved": "1"})
        self.assertEqual(response.data["resolved"], 1)


    def test_05_resolve_issue_check_prop_status(self):
        """ Test that the property status of a property is altered when an issue is resolved"""
        p = Property.objects.all()

        response = self.c.post("/issue/" + str(p[0].id), {"severity": "3",
                                                          "description": "This is a severe test issue",
                                                          "property_id": str(p[0].id)})
        
        self.assertEqual(p[0].status, 3)

    def test_06_retrieve_issues_for_property(self):
        """ Test ensures that a list of issues is returned for a property """

        p = Property.objects.all()
        self.c.post("/issue/" + str(p[0].id), {"severity": "3",
                                               "description": "This is a severe test issue",
                                               "property_id": str(p[0].id)})
        self.c.post("/issue/" + str(p[0].id), {"severity": "3",
                                               "description": "This is a severe test issue",
                                               "property_id": str(p[0].id)})
        response = self.c.get("/issues/" + str(p[0].id))

        self.assertEquals(len(response.data), 3)
        self.assertEquals(p[0].status, 3)

    def test_07_retrieve_issues_for_property(self):
        """ Test that issues cann't be retrieved from a non existent property"""
        response = self.c.get("/issues/666")
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_08_delete_an_issue(self):
        """ Ensure that tests can be deleted after creation"""
        p = Property.objects.all()
        i = Issue.objects.filter(property_id=p)

        self.c.post("/issue/" + str(p[0].id), {"severity": "3",
                                               "description": "This is a severe test issue",
                                               "property_id": str(p[0].id)})
        self.assertEquals(len(i), 2)
        i = Issue.objects.filter(property_id=p)

        self.c.delete("/issue/" + str(i[1].id))

        i = Issue.objects.filter(property_id=p)
        self.assertEquals(len(i), 1)
    
    def test_09_delete_nonexistant_issue(self):
        """ Ensure that deleting issues catches invalid parameters"""
        # 222 is a non-existant issue id
        response = self.c.delete("/issue/222")
        self.assertEqual(response.data["detail"], "Not found.")


class XAuthTests(TestCase):
    """ Rudimentary tests of the authorization system """
    
    def setUp(self):
        self.u = User.objects.create(username="test", password="tom")
        
        agent = Agent.objects.create(contact_num="1234567890",
                                     real_estate="testRS",
                                     email="test@test.com")
        wfUser = WFUser.objects.create(user=self.u,
                                       user_level=1,
                                       agent_id=agent
        )

        self.c = APIClient()
        user = User.objects.get(username="test")
        tok = Token.objects.get(user=user)
        self.c.login(username="test", password="test")
        self.c.credentials(HTTP_AUTHORIZATION="Token " + tok.key)

    def test_01_get_user_details(self):
        """ Test that a user's details can be retrieved """
        new = User.objects.create(username="tester", password="testpass")
        new.save()
        response = self.c.get("/auth/", {
            "username": self.u.username,
            "password": self.u.password})

        tok = Token.objects.get(user=self.u)
        
        self.assertEqual(response.data["user"], "test")
        self.assertEqual(response.data["level"], 1)
        self.assertEqual(response.data["auth"], str(tok))

    def test_02_get_invalid_user(self):
        self.c.logout()
        response = self.c.get("/auth/", {
            "username": "invalid",
            "password": "youshallnotpass"
        })

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class Y_UserTests(TestCase):
    """ Tests for getting user details, including properties"""

    def setUp(self):
        u = User.objects.create(username="test", password="tom")
        o = User.objects.create(username="owner", password="owner")
        t = User.objects.create(username="tenant", password="tenant")

        agent = Agent.objects.create(contact_num="1234567890",
                                     real_estate="testRS",
                                     email="test@test.com")
        owner = Owner.objects.create(contact_number="1234567890",
                                     owner_name="Jerry Test",
                                     address="12 Owner Cr, OwnerVille",
                                     email="jerry@propertymogul.com",
                                     num_properties=100)
        tenant = Tenant.objects.create(email="tenant@rs.com")

        wfOwner = WFUser.objects.create(user=o,
                                        user_level=2,
                                        owner_id=owner)

        wfUser = WFUser.objects.create(user=u,
                                       user_level=1,
                                       agent_id=agent)

        
        prop = Property.objects.create(address='12 Test Ave, TestVille',
                                       status=1,
                                       agent_id=agent,
                                       owner_id=owner)


        wfTenant = WFUser.objects.create(user=t,
                                         user_level=3,
                                         tenant_id=tenant)
                                         

        self.c = APIClient()
        user = User.objects.get(username="test")
        tok = Token.objects.get(user=user)
        self.c.login(username="test", password="tom")
        self.c.credentials(HTTP_AUTHORIZATION="Token " + tok.key)

    def test_01_get_user_detail(self):
        """ Test getting a users Wallfly details eg. Properties"""
        # test the default admin agent
        u = User.objects.get(username="test")
        wfUser = WFUser.objects.get(user=u)
        response = self.c.get("/user/" + str(wfUser.id))

        self.assertEquals(response.data["user"]["username"], str(wfUser.user.username))
        
        # login and test the owner level object
        
        user = User.objects.get(username="owner")
        tok = Token.objects.get(user=user)
        self.c.login(username=user.username, password=user.password)
        self.c.credentials(HTTP_AUTHORIZATION="Token " + tok.key)
        wfOwner = WFUser.objects.get(user=user)
        
        response = self.c.get("/user/" + str(wfOwner.id))
        self.assertEquals(response.data["user"]["username"], str(wfOwner.user.username))

        # login and test the tenant level object
        p = Property.objects.all()
        user = User.objects.get(username="tenant")
        tok = Token.objects.get(user=user)
        self.c.login(username=user.username, password=user.password)
        self.c.credentials(HTTP_AUTHORIZATION="Token " + tok.key)
        ten = WFUser.objects.get(user=user)

        response = self.c.get("/user/" + str(ten.id))
        self.assertEquals(response.data["user"]["username"], str(ten.user.username))

    def test_02_get_invalid_user_details(self):

        """ Ensure that an invalid user login returns a 404"""

        response = self.c.get("/user/666")
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
        
