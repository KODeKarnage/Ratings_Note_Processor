


# XBMC modules
import xbmc
import xbmcaddon

# Standard modules
import os
import shutil
import time
import re
import sys

# Custom modules
import lazytools as T
log = T.logger()




class monitor(xbmc.Monitor):

	def __init__(self, main):
		self.main = main

	def onDatabaseUpdate(self):
		if video:
			main.REFRESH()

	def onSettingsChanged(self):
		MAIN.refresh_setings()


class Main:

	def __init__(self):

		'''
		self.show_dict = {
				SHOWID: {
					'TVDBID': @@@@, 
		 			'name': @@@@, 
		 			'local_episodes': { (season, episode) : episodeID, ..., ...},
		 			'TVDB_episodes'	: [ (season, episode), , ..., ...],
		 			'missing_episodes'  : [ (season, episode), , ..., ...],
		 			}
		 		}
		'''

		self.show_dict = {}

		# a list of the entries to remove from the library
		# this will only be populated when stubs are slated for removal
		self.remove_these = []

		self.create_show_dict()

		# create TVDB api
		self.TVDB = THETVDBAPI()

		# create database and settings monitor
		self.monitor = monitor()

	# MAIN 
	def refresh(self):
		'''
		# check for any new shows
			process any that are new

		# check all stubs to see if they have epid, if not then add them


		'''

	# MAIN
	def retrieve_settings(self):
		
		__addon__        = xbmcaddon.Addon('script.missing.tv')
		__setting__      = __addon__.getSetting


		self.sub_location = __setting__('sub_location')
		self.sub_prefix   = __setting__('prefix')

		if self.sub_location == 'default':
			self.ADDON_DATA_FOLDER = xbmc.translatePath('special://userdata')
			self.SUB_FOLDER = os.path.join(self.ADDON_DATA_FOLDER, 'Missing_TV')
		else:
			self.SUB_FOLDER = self.sub_location


		# check if the SUB_FOLDER exists, create if it doesnt
		if not os.path.exists(self.SUB_FOLDER):
			os.mkdirs(self.SUB_FOLDER)

	# MAIN		
	def threader(self, function, arguments):
		''' creates x number of threads to process the arguments in the function '''

	# SHOW DICT
	def create_show_dict(self, showid = None):
		''' 
		# self.show_dict = {
		#			SHOWID: {
		#			'TVDBID': @@@@, 
		# 			'name': @@@@, 
		# 			'local_episodes': { (season, episode) : episodeID, ..., ...},
		# 			'TVDB_episodes'	: [ (season, episode), , ..., ...],
		# 			'missing_episodes'  : [ (season, episode), , ..., ...],
		# 			}}
		'''

		# get showid, name from JSON
		# get local_episodes from JSON, process into local_episodes dict
		# get TVDB ID from api
		# get TVDB episodes, process into TVDB_episodes

		## once created ##

		# find the missing episodes
		self.identify_missing()

		# create the subsitutes
		self.create_substitutes()

		# remove_these stubs from the library
		

		# call for a refresh of the SUB_FOLDER
		self.request_library_update()


	# SHOW DICT
	def process_show_info(self, local_show_dict, new_show = False):

		if new_show:
			''' retrieve the TVDBID '''
			SHOWID = local_show_dict.get('showid','')
			self.show_dict[SHOWID] = {}

			if SHOWID:
				self.show_dict[SHOWID]['TVDBID'] = self.retrieve_TVDBID(SHOWID)
			else:
				return

		''' create or update entry in local_show_dict '''
		episodes = [(season, episode) for x in local_show_dict]

	# SHOW DICT
	def retrieve_show_info(self, showid = None):
		''' retrieves the locally stored info '''
		pass

	# SHOW DICT
	def retrieve_TVDBID(self, showname):
		''' use showname to get TVDBID '''

	# SHOW DICT
	def retrieve_TVDB_info(self, TVDBID):
		''' retrieve all episode info for a specific show '''

	# SHOW DICT
	def identify_missing(self, showid = None):
		''' compares the TVDB episodes to the local episodes 
			and updates show dict with all missing eps '''

		# allow for single show update
		pairs = single_or_all(showid)

		for k, v in pairs:
			
			local_eps  = set(v.get('local_episodes',{}).keys())
			remote_eps = set(v.get('TVDB-Episodes',[]))

			self.show_dict[k]['missing_episodes'] = list(remote_eps.difference(local_eps))

	# SHOW DICT
	def single_or_all(self, showid):
		''' allow for single show, or complete update '''

		if showid:
			pairs = (showid, self.show_dict.get(showid,{}))
		else:
			pairs = self.show_dict.iteritems()

		return pairs

	# STUBS
	def create_substitutes(self, showid = None):
		''' creates/updates the substitutes folder in addondata '''

		# allow for single show update
		pairs = single_or_all(showid)

		# get the current structure and population of sub folder
		subs = self.retrieve_subs()

		# get just the names of the folders (tvshows)
		existing_sub_folders = set(subs.keys())

		# get the list of the folders that are needed
		needed_sub_folders = set([v['name'] for k, v in pairs if v.get('name', False)])

		# create a list of the folders that need to be created
		create_these_folders  = needed_sub_folders.difference(existing_sub_folders)

		# create a list of the folders that need to be destroyed
		destroy_these_folders = destroy_these_folders.difference(needed_sub_folders)		

		# create the folders
		self.create_folders(create_these_folders)

		# only destroy folders if this ISNT a single show update
		if not showid:
			self.destroy_folders(destroy_these_folders)

		# cycle through the shows and create the episode stubs
		for k, v in pairs:

			self.create_or_delete_stubs(k, v, subs)

	# STUBS
	def retrieve_subs(self):
		''' returns a dict of {showname : [(season, episode), ...]}
			for each sub-folder in addondata '''

			subs_dict = {}

		for showname in os.walk(self.SUB_FOLDER):

			for stub in os.listdir(showname):

				p = r'Missing_Sub_s(\d+)e(\d+).avi'
				match = re.search(p, stub)

				if not match:
					continue

				subs_dict['showname'] = (match.group(1), match.group(2))

		return subs_dict

	# STUBS
	def create_folders(self, namelist):
		''' creates the folders in the namelist in the addondata directory '''
		for name in namelist:
			path = os.path.join(self.SUB_FOLDER, name)
			os.mkdir(path)

	# STUBS
	def destroy_folders(self, namelist):
		''' destroys the folders in the namelist from the addondata directory '''	
		for name in namelist:
			path = os.path.join(self.SUB_FOLDER, name)

			self.remove_these += os.listpath(path)

			shutil.rmtree(path)

	# STUBS
	def create_or_delete_stubs(self, k, v, subs):

		# get the missing episode tuples
		missing_episodes = set(v.get('missing_episodes', []))

		# get the existing episode tuples
		existing_stubs = set(subs.values())

		# delete the unneeded stubs
		delete_these_stubs = existing_stubs.difference(missing_episodes)

		for stub in delete_these_stubs:

			epid = self.remove_stub(stub)

		# create the missing stubs
		create_these_stubs = missing_episodes.difference(existing_stubs)

		for episode in create_these_stubs:
			
			self.add_stub(episode)

	# STUBS
	def remove_stub(self, stub):
		ep_name = 'Missing_Sub_s{}e{}.avi'.format(stub[0], stub[1])

		path = os.path.join(self.SUB_FOLDER, k, ep_name)		

		os.remove(path)

		self.remove_these.append(path)

	# STUBS
	def add_stub(self, episode):
		''' create_stub using season and episode, write the epid into the file '''

		ep_name = 'Missing_Sub_s{}e{}.avi'.format(episode[0], episode[1])

		stub = os.path.join(self.SUB_FOLDER, k, ep_name)

		epid = ???????????????????????????????????????????

		with open(stub, 'w') as f:
			pass

	# STUBS
	def update_stubs(self):
		''' runs immediately after a library update, 
			writes the epid into each stub '''

	# STUBS
	def request_library_update(self):
		''' Request a library update of the specific addondata folder  '''

	# LIBRARY
	def remove_from_library(self, epid):
		''' removes the episode from the library '''

		for filename in self.remove_these:
			JSON REQUEST REMOVAL FROM LIBRARY

		self.remove_these = []

	# LIBRARY		
	def change_name_in_library(self):
		''' find all the stub items in the library and rename them using the 
			user selected prefix self.sub_prefix '''

		get all the episodes from the local dir 
		where there is a filename with 'Missing_Sub_s'
		and where the display name doesnt have the prefix
		change the display name to have the prefix

		also write the epid into the stub


if ( __name__ == "__main__" ):

	Main()

	while not xbmc.abortRequested:

		xbmc.sleep(10)

	del Main
