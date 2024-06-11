import unittest
from unittest.mock import MagicMock, patch
from UserInteraction import *


class TestUserInteraction(unittest.TestCase):
    def setUp(self):  # set up a user interaction class.
        self.user_interaction = UserInteraction()
        self.valid_zipcode = '50023'
        self.invalid_zipcode = '12345'

    @patch('UserInteraction.requests')  # Mock requests to avoid an actual API call
    def test_validPostalCode_valid(self, mock_requests):
        # Simulate a successful API response
        mock_response = MagicMock()
        mock_response.json.return_value = {'location': {'name': 'Ankeny'}}
        mock_requests.get.return_value = mock_response

        # self.user_interaction.zipcode = self.valid_zipcode
        result = self.user_interaction.validPostalCode()
        self.assertTrue(result)

    @patch('UserInteraction.requests')  # Mock requests to avoid an actual API call
    def test_validPostalCode_invalid(self, mock_requests):
        # Simulate an API response with an error
        mock_response = MagicMock()
        mock_response.json.return_value = {'error': {'code': 1006, 'message': 'Invalid location'}}
        mock_requests.get.return_value = mock_response

        self.user_interaction.zipcode = self.invalid_zipcode
        result = self.user_interaction.validPostalCode()
        self.assertFalse(result)

    @patch('builtins.input', return_value='historic')  # patch input to return 'historic'
    def test_promptCrrentOrHistoric_historic(self, mock_input):
        result = self.user_interaction.promptCrrentOrHistoric()
        self.assertFalse(result)

    @patch('builtins.input', return_value='current')  # patch input to return 'current'
    def test_promptCrrentOrHistoric_current(self, mock_input):
        result = self.user_interaction.promptCrrentOrHistoric()
        self.assertTrue(result)

    @patch('builtins.input', return_value='foo,bar')  # patch input to return an invalid response
    def test_promptCrrentOrHistoric_invalid(self, mock_input):
        result = self.user_interaction.promptCrrentOrHistoric()
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
