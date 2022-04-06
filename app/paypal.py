from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
from paypalcheckoutsdk.orders import OrdersGetRequest, OrdersCaptureRequest
from decouple import config


class PayPalClient:
    def __init__(self):
        self.client_id = config('PAYPAL_CLIENT_ID')
        self.client_secret = config('PAYPAL_SECRET_ID')

        self.environment = SandboxEnvironment(
            client_id=self.client_id, client_secret=self.client_secret)

        self.client = PayPalHttpClient(self.environment)

    def object_to_json(self, json_data):
        result = {}

        itr = json_data.__dict__.items()
        for key, value in itr:
            if key.startswith("__"):
                continue
            result[key] = self.array_to_json_array(value) if isinstance(value, list) else\
                self.object_to_json(value) if not self.is_primittive(value) else\
                value
        return result

    def array_to_json_array(self, json_array):
        result = []
        if isinstance(json_array, list):
            for item in json_array:
                result.append(self.object_to_json(item) if not self.is_primittive(item)
                              else self.array_to_json_array(item) if isinstance(item, list) else item)
        return result

    def is_primittive(self, data):
        return isinstance(data, str) or isinstance(data, int)


# Obtener los detalles de la transacción
class GetOrder(PayPalClient):

    def get_order(self, order_id):
        request = OrdersGetRequest(order_id)
        response = self.client.execute(request)
        return response


class CaptureOrder(PayPalClient):

    def capture_order(self, order_id, debug=False):
        request = OrdersCaptureRequest(order_id)
        response = self.client.execute(request)
        if debug:
            print('Status Code: ', response.status_code)
            print('Status: ', response.result.status)
            print('Order ID: ', response.result.id)
            print('Links: ')
            for link in response.result.links:
                print('\t{}: {}\tCall Type: {}'.format(
                    link.rel, link.href, link.method))
            print('Capture Ids: ')
            for purchase_unit in response.result.purchase_units:
                for capture in purchase_unit.payments.captures:
                    print('\t', capture.id)
            print("Buyer:")
        return response