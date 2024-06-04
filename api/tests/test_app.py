import unittest
from unittest.mock import patch, MagicMock
from app import app


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        app.testing = True

    
    def test_get_venue(self):
        response = self.app.get('/venues/1')

        self.assertEqual(response.status_code, 200)

        expected_data = {
            "bbox": "{\"type\":\"Polygon\",\"crs\":{\"type\":\"name\",\"properties\":{\"name\":\"EPSG:27700\"}},\"coordinates\":[[[518013,182241],[520015,182241],[520015,183241],[518013,183241],[518013,182241]]]}",
            "capacity": 12500,
            "venue_id": 1,
            "venue_name": "Wembley Arena"
        }

        self.assertEqual(response.json, expected_data)
    

    def test_get_venue_with_nonexistant_id(self):
        # GET request to /venues with invalid data
        response = self.app.get(f'/venues/99999')
        
        self.assertEqual(response.status_code, 404)

        expected_error = {"error": "Venue not found"}
        self.assertEqual(response.json, expected_error)


    @patch('app.get_conn')
    def test_add_venue_with_name(self, mock_get_conn):
        mock_conn = MagicMock()
        mock_result = MagicMock()
        mock_result.fetchone.return_value = [1]
        mock_conn.execute.return_value = mock_result
        mock_get_conn.return_value = mock_conn

        data = {
            "venue_name": "Test Venue",
            "bbox": '{"type": "Polygon", "coordinates": [[[0,0], [0,1], [1,1], [1,0], [0,0]]]}',
            "capacity": 100
        }

        response = self.app.post('/venues/', json=data)

        self.assertEqual(response.status_code, 201)
        response_json = response.get_json()
        self.assertEqual(response_json["venue_name"], "Test Venue")
        self.assertEqual(response_json["bbox"], data["bbox"])
        self.assertEqual(response_json["capacity"], 100)


    @patch('app.get_conn')
    def test_add_venue_without_name(self, mock_get_conn):
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn

        data = {
            "bbox": '{"type": "Polygon", "coordinates": [[[0,0], [0,1], [1,1], [1,0], [0,0]]]}',
            "capacity": 100
        }

        response = self.app.post('/venues/', json=data)

        self.assertEqual(response.status_code, 400)
        response_json = response.get_json()
        self.assertIn("Venue name is required", response_json["error"])


    def test_get_performing_artists(self):
        response = self.app.get('/performing-artists/2')

        self.assertEqual(response.status_code, 200)

        expected_data = [
            {
                "artist_name": "Dua Lipa"
            }
        ]

        self.assertEqual(response.json, expected_data)


    def test_get_performing_artists_404(self):

        response = self.app.get('/performing-artists/404')

        self.assertEqual(response.status_code, 404)

        expected_data = {"error": "Event not found or no artists associated with this event"}

        self.assertEqual(response.json, expected_data)


if __name__ == '__main__':
    unittest.main()