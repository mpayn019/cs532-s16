#Developed by Kevin Clemmons
import threading 
import logging 
import unittest
import datetime
#logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',datefmt='%m-%d %H:%M:%S',filename='data_files_py.log',filemode='w')


generalLogger = logging.getLogger('gen_log')
dataLogger = logging.getLogger('u_data')
itemLogger = logging.getLogger('u_item')
userLogger = logging.getLogger('u_user')
read_data_logger = logging.getLogger('read_data')



def read_data(data_lines,data):
	'''Reads the lines extracted from the file u.data 
	Args:
		data_lines: Strings that where read from the file u.data. 
		data: A list of dictionaries containing the various data parts.
	''' 
	dataLogger.info("Extracting <user_id> <item_id> <rating> <timestamp> from {0} lines.".format(len(data_lines)))
	for line in data_lines:
		# Split the line into
		tmp = line.split()
		timeS = float(tmp[3])
		timeConvert = datetime.datetime.utcfromtimestamp(timeS).timetuple()
		timeVal = {'year':timeConvert.tm_year,'month':timeConvert.tm_mon,'day':timeConvert.tm_mday,'hour':timeConvert.tm_hour,'minute':timeConvert.tm_min,'second':timeConvert.tm_sec}


		# Create a data point 
		dataPoint = {'user_id':tmp[0],'item_id':tmp[1],'rating':float(tmp[2]),'timestamp':float(tmp[3]),'converted_time_stamp':timeVal}
		#print(dataPoint)
		# Add the data point to the list of data 
		data.append(dataPoint)
	dataLogger.info("Finished extracting {0} lines of data".format(len(data_lines)))



def read_item(item_lines,items):
	'''Reads the lines extracted from u.item 
	Args: 
		item_lines: Strings that were extracted from the file u.item 
		items: A list of dictionaries containing the various data parts 
	'''
	itemLogger.info("Extracting <movie_id>|<movie_title>|<release_date>|<video_release_date>|<IMDb_URL>|<movieGenres>... from {0} lines".format(len(item_lines)))
	for line in item_lines:
		tmp = line.split("|")
		dataPoint = {'movie_id': tmp[0],
					 'movie_title': tmp[1],
					 'release_date': tmp[2],
					 'video_release_date': tmp[3],
					 'IMDb_URL': tmp[4],
					 'unknown': int(tmp[5]),
					 'Action': int(tmp[6]),
					 'Adventure': int(tmp[7]),
					 'Animation': int(tmp[8]),
					 'Childrens': int(tmp[9]),
					 'Comedy': int(tmp[10]),
					 'Crime': int(tmp[11]),
					 'Documentary': int(tmp[12]),
					 'Drama': int(tmp[13]),
					 'Fantasy': int(tmp[14]),
					 'Film-Noir': int(tmp[15]),
					 'Horror': int(tmp[16]),
					 'Musical': int(tmp[17]),
					 'Mystery': int(tmp[18]),
					 'Romance': int(tmp[19]),
					 'Sci-Fi': int(tmp[20]),
					 'War': int(tmp[21]),
					 'Western': int(tmp[22])}
		items.append(dataPoint)
	itemLogger.info("Finished extracting {0} lines.".format(len(item_lines)))

def read_user(user_lines,users):
	'''Reads the lines created from the file u.user. 
	Args: 
		user_lines: Strings that were read from u.user
		users: A list of dictionaries containing parts extracted from the lines acquired from u.user
	'''
	userLogger.info("Extracting <user_id>|<age>|<gender>|<occupation>|<zipcode> from {0} lines.".format(len(user_lines)))
	for line in user_lines:
		tmp = line.split("|")
		dataPoint = {'user_id':int(tmp[0]),'age':int(tmp[1]),'gender':tmp[2],'occupation':tmp[3],'zipcode':tmp[4]}
		users.append(dataPoint)
	userLogger.info("Finished extracting {0} lines".format(len(user_lines)))

def read_data_set(data_set_file_name):
	'''Creates a list of strings read from a file. 
	Args:
		data_set_file_name: The name of a file to read data from.
	Returns:
		A list of strings from a file. 
	'''

	lines = None
	dataFile = None 

	try:
		dataFile = open(data_set_file_name,'r')
	except IOError as e:
		generalLogger.error("Error opening data file: {0}, {1}".format(data_set_file_name,e[1]))

	if dataFile is not None:
		lines = []
		# Add all lines of data into an array stripping the new line character
		generalLogger.info("Reading {0} and creating array of lines.".format(data_set_file_name))
		for line in dataFile.readlines():
			lines.append(line.strip('\n'))
		dataFile.close()

		generalLogger.info('Finished reading {0}'.format(data_set_file_name))

	return lines 


def read_data_files(dataName='u.data',itemName='u.item',userName='u.user'):
	threadList = [] # A list of concurrent threads
	
	data = [] # A list of processed lines 
	users = [] # A list of processed users 
	items = [] # A list of processed items
	
	# Threading variables 
	data_thread = None
	item_thread = None 
	user_thread = None 

	# Read the lines of the data files 
	raw_data = read_data_set(dataName)
	raw_items = read_data_set(itemName)
	raw_users = read_data_set(userName)

	# Create threads to process the lines from the data files
	if raw_data is not None:
		data_thread = threading.Thread(name='data_thread',target=read_data,args=(raw_data,data))
		generalLogger.debug('Created thread: {0}'.format(data_thread.getName()))
		threadList.append(data_thread)
	
	if raw_items is not None:
		item_thread = threading.Thread(name='item_thread',target=read_item,args=(raw_items,items))
		generalLogger.debug('Created thread: {0}'.format(item_thread.getName()))
		threadList.append(item_thread)
	
	if raw_users is not None:
		user_thread = threading.Thread(name='user_thread',target=read_user,args=(raw_users,users))
		generalLogger.debug('Created thread: {0}'.format(user_thread.getName()))
		threadList.append(user_thread)

	# Start processing the data lines 
	for i in threadList:
		generalLogger.debug('Starting thread: {0}'.format(i.getName()))
		i.start()

	# Wait for all the data components to be processed
	while True:
		if len(filter(lambda t: t.is_alive(),threadList)) == 0:
			break

	generalLogger.info('Finished processing data files')

	# Return data,users,items
	return data,users,items

##########################Test code######################################
# Unit tests for above functions
class TestDataExtractors(unittest.TestCase):
	def setUp(self):
		pass

	def test_read_data_set(self):
		self.assertEqual(len(read_data_set('data_files/u.data')),100000)
		self.assertEqual(len(read_data_set('data_files/u.item')),1682)
		self.assertEqual(len(read_data_set('data_files/u.user')),943)

	def test_read_user(self):
		lines = read_data_set('data_files/u.user')
		userList = []
		read_user(lines,userList)
		self.assertEqual(len(userList),len(lines))

	def test_read_item(self):
		lines = read_data_set('data_files/u.item')
		itemList = [] 
		read_item(lines,itemList)
		self.assertEqual(len(itemList),len(lines))

	def test_read_data(self):
		lines = read_data_set('data_files/u.data')
		dataPoints = []
		read_data(lines,dataPoints)
		self.assertEqual(len(dataPoints),len(lines))

	def test_read_data_files(self):
		data,users,items = read_data_files(dataName='data_files/u.data',itemName='data_files/u.item',userName='data_files/u.user')
		self.assertEqual(len(data),100000)
		self.assertEqual(len(users),943)
		self.assertEqual(len(items),1682)

####################################################### Running the test code 
# To Run tests: 
## Enter the command: python data_extractor.py 
## For verbose command: python data_extractor.py -v
if __name__ == '__main__':
	unittest.main()
