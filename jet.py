import json
from requests import request

#base URL
base_url = 'https://merchant-api.jet.com/api'

class jet(object):
	#snakes on a plane
	def __init__(self, jet_user, jet_secret):
		self.auth_header = False
		params = { 
			"post_data":
				{
				"user":jet_user,
				"pass":jet_secret
				}
			}
		key_response = self.make_request("POST", "/token", **params)
		key = key_response['id_token'].encode()
		self.auth_header = {"Authorization":"Bearer %s" % key}

	def make_request(self, method, url, **kwargs):
		url = base_url + url
		if "post_data" in kwargs:
			post_data = kwargs['post_data']
			if self.auth_header:
				r = request(method, url, data=json.dumps(post_data), headers=self.auth_header)
			else:
				r = request(method, url, data=json.dumps(post_data))
		else:
			r = request(method, url, headers=self.auth_header)

		try:
			return json.loads(r.text)
		except ValueError:
			return r.text

	def get_ready_order_urls(self):
		endpoint = '/orders/ready'
		return self.make_request("GET", endpoint)['order_urls']

	def get_order_details_by_url(self, order_url):
		return self.make_request("GET", order_url)

	def ack_order(self, jet_order_id):
		ack_url = "/api/orders/%s/acknowledge" % jet_order_id
		#TO-DO: Fix post-data for order items. 
		#https://developer.jet.com/docs/acknowledge-order
		post_data = {
			"acknowledgement_status": "accepted", //this order will moved to the 'acknowledged' status
			"alt_order_id": "232145",
			"order_items": [
					{
						"order_item_acknowledgement_status": "fulfillable",
						"order_item_id": "8f5ae15b6b414b00a1b9d6ad99166a00",
						"alt_order_item_id": "76-i105"
					}
				]
			}
		return self.make_request("GET", ack_url, post_data)

	#def print_key(self):
	#	return self.auth_header


