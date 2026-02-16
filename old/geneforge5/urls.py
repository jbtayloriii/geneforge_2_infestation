from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.indexView, name='index'),
	
	#Aggregate pages
	url(r'^zones/$', views.zonesView, name='zones'),
	url(r'^items/$', views.itemsView, name='items'),
	url(r'^canisters/$', views.canistersView, name='canisters'),
	url(r'^quests/$', views.questsView, name='quests'),
	url(r'^skills/$', views.skillsView, name='skills'),
	url(r'^reputation/$', views.reputationView, name='reputation'),
	url(r'^specItems/$', views.specItemsView, name='specItems'),
	url(r'^shops/$', views.shopsView, name='shops'),
	url(r'^crafting/$', views.craftingView, name='crafting'),

	#Specific pages
	url(r'^zone/(?P<zone_id>[0-9]+)/$', views.zoneView, name='zone'),
	url(r'^item_template/(?P<item_template_id>[0-9]+)/$', views.itemTemplateView, name='item_template'),
	url(r'^quest/(?P<quest_id>[0-9]+)/$', views.questView, name='quest'),
	url(r'^skill/(?P<skill_id>[0-9]+)/$', views.skillView, name='skill'),
	url(r'^shop/(?P<shop_id>[0-9]+)/$', views.shopView, name='shop'),
]
