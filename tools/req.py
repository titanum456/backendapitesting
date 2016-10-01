from woocommerce import API

class REQ():

	def __init__(self):
		admin_consumer_key = ''
		admin_consumer_secret = ''

		self.wcapi = API(
			url="http://127.0.0.1/akstore/",
			consumer_key=admin_consumer_key,
			consumer_secret=admin_consumer_secret,
			version="v3")

	# method to test the api
	def test_api(self):
		'''

		:return:
		'''
		# below para is empty string
		print self.wcapi.get("").json()


	# for post call, we pass some endpoint and data which is payload
	def post(self,endpoint,data):
		'''

		:param endpoint:
		:param data:
		:return:
		'''

		# below capture the result
		result = self.wcapi.post(endpoint,data)
		rs_code = result.status_code
		# then we get the body which is the main content
		# if its not json, below wont work
		rs_body = result.json()
		rs_url = result.url

		return [rs_code,rs_body,rs_url]

	def get(self,endpoint):
		'''

		:param endpoint:
		:param data:
		:return:
		'''

		result = self.wcapi.get(endpoint)

		rs_code = result.status_code
		rs_body = result.json()
		rs_url = result.url

		# the url is not so useful, but good for debugging
		return [rs_code,rs_body,rs_url]