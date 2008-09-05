# Create your views here.

#   User is that person who has logged in
#
#
#
#

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from GOSDjango.GOSApp.models import User
from GOSDjango.GOSApp.models import User_Profile
from GOSDjango.GOSApp.models import User_Relation
from GOSDjango.GOSApp.models import Scraps
from GOSDjango.GOSApp.models import UserGadget
from GOSDjango.GOSApp.models import MasterGadget
from django.db import transaction
from django.core.context_processors import request
from django import newforms as forms
from datetime import date
from django.db.models.fields import ImageField
from MySQLdb import IntegrityError
from django.http import Http404
from django.core import validators
from django import oldforms as forms
from django.newforms import ValidationError

    



#
#All  Redirection are here
#
def getloginpage(request):
    return render_to_response('GOSApp/login.html')

def showInvalidLogin(request):
    return render_to_response('GOSApp/login.html',{'invalid':True})

def getRegistrationPage(request):
   return render_to_response('GOSApp/register.html')




#
#End of All Redirections 
#
    


def showMyProfile(request):
    ############################################################
    try:
        sessionMGT=request.session['user_info']
    except:
        return HttpResponseRedirect('/login/')
    ############################################################
        
    friends_list=set(request.session['friends_list'])
    profile_info = request.session['profile_info']
    user_info =  request.session['user_info']
    user_gadgets_info=UserGadget.objects.filter(USER_ID=user_info.USER_ID)
    print user_gadgets_info
    
    return render_to_response('GOSApp/myprofile.html',{'invalid':False,'friends_list':friends_list,'profile_info':profile_info,'user_info':user_info,'user_gadgets_info':user_gadgets_info})


#
#Handlers Login
#    
def checklogin(request):
    
    
    user_name=request.POST['user_name']
    password =request.POST['password']
    auth=User.objects.filter(USER_NAME=user_name)
    if auth:
        if auth[0].PASSWORD == password:
            fetchUserInfo(auth[0].USER_ID,request);
            return HttpResponseRedirect('/successlogin/')
        
        else :
            user_name=None
            password=None
            return HttpResponseRedirect('/invalidlogin/')
        
    user_name=None
    password=None
    return HttpResponseRedirect('/invalidlogin/') 
     

def fetchUserInfo(id,request):   
    
    friends_list=getFriendList(id)
    request.session['friends_list']=friends_list
    
    profile_info=User_Profile.objects.get(USER_ID=id)
    request.session['profile_info']=profile_info
    
    user_info=User.objects.get(USER_ID=id)
    request.session['user_info']=user_info
    
   
    
           
#
# End of Login Handlers
#  
  
       
#
#Login module till here
#
  
   
   
#
#View Profile Page Handlers 
#

def showProfilePage(request,owner_id):
    ############################################################
    try:
        sessionMGT=request.session['user_info']
    except:
        return HttpResponseRedirect('/login/')
    ############################################################
        
    profile_info= get_object_or_404(User_Profile, USER_ID=owner_id)
    user_info=request.session['user_info']
    user_friends=request.session['friends_list']
    
    alreadyAFriend=isAlreadyAFriend(user_info,user_friends, owner_id)
    friends_list=getFriendList(owner_id)
    
    ####################################
    #Gadgets
    ####################################
    user_gadgets_info=UserGadget.objects.filter(USER_ID=profile_info.USER_ID.USER_ID)

    return render_to_response('GOSApp/profile.html',{'friends_list':friends_list,'profile_info':profile_info,'user_info':user_info,'alreadyAFriend':alreadyAFriend,'user_gadgets_info':user_gadgets_info})


#
#End of Profile Page Handlers
#  
   
   
   
#
#Add Friend Page Request Handlers
#   

#
#There are only 1 ways of adding a friend
# 1.Go to his profile and add him
# 

def confirmAddFriend(request,owner_id):
    ############################################################
    try:
        sessionMGT=request.session['user_info']
    except:
        return HttpResponseRedirect('/login/')
    ############################################################
    
    profile_info= get_object_or_404(User_Profile, USER_ID=owner_id)
    user_friends=request.session['friends_list']
    user_info=request.session['user_info']    
    alreadyAFriend=isAlreadyAFriend(user_info,user_friends, owner_id)
    if alreadyAFriend:
        return  render_to_response('GOSApp/alreadyafrd.html','')
        
    return render_to_response('GOSApp/confirmAddFriend.html',{'profile_info':profile_info,'user_info':sessionMGT})
      

def addFriend(request):
    ############################################################
    try:
        sessionMGT=request.session['user_info']
    except:
        return HttpResponseRedirect('/login/')
    ############################################################
    
    owner_id= request.POST['owner_id']
    user_info =  request.session['user_info']
    user_friends=user_friends=request.session['friends_list']
    alreayAFriend=isAlreadyAFriend(user_info, user_friends, owner_id)
    if alreayAFriend:
       return  render_to_response('GOSApp/alreadyafrd.html','') 
    
    user_id=user_info.USER_ID
    saveFriend(user_id, owner_id)
    fetchUserInfo(user_id,request)    
    return HttpResponseRedirect('/successlogin/')
    
       
#
#Add Friend Request Handler End here
#   
   
#
#Search Handlers after this
#   


def searchFriend(request):
    ############################################################
    try:
        sessionMGT=request.session['user_info']
    except:
        return HttpResponseRedirect('/login/')
    ############################################################
    
    searchString= request.GET['searchString']
    searchResults=User_Profile.objects.filter(NAME__icontains=searchString)
    if len(searchResults)==1:
        print searchResults[0].USER_ID.USER_ID        
        return HttpResponseRedirect('/profile/' +str(searchResults[0].USER_ID.USER_ID)+ '/')
    
    friends_list=request.session['friends_list']
    profile_info=request.session['profile_info']                                    
    return render_to_response('GOSApp/searchresults.html',{'searchResults':searchResults,'user_info':sessionMGT,'friends_list':friends_list,'profile_info':profile_info})
    print searchResults   
      
#
#Search handlers end here
#

#
# Log out Handlers here
#

def logout(request):
    ############################################################
    try:
        sessionMGT=request.session['user_info']
    except:
        return HttpResponseRedirect('/login/')
    ############################################################
    
    del request.session['user_info']
    del request.session['friends_list']
    del request.session['profile_info']
    return HttpResponseRedirect('/login/')


#
#End of logout handlers
#  


#
#Registration handlers here
#


def registerNewUser(request):
   user_name=request.POST['user_name']
   display_name=request.POST['display_name']
   pass_word=request.POST['password']
   re_password=request.POST['repassword']
   validationError=False
   genderError=False
   imgObjNull=False
   try:
        gender=request.POST['gender']
   except:
        validationError=True
        genderError=True
   date_of_birth1=request.POST['dateofbirth1']
   date_of_birth2=request.POST['dateofbirth2']
   date_of_birth3=request.POST['dateofbirth3']
   
   try:
       my_image_valid = request.FILES['my_image']
   except:
       imgObjNull=True
       pass
   
   aboutme=request.POST['aboutme']
   
       ##################
       #Validation Here##
       ##################
       
   userNameError=False
   displayNameError=False
   passwordError=False
   confirmPasswordError=False
   dateOfBirthError=False
   imageError=False
   try:
       tempDate=date(int(date_of_birth3),int(date_of_birth1),int(date_of_birth2))
       if int(date_of_birth3)>2007:
           validationError=True
           dateOfBirthError=True
           
       
   except:
       validationError=True
       dateOfBirthError=True
    
   try:
        userName = validators.isAlphaNumeric(user_name,request.POST)
   except :
        print 'userNameError'
        validationError=True
        userNameError=True
        
        
   try:
         displayName = validators.isAlphaNumeric(display_name,request.POST)
   except :
        validationError=True
        displayNameError=True
        
        
   try:
         password= validators.isNotEmpty(pass_word,request.POST)
   except :
        validationError=True
        passwordError=True
        
   #try:
       #  dateOfBirth = validators.isValidANSIDate (tempDate,request.POST)
   #except :
        #validationError=True
        #dateOfBirthError=True
        
   try:
         image = validators.isValidImage(my_image_valid,request.POST)
   except :
        if not imgObjNull:
            validationError=True
            imageError=True
        
   if  pass_word!=re_password:
         validationError=True
         confirmPasswordError=True
         
   if validationError:
        print 'error'
        return render_to_response('GOSApp/register.html', {'userNameError':userNameError,'displayNameError':displayNameError,'passwordError':passwordError,'dateOfBirthError':dateOfBirthError,'imageError':imageError,'genderError':genderError,'confirmPasswordError':confirmPasswordError})
               
   print 'hi'     
        
    
    
   class InstallationManipulator(forms.Manipulator):
        def __init__(self):
             self.fields = (
             forms.CharField(field_name = "user_name",field_name="display_name",field_name="password",field_name="",field_name="",field_name="my_image", validator_list=[userName,displayName,password , dateOfBirth,image])
             
             )
       
       
       
       
       
       
       
       
       
       
        
       
       ####################
       #End of Validation##
       ####################
   
   filename=None
   content=None
   print 'hi'
   #image
   if request.FILES.has_key('my_image'):
      filename = request.FILES['my_image']['filename']
      content= request.FILES['my_image']['content']
      
   if filename == None:
       try:
           if gender=='male':
               subsURL='css/images/boy.jpg'
           elif gender=='female':
               subsURL='css/images/girl.jpg'
               
           userregistration=User.objects.create(USER_NAME=user_name,DISPLAY_NAME=display_name,PASSWORD=pass_word)
           register=User_Profile.objects.create(NAME=display_name,GENDER=gender, DATEOFBIRTH=tempDate, ABOUTME=aboutme,USER_ID=userregistration,MY_IMAGE=subsURL)           
       except IntegrityError :
           print 'catch'
           return render_to_response('GOSApp/register.html',{'alreadyPresent':True})
       except :
           userregistration.delete()   #Transaction control was not working that is why i have to do this
           return render_to_response('GOSApp/register.html',{'invalidDate':True})
   
             
       return HttpResponseRedirect('/login/')

           
   else:     
       #image
       try:
           userregistration=User.objects.create(USER_NAME=user_name,DISPLAY_NAME=display_name,PASSWORD=pass_word)
           register=User_Profile.objects.create(NAME=display_name,GENDER=gender, DATEOFBIRTH=tempDate, ABOUTME=aboutme,USER_ID=userregistration)  
           #register.save()
           register.save_MY_IMAGE_file(filename, content)
              
       except IntegrityError :
           print 'catch'
           return render_to_response('GOSApp/register.html',{'alreadyPresent':True})
       except :
           userregistration.delete()   #Transaction control was not working that is why i have to do this
           return render_to_response('GOSApp/register.html',{'invalidDate':True})
       
                 
       return HttpResponseRedirect('/login/')


    

#
#End of Registration handlers 
#



#util functions after this

def isAlreadyAFriend(user_info,user_friends,owner_id):
    
    alreadyAFriend=False
    for users in user_friends:
        if int(owner_id) == int(users.USER_ID.USER_ID):
            alreadyAFriend=True
        else:
            continue
        
    if int(owner_id)==int(user_info.USER_ID):
        alreadyAFriend=True                        #Everybody is a friend of itself
        
    return alreadyAFriend                          #If the person is already a friend then no need of add a frd link
      
     
@transaction.commit_on_success
def saveFriend(user_id,owner_id):
    user_details=User.objects.get(USER_ID=user_id)
    owner_details=User.objects.get(USER_ID=owner_id)
    obj=User_Relation(USER_ID=user_details,FRIEND_USER_ID=owner_details,STATUS="APPROVED")
    obj.save()
    return

def getFriendList(id):
    #Mannually removing all the duplicate entries if
    #Logic will not do duplicate entries in the database 
    #But smhow if smbody hacked the logic to bypasss that we r removing 
    #a single friend entry multiple times
    #
    friends_list_temp=User_Relation.objects.filter(USER_ID=id)
    friend_id_list=[x.FRIEND_USER_ID.USER_ID for x in friends_list_temp]
    friend_id_unique_list=set(friend_id_list)    
        
    friends_list=[]
    
    # A for loop a setback to performance
    for count in friend_id_unique_list:
        friends_list.append(User_Profile.objects.get(USER_ID=count))
        
    return friends_list
     


def convertIdListintoUser_ProfileObjList(idList):
    userProfileObj=[]
    for count in idList:
        userProfileObj.append(User_Profile.objects.get(USER_ID=count))
        
    return userProfileObj                      
                              
    
   
    

###############################################################################################
#Scraps functionality after this including redirections
#
#
#
###############################################################################################


def getScraps(request,owner_id):    #owner_id is the person who owns the scrap book
    ############################################################
   try:
        sessionMGT=request.session['user_info']
   except:
        return HttpResponseRedirect('/login/')
    ############################################################
   viewer_id=request.session['user_info'].USER_ID
   
   #Weather the person is able to delete the scrap or not
   activateDeleteButton=False
   if int(viewer_id)== int(owner_id):
       activateDeleteButton=True
   
   #Getting user details
   user_info=request.session['user_info']
   profile_info= get_object_or_404(User_Profile, USER_ID=owner_id)
   
   
   #Fetching the scraps
   scrapsResult=Scraps.objects.filter(USER_ID=owner_id)
   scrapperIdList=[x.SCRAPPER_ID.USER_ID for x in scrapsResult]
   print scrapperIdList
   scrapperProfileList=convertIdListintoUser_ProfileObjList(scrapperIdList)
   scrapsCombo=[]
   for count in range(len(scrapperProfileList)):
       scrapsCombo.append([scrapperProfileList[count],scrapsResult[count]])
       

   return render_to_response('GOSApp/scraps.html',{'user_info':user_info,'profile_info':profile_info,'scrapsCombo':scrapsCombo,'activateDeleteButton':activateDeleteButton})   



def addScrap(request):
    ############################################################
    try:
        sessionMGT=request.session['user_info']
    except:
        return HttpResponseRedirect('/login/')
    ############################################################
    
    scrapData= request.POST['scrapData']
    owner_id= request.POST['owner_id']
    user_info=request.session['user_info']   # the person who has logged in
    userOBJ= get_object_or_404(User, USER_ID=owner_id)
    data=Scraps.objects.create(USER_ID=userOBJ,SCRAPPER_ID=user_info,SCRAP=scrapData,STATUS='new')
    data.save()
    redirectURL='/getscraps/'+str(owner_id)
    return HttpResponseRedirect(redirectURL)


def deleteScrap(request,scrap_id):
    ############################################################
    try:
        sessionMGT=request.session['user_info']
    except:
        return HttpResponseRedirect('/login/')
    ############################################################
    
    userId=request.session['user_info'].USER_ID
    scrapOBJ= get_object_or_404(Scraps, SCRAP_ID=scrap_id)
    access = False
    if scrapOBJ.USER_ID.USER_ID == userId:
        access=True
    elif scrapOBJ.SCRAPPER_ID.USER_ID == userId:
        access =True            
    else:
        raise Http404
    
    pagetoRedirect='/getscraps/'+str(scrapOBJ.USER_ID.USER_ID)
    scrapOBJ.delete()
    return HttpResponseRedirect(pagetoRedirect) 



def replyScrap(request,owner_id):
    userOBJ= get_object_or_404(User,USER_ID=owner_id)
    print owner_id
    return render_to_response('GOSApp/replypage.html',{'owner_id':owner_id})
       
    


###############################################################################################
#Gadgets functionality after this including redirections
#
#
#
###############################################################################################



def getGadgetPage(request):
    ############################################################
    try:
        sessionMGT=request.session['user_info']
    except:
        return HttpResponseRedirect('/login/')
    ############################################################
    
    profile_info=request.session['profile_info']
    userGadgets=UserGadget.objects.filter(USER_ID=sessionMGT.USER_ID)
    allGadgets=MasterGadget.objects.all()
    
    gadgetComboList=[]
    userGadgetsList=[x.ID.ID for x in userGadgets]
    for count in allGadgets:
        if count.ID in userGadgetsList:
            gadgetComboList.append([count,True])
        else:
            gadgetComboList.append([count,False])
            
    print gadgetComboList        
    return render_to_response('GOSApp/viewgadgets.html',{'gadgetComboList':gadgetComboList})



def addGadget(request,gadget_id):
    ############################################################
    try:
        sessionMGT=request.session['user_info']
    except:
        return HttpResponseRedirect('/login/')
    ############################################################
    
    usergadgets=UserGadget.objects.filter(USER_ID=sessionMGT.USER_ID)
    
    if int(gadget_id) in [int(x.ID.ID) for x in usergadgets]:
        raise Http404
     
    try:
        gadgetObj=MasterGadget.objects.get(ID=gadget_id)
        insert=UserGadget.objects.create(ID=gadgetObj,USER_ID=sessionMGT)
        insert.save()
        return HttpResponseRedirect('/viewgadgets/')
        
    
    except Exception:
       raise Http404
        
        
        
    
      


def deleteGadget(request,gadget_id):
    ############################################################
    try:
        sessionMGT=request.session['user_info']
    except:
        return HttpResponseRedirect('/login/')
    ############################################################
    
    print gadget_id
    gadgetObj=MasterGadget.objects.filter(ID=gadget_id)
    print gadgetObj
    
    objToDelete=get_object_or_404(UserGadget,USER_ID=sessionMGT.USER_ID,ID=gadget_id)
    try:
        objToDelete.delete()
        return HttpResponseRedirect('/viewgadgets/')
    except:
        raise Http404
     