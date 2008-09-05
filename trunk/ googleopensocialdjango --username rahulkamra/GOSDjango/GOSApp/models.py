from django.db import models
from django.db.models import ImageField, signals
from django.dispatch import dispatcher




    
     
# Create your models here.
class User(models.Model):
  USER_ID = models.AutoField(primary_key=True,db_column="USER_ID")
  USER_NAME=models.CharField(maxlength=255,db_column="USER_NAME",unique=True)
  PASSWORD =models.CharField(maxlength=255,db_column="PASSWORD")
  DISPLAY_NAME=models.CharField(maxlength=255,db_column="DISPLAY_NAME")
  
  class Meta:
      db_table="user"
  
  class Admin:
    list_display=("USER_NAME","PASSWORD","DISPLAY_NAME")
    
  def __str__(self):
        return self.USER_NAME  
    
###########################################################################
###########################################################################
  
  
class User_Profile(models.Model):
  USER_ID = models.ForeignKey(User,db_column="USER_ID",primary_key=True)
  MY_IMAGE=models.ImageField(upload_to='gosphotos/%Y/%m/%d')
  NAME=models.CharField(maxlength=255) #considering this as display name
  GENDER=models.CharField(maxlength=255)
  DATEOFBIRTH =models.DateField()
  ABOUTME =models.TextField()
  
  class Meta:
      db_table="user_profile"
      
  class Admin:
    list_display=("MY_IMAGE","NAME","GENDER","DATEOFBIRTH","ABOUTME")

  def __str__(self):
        return self.NAME 
  #def get_upload_to(self, field_attname):
   #     """Get upload_to path specific to this photo."""
    #    return 'photos/%d' % self.id
  
 
###########################################################################
########################################################################### 

class User_Relation(models.Model):
  USER_RELATION_ID = models.AutoField(primary_key=True,db_column="USER_RELATION_ID")
  USER_ID = models.ForeignKey(User,db_column="USER_ID" ,related_name="user_id")
  FRIEND_USER_ID=models.ForeignKey(User,db_column="FRIEND_USER_ID",related_name="friend_id")
  STATUS=models.CharField(maxlength=255)

  
  class Admin:
    list_display=("USER_ID","FRIEND_USER_ID","STATUS")
    
  class Meta:
      db_table="user_relation"
    
  def __unicode__(self):
        return self.USER_ID 
  
###########################################################################
###########################################################################

  
class Scraps(models.Model):
    SCRAP_ID=models.AutoField(primary_key=True,db_column="SCRAP_ID")
    USER_ID = models.ForeignKey(User,db_column="USER_ID" ,related_name="user_scraps_id")
    SCRAPPER_ID = models.ForeignKey(User,db_column="SCRAPPER_ID" ,related_name="scrapper_id")
    SCRAP=models.TextField() 
    STATUS=models.CharField(maxlength=255)
    
    class Admin:
        pass 
    
    class Meta:
      db_table="scraps"
      ordering=['-SCRAP_ID']
      
    def __str__(self):
        return self.SCRAP

###########################################################################
###########################################################################



class MasterGadget(models.Model):
  ID =models.AutoField(primary_key=True,db_column="ID")
  NAME= models.CharField(maxlength=255)
  DESCRIPTION=models.TextField()
  GADGET_URL =models.CharField(maxlength=255)
  IMAGE_URL = models.ImageField(upload_to='gadgetimages/%Y/%m/%d')
  class Admin:
    list_display=("ID","NAME","DESCRIPTION","GADGET_URL","IMAGE_URL")
    
  class Meta:
      db_table="mastergadget"
      
  def __str__(self):
        return self.NAME 


###########################################################################
###########################################################################

class UserGadget(models.Model):
  GADGET_RELATION_ID=models.AutoField(primary_key=True,db_column="GADGET_RELATION_ID")  
  ID =models.ForeignKey(MasterGadget,db_column="ID")
  USER_ID=models.ForeignKey(User,db_column="USER_ID") 
  class Admin:
    list_display=("GADGET_RELATION_ID","ID","USER_ID")
    
  class Meta:
      db_table="usergadget"
      
  def __unicode__(self):
        return self.ID 
