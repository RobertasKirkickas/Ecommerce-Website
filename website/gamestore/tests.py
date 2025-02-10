from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Games

class GamesTestCase(TestCase):
    def setUp(self):
        self.game = Games(
            game_title='Elden Ring',
            game_genre='RPG',
            game_platform='PC',
            game_price=60.00,
            game_quantity=10
        )

    def test_in_stock(self):
        self.game.game_quantity=5
        self.assertTrue(self.game.game_quantity)
        self.game.game_price=10
        self.assertTrue(self.game.game_quantity)
        self.game.game_quantity=0
        self.assertFalse(self.game.game_quantity)
        self.game.game_price =-0
        self.assertFalse(self.game.game_price)
        game1 = Games(game_price=10.00, game_quantity=5)
        self.assertEqual(game1.get_total_price(), 50.00)

        '''Test with game_price=20.00 and stock=2'''
        game2 = Games(game_price=20.00, game_quantity=2)
        self.assertEqual(game2.get_total_price(), 40.00)
    def test_clean_negative_price(self):
        '''Create an instance of Games with a negative price'''
        game = Games(game_price=-10.00, game_quantity=5)

        # Check if clean raises a ValidationError for negative price
        with self.assertRaises(ValidationError):
            game.clean()  # Call the clean method to validate

    def test_clean_negative_stock(self):
        # Create an instance of Games with a negative stock
        game = Games(game_price=10.00, game_quantity=-5)

        # Check if clean raises a ValidationError for negative stock
        with self.assertRaises(ValidationError):
            game.clean()  # Call the clean method to validate

    def test_clean_valid_price_and_stock(self):
        # Create an instance of MyBook with valid price and stock
        game = Games(game_price=10.00, game_quantity=5)

        # Ensure that clean doesn't raise any exception (valid values)
        try:
            game.clean()  # Call the clean method to validate
        except ValidationError:
            self.fail("clean() raised ValidationError unexpectedly!")
