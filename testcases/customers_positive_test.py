import req
import dbconnect
import helpers
from datetime import datetime
import string
import random

rq = req.REQ()
qry = dbconnect.DBConnect()
helper = helpers.Helper()

# this generate random inforation
def generate_random_info():
	"""
	This generates random strings. The strings generated are for email, username, first name and last name.

	:return: info - dictionary containing the randomly generated info

	"""

	info = {}
	# Generate random email and username
	# below is date time stamp of now and convert to string
	stamp = datetime.now().strftime("%Y%m%d%H%M%S")
	info['email'] = "api_user_" + stamp + "@gmail.com"
	info['user_name'] = "backend." + stamp

	# Generate random first name, last name and user name
	all_letters = string.lowercase
	# random mean select alphabets from a-z
	info['first_name'] = "".join(random.sample(all_letters, 8))
	info['last_name'] = "".join(random.sample(all_letters, 8))

	print("The generated email: {}".format(info['email']))
	print("The generated user name: {}".format(info['user_name']))
	print("The generated first name: {}".format(info['first_name']))
	print("The generated last name: {}".format(info['last_name']))

	return info

def test_create_customer():
	"""
	One happy path test. It will provide all the required and optional fields then verify that the response is as expected
	and also the database entry is as expected.
	"""

	# we put it global coz we use it in diff func
	global customer_id
	global expected_info_dict

	print 'TC1, customers, create new customer...'
	# generating random user info
	print 'Generating random user info'
   
	user_info = generate_random_info()

	email = user_info['email']
	user_name = user_info['user_name']
	first_name = user_info['first_name']
	last_name = user_info['last_name']

	input_data = {
	"customer": {
		"email": email,
		"first_name": first_name,
		"last_name": last_name,
		"username": user_name,
		"password": "test123",
		"billing_address": {
			"first_name": first_name,
			"last_name": last_name,
			"company": "",
			"address_1": "969 Market",
			"address_2": "",
			"city": "San Francisco",
			"state": "CA",
			"postcode": "94103",
			"country": "US",
			"email": email,
			"phone": "(555) 555-5555"
		},
		"shipping_address": {
			"first_name": last_name,
			"last_name": last_name,
			"company": "",
			"address_1": "969 Market",
			"address_2": "",
			"city": "San Francisco",
			"state": "CA",
			"postcode": "94103",
			"country": "US"
				}
			}
		}

	rs = rq.post('customers', input_data)

	expected_info_dict = input_data['customer']
	print rs

	print 'verifying response'
	# verify the status code before attempting to parse the response data. There may not be response data
	status_code = rs[0]
	assert status_code == 201 , "'customers' endpoint failed. status code expected: 201, Actual: {}. " \
								"The response body is: {}, URL is: {}".format(status_code, rs[1], rs[2])

	# if call is successful then get the response body
	response_body = rs[1]['customer']
	customer_id = response_body['id']
	print response_body
	print customer_id

	# start verification
	assert response_body["email"] == email, "'email' in response is not as expected. " \
											"Expected: {exp}, Actual: {act}".format(exp=response_body["email"], act=email)

	assert response_body["username"] == user_name, "'username' in response is not as expected." \
												   " Expected: {exp}, Actual: {act}".format(exp=response_body["username"], act=user_name)

	assert response_body["first_name"] == first_name, "'first_name' in response is not as expected." \
													  " Expected: {exp}, Actual: {act}".format(exp=response_body["first_name"], act=first_name)

	assert response_body["last_name"] == last_name, "'last_name' in response is not as expected. " \
													"Expected: {exp}, Actual: {act}".format(exp=response_body["last_name"], act=last_name)

	print 'PASS - Test Case: create customer happy path'


def test_verify_customer_info_in_db(expected_info_dict):
	"""

	:return: 

	"""

	# we take from helper class
	db_info = helper.get_customer_info_from_db_provided_customer_id(customer_id)

	failed_list = []
	# prints out the dict items in list format
	for key, value in expected_info_dict.items():
		print key
		print value
		# instead of using assert func, this will tell which line fails:
		if db_info[key] != value:
			msg = 'Bad value for {key} in db. Payload value: {pl}, DB value: {db}'.format(key=key,pl=value, db=db_info[key])
			failed_list.append(msg)

	# below means if the failed list is not empty
	if failed_list:
		raise Exception("There are failed values for created customer in db. Failed items are: {}".format(failed_list))
	# below print the success statement
	else:
		print("DB verification for create customer PASS!!!")

test_create_customer()