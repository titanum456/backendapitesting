import string
import random
from datetime import datetime
import dbconnect

class Helper():
    """
    This is a class for function to be shared between test cases.
    Common tasks or tools go here.
    """

    qry = dbconnect.DBConnect()

    def __init__(self):
        pass

    # below paste from earilier file
    def generate_random_info(self):
        """
        This generates random strings. The strings generated are for email, username, first name and last name.

        :return: info - dictionary containing the randomly generted info
        """

        info = {}

        print("Generating random stings for email and user_namee")
        stamp = datetime.now().strftime("%Y%m%d%H%M%S")
        info['email'] = "api_user_" + stamp + "@gmail.com"
        info['user_name'] = "backend." + stamp

        print("Generating random strings for first_name and last_nam")
        all_letters = string.lowercase
        info['first_name'] = "".join(random.sample(all_letters, 8))
        info['last_name'] = "".join(random.sample(all_letters, 8))

        print("The generated email: {}".format(info['email']))
        print("The generated user name: {}".format(info['user_name']))
        print("The generated first name: {}".format(info['first_name']))
        print("The generated last name: {}".format(info['last_name']))

        return info

    # need to put self as you are in a class   *****

def get_customer_info_from_db_provided_customer_id(self,cust_id):
    """

    :return: 

    """

    customer_db_info = {}
    #get the cust id and some info from the ak_users table:
    sql = "SELECT user_login, user_nicename, user_email, display_name FROM wp165.ak_users WHERE ID = {};".format(cust_id)
    cust = qry.select('wp165',sql)

    print cust
    customer_db_info['user_login'] = cust[0][0]
    customer_db_info['user_nicename'] = cust[0][1]
    customer_db_info['user_email'] = cust[0][2]
    customer_db_info['display_name'] = cust[0][3]

    # get customers metadata from he 'ak usermeta' table
    sql = "SELECT meta_key, meta_value FROM wp165.ak_usermeta WHERE user_id = {};".format(cust_id)
    cust_meta = qry.select('wp165',sql)
    
    # lets add all the user meta data to the customer_db_info dictionary
    for row in cust_meta:
        customer_db_info[row[0]] = row[1]
        
    return customer_db_info

    # print cust_meta
    print customer_db_info
