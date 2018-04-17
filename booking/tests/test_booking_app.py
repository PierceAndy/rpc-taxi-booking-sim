from django.test import SimpleTestCase
import json


class TestBookingApp(SimpleTestCase):

    def setUp(self):
        self.book_url = '/api/book/'
        self.tick_url = '/api/tick/'
        self.reset_url = '/api/reset/'
        self.client.post(self.reset_url)

        self.encoding = 'utf-8'
        self.json_content_type = "application/json"
        self.html_content_type = "text/html"

        self.raw_json_data = {'source': {'x': 1, 'y': 2}, 'destination': {'x': 3, 'y': 4}}
        self.json_data = json.dumps(self.raw_json_data)

    # /api/book/
    def test_booking_app_for_valid_book_http_post_request(self):
        response = self.client.post(self.book_url,
                                    data=self.json_data,
                                    content_type=self.json_content_type)
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.encoding, response.charset)
        self.assertEqual(self.json_content_type,
                         response.__getitem__("content-type"))

        expected_response_content = {'car_id': 1, 'total_time': 7}
        actual_response_content = json.loads(response.content,
                                             encoding=response.charset)
        self.assertEqual(expected_response_content, actual_response_content)

    def test_booking_app_for_invalid_book_http_get_request_method(self):
        response = self.client.get(self.book_url)
        self.assertEqual(405, response.status_code)

    def test_booking_app_for_invalid_book_http_put_request_method(self):
        response = self.client.put(self.book_url)
        self.assertEqual(405, response.status_code)

    def test_booking_app_for_book_invalid_html_content_type(self):
        response = self.client.post(self.book_url,
                                    data=self.json_data,
                                    content_type=self.html_content_type)
        self.assertEqual(415, response.status_code)
        expected_response_content \
            = "Expected Content-Type: application/json\n" \
              + "Received Content-Type: {}".format(self.html_content_type)
        self.assertEqual(expected_response_content,
                         response.content.decode(response.charset))

    def test_booking_app_for_book_invalid_json_data(self):
        response = self.client.post(self.book_url,
                                    data=self.raw_json_data,
                                    content_type=self.json_content_type)
        self.assertEqual(400, response.status_code)
        self.assertEqual("Error decoding JSON data",
                         response.content.decode(response.charset))

    def test_booking_app_for_book_invalid_booking_locations(self):
        raw_json_data = {'source': {'x': 1, 'y': 2},
                         'destination': {'x': 1, 'y': 2}}
        json_data = json.dumps(raw_json_data)
        response = self.client.post(self.book_url,
                                    data=json_data,
                                    content_type=self.json_content_type)

        self.assertEqual(204, response.status_code)
        self.assertEqual(self.encoding, response.charset)
        self.assertEqual("", response.content.decode(response.charset))

    def test_booking_app_for_book_no_free_taxis(self):
        # Book first taxi
        response = self.client.post(self.book_url,
                                    data=self.json_data,
                                    content_type=self.json_content_type)
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.encoding, response.charset)
        self.assertEqual(self.json_content_type,
                         response.__getitem__("content-type"))

        expected_response_content = {'car_id': 1, 'total_time': 7}
        actual_response_content = json.loads(response.content,
                                             encoding=response.charset)
        self.assertEqual(expected_response_content, actual_response_content)

        # Book second taxi
        response = self.client.post(self.book_url,
                                    data=self.json_data,
                                    content_type=self.json_content_type)
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.encoding, response.charset)
        self.assertEqual(self.json_content_type,
                         response.__getitem__("content-type"))

        expected_response_content = {'car_id': 2, 'total_time': 7}
        actual_response_content = json.loads(response.content,
                                             encoding=response.charset)
        self.assertEqual(expected_response_content, actual_response_content)

        # Book third taxi
        response = self.client.post(self.book_url,
                                    data=self.json_data,
                                    content_type=self.json_content_type)
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.encoding, response.charset)
        self.assertEqual(self.json_content_type,
                         response.__getitem__("content-type"))

        expected_response_content = {'car_id': 3, 'total_time': 7}
        actual_response_content = json.loads(response.content,
                                             encoding=response.charset)
        self.assertEqual(expected_response_content, actual_response_content)

        # Book fourth taxi
        response = self.client.post(self.book_url,
                                    data=self.json_data,
                                    content_type=self.json_content_type)
        self.assertEqual(204, response.status_code)
        self.assertEqual(self.encoding, response.charset)
        self.assertEqual("", response.content.decode(response.charset))

    def test_booking_app_for_valid_book_32_bit_int_limits(self):
        min_int = -2147483648
        max_int = 2147483647
        raw_json_data = {'source': {'x': min_int, 'y': min_int},
                         'destination': {'x': max_int, 'y': max_int}}
        json_data = json.dumps(raw_json_data)
        response = self.client.post(self.book_url,
                                    data=json_data,
                                    content_type=self.json_content_type)
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.encoding, response.charset)
        self.assertEqual(self.json_content_type,
                         response.__getitem__("content-type"))

        expected_response_content = {'car_id': 1, 'total_time': 12884901886}
        actual_response_content = json.loads(response.content,
                                             encoding=response.charset)
        self.assertEqual(expected_response_content, actual_response_content)

    # /api/tick/
    def test_booking_app_for_valid_tick_http_post_request(self):
        response = self.client.post(self.tick_url)
        self.assertEqual(204, response.status_code)

    def test_booking_app_for_invalid_tick_http_put_request(self):
        response = self.client.put(self.tick_url)
        self.assertEqual(405, response.status_code)

    def test_booking_app_for_invalid_tick_http_get_request_method(self):
        response = self.client.get(self.tick_url)
        self.assertEqual(405, response.status_code)

    # /api/reset/
    def test_booking_app_for_valid_reset_http_post_request(self):
        response = self.client.post(self.reset_url)
        self.assertEqual(204, response.status_code)

    def test_booking_app_for_invalid_reset_http_get_request_method(self):
        response = self.client.get(self.reset_url)
        self.assertEqual(405, response.status_code)

    def test_booking_app_for_invalid_reset_http_put_request_method(self):
        response = self.client.put(self.reset_url)
        self.assertEqual(405, response.status_code)
