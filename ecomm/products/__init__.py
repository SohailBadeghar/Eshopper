# import os
# import braintree


# Merchant_ID ='f49w49kxcr7dhx3p'
# Public_Key='5g29t22hfk42zk2d'
# Private_Key='b252c6e805ae98e5735610fdb76eda8e'

# # Configuring the environment and API credentials
# # Source: https://developer.paypal.com/braintree/docs/start/hello-server/python
# gateway = braintree.BraintreeGateway(
#     braintree.Configuration(
#         braintree.Environment.Sandbox,
#         # merchant_id=str(os.getenv("BT_MERCHANT_ID")),
#         # public_key=str(os.getenv("BT_PUBLIC_KEY")),
#         # private_key=str(os.getenv("BT_PRIVATE_KEY"))
#          merchant_id=Merchant_ID,
#         public_key=Public_Key,
#         private_key=Private_Key
#     )
# )

# # pass client_token to your front-end
# def generate_client_token():
#     return str(gateway.client_token.generate())

# def transact(options):
#     return gateway.transaction.sale(options)

# def find_transaction(id):
#     return gateway.transaction.find(id)

