import req
import dbconnect

import json

rq = req.REQ()
qry = dbconnect.DBConnect()

def create_a_product():
	'''

	:return:
	'''

	# here we set it to global as later can use in the function below   ##very important
	global product_id
	global title
	global price

	# below is how the payload will look like:
	title =  'TEST1 TITLE'
	price = '9.99'

	input_data = {
					'product':{
						'title':title,
						'type':'simple',
						'regular_price':price}}
	info = rq.post('products',input_data)			# notice its called products by default
	response_code =  info[0]   			# 1st element is response code
	response_body =  info[1]  			

	# now we want to make sure response code is 201
	assert response_code == 201, "The status code returned creating product is not as " \
								 "expected. Expected: 201, Actual: {act}".format(act=response_code)
	rs_title = response_body['product']["title"]
	rs_price = response_body["product"]["regular_price"]
	product_id = response_body["product"]["id"]

	print 'id is: {}'.format(product_id)

	assert rs_title == title, "The title in response is not same as in request." \
							  "The response title is: {}".format(rs_title)        

	assert rs_price == price, "The price in response did not match." \
							  "Expected: {}, Actual, {}".format(price, rs_price)            
	print 'The create_product test PASS'

def test_verify_product_created_in_db():
    """
    Function to query the data base and verify product is created with the correct information.

    Note:
        This function depends on the first function 'test_create_a_product()' being called first. The variables
        set in that function are used in this function.
    """

    print "Querying the database to get product information"
    sql ='''SELECT p.post_title, p.post_type, pm.meta_value FROM ak_posts p JOIN ak_postmeta pm
            ON p.id=pm.post_id WHERE p.id={} AND pm.meta_key='_regular_price' '''.format(product_id)
    qrs = qry.select('wp165', sql)

    # extracting the data
    db_title = qrs[0][0]
    db_type = qrs[0][1]
    db_regular_price = qrs[0][2]

    print "Verifying the product title"
    assert db_title == title, "The tile in db is not as expected. DB title: {}, Expected: {}".format(db_title, title)

    print "Verifying the post_type"
    assert db_type == 'product', "The post_type in DB is not 'product'. Expected: 'product', Actual: {}".format(db_type)

    print "Verifying the product regular price"
    assert db_regular_price == price, "The regular price in db is not as expected. Expected: {}, Actual: {}".format(price, db_regular_price)

    print "'products positive tc, verify product created in db, PASS"

create_a_product()
test_verify_product_created_in_db()