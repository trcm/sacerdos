from django.db import models
from django_extensions.db.fields import UUIDField
from django.contrib.auth.models import User
from django_resized import ResizedImageField


# Token auth libraries
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token


# Called after the creation of a new user to create a new Token for authentication
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class Agent(models.Model):
    """
    Agent - Model representing the real estate agents in the database

    Attributes:
     agent_id(uuid)      - unique identifier
     contact_num(string) - contact number
     real_estate(string) - agents real estate
     email(string)       - agents email
    """
    agent_id = UUIDField(auto=True)
    contact_num = models.CharField(max_length=12, null=False)
    real_estate = models.CharField(max_length=100, null=False)
    email = models.EmailField(null=False)

    def __unicode__(self):
        return "%s" % self.email
    
class Owner(models.Model):

    """
    Owner - Model representing a property owner in the database

    Attributes:
    owner_id(uuid) - unique identifier for the owner
    contact_number(string) - current contact number
    address(string) - current address
    email(string) - current email
    num_properties(int) - number of properties
    """

    owner_id = UUIDField(auto=True)
    owner_name = models.CharField(max_length=100, null=False)
    contact_number = models.CharField(max_length=20, null=False)
    address = models.CharField(max_length=200, null=False)
    email = models.EmailField(null=False)
    num_properties = models.IntegerField(default=0)

    def __unicode__(self):
        return "%s" % self.owner_name

class Property(models.Model):

    """
    Property - representation of a property in the database

    Attributes:

     property_id(uuid)           - Property's database id
     Address(string)             - Address of the property
     Status(int)                 - Current status of the property from 1-3 (good-bad)
     owner_id(foreignkey(owner)) - Property's owner
     agent_id(foreignkey(agent)) - Property's agent
     num_tenants(int)            - Number of people living at a property
     name(string)                - Property name
     property_image(image)       - Image of the property
    """

    property_id = UUIDField(auto=True)
    address = models.CharField(unique=True, max_length=200, blank=False, null=False)
    status = models.IntegerField(null=False)
    owner_id = models.ForeignKey(Owner, null=True)
    agent_id = models.ForeignKey(Agent, null=True, related_name='properties')
    num_tenants = models.IntegerField(null=True)
    name = models.CharField(max_length=200)

    # property_image = models.ImageField(null=True)
    property_image = ResizedImageField(size=[500,300], null=True)

    def __unicode__(self):
        return "%s" % (self.name)


class Tenant(models.Model):

    """
    Tenant - model representing a property Tenant in the database

    Attributes:
    tenant_id(uuid)                     - tentant id
    property_id(foreignkey(Properties)) - Property which the tenant is renting
    contact_number(string)              - current contact number
    email(string)                       - tenant email
    previous_address(string)            - previous tenants address
    extra_information(string)           - any extra information regarding the property eg. extra tenant information
    """

    tenant_id = UUIDField(auto=True)
    property_id = models.ForeignKey(Property, null=True)
    contact_number = models.CharField(max_length=20, null=True)
    email = models.EmailField()
    previous_address = models.CharField(max_length=200, null=True)
    extra_information = models.CharField(max_length=200, null=True)

class Issue(models.Model):

    """
    Issue - model representing a property issue

    Attributes:
    issue_id(uuid)                    - issue identifier
    severity(int)                     - severity of issue from 1-3
    description(string)               - description of issue
    image(imagefield)                 - picture of issue
    resolved(int)                     - status of issue resolution from 1 - 3 (1. Not resolved 2. Inprogress 3. Completed)
    property_id(foreignkey(property)) - foreign key to property related to issue
    """

    issue_id    = UUIDField(auto=True)
    severity    = models.IntegerField(default=1)
    description = models.CharField(max_length=1000, null=True)
    image       = ResizedImageField(size=[500,300], null=True)
    resolved    = models.IntegerField(default=0)
    property_id = models.ForeignKey(Property, null=True)

    def __unicode__(self):
        return "%s - %s" % (self.severity, self.description)

class Financial(models.Model):
    """
Financial - Model representing the finanal data for a property
 property-id( foriegnkey(property)) - foreignkey to financial detail of a property
 rent-amount( int) - current amount of property's rent
 day-of-paymen( enum) - day of the week the rent is paid
 payment-type( string) - how the payment is made
 payment-due( datetime) - when the tenants needs to pay
 payment-status(int) - the status of the payment ie up to date, overdue
 bond(int) - amount of the bond
"""
    DAYS = (
        ("Monday", "Mon"),
        ("Tuesday", "Tues"),
        ("Wednesday", "Wed"),
        ("Thursday", "Thurs"),
        ("Friday", "Fri")
    )

    property_id    = models.ForeignKey(Property, null=True)
    rent_amount    = models.IntegerField()
    day_of_payment = models.CharField(max_length=10, choices=DAYS, null=True)
    payment_type   = models.CharField(max_length=50, null=True)
    payment_due    = models.IntegerField(null=True)
    payment_status = models.IntegerField(default=1, null=True)
    bond           = models.IntegerField(default=0)


class WFUser(models.Model):
    """
    WFUser represents a Wallfly user.
    user - foreign key to a django user object
    user_level - denotes the level of the user in the system
    (1 - agent, 2 - owner, 3 - tenant)
    tenant_id (ForeignKey(Tenant)) - either null or the id of the Tenant
    owner_id (ForeignKey(Owner)) - either null or the id of the Owner
    agent_id (ForeignKey(Tenant)) - either null or the id of the Agent
    """

    user = models.OneToOneField(User)
    user_level = models.IntegerField(default=0)
    tenant_id = models.ForeignKey(Tenant, null=True, blank=True)
    owner_id = models.ForeignKey(Owner, null=True, blank=True)
    agent_id = models.ForeignKey(Agent, null=True, blank=True)

    def __unicode__(self):
        return "%s" % self.user
