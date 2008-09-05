
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'^GOSDjango/', include('GOSDjango.foo.urls')),

    # Uncomment this for admin:
     (r'^admin/', include('django.contrib.admin.urls')),    
     (r'^checklogin/', 'GOSDjango.GOSApp.views.checklogin'),
     (r'^profile/(?P<owner_id>\d+)/$', 'GOSDjango.GOSApp.views.showProfilePage'),
     (r'^confirmaddfriend/(?P<owner_id>\d+)/$', 'GOSDjango.GOSApp.views.confirmAddFriend'),
     (r'^addfriend/', 'GOSDjango.GOSApp.views.addFriend'),
     (r'^searchfriend/', 'GOSDjango.GOSApp.views.searchFriend'),
     (r'^logout/', 'GOSDjango.GOSApp.views.logout'),
     (r'^registration/', 'GOSDjango.GOSApp.views.getRegistrationPage'),
     (r'^registernewuser/', 'GOSDjango.GOSApp.views.registerNewUser'),
     (r'^getscraps/(?P<owner_id>\d+)/$', 'GOSDjango.GOSApp.views.getScraps'),
     (r'^postscrap/', 'GOSDjango.GOSApp.views.addScrap'),
     (r'^deletescrap/(?P<scrap_id>\d+)/$', 'GOSDjango.GOSApp.views.deleteScrap'),
     (r'^addgadget/(?P<gadget_id>\d+)/$', 'GOSDjango.GOSApp.views.addGadget'),
     (r'^deletegadget/(?P<gadget_id>\d+)/$', 'GOSDjango.GOSApp.views.deleteGadget'),
     (r'^viewgadgets/', 'GOSDjango.GOSApp.views.getGadgetPage'),
     (r'^replyscrap/(?P<owner_id>\d+)/$', 'GOSDjango.GOSApp.views.replyScrap'),
     
     
     
     
     #Redirections after this
     
     (r'^login/', 'GOSDjango.GOSApp.views.getloginpage'),
     (r'^invalidlogin/', 'GOSDjango.GOSApp.views.showInvalidLogin'),
     (r'^successlogin/', 'GOSDjango.GOSApp.views.showMyProfile'),
     

     
     
)
