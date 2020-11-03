from unittest.mock import patch
import unittest
import GP1

class TestPostActionMarkAsTheAccepted(unittest.TestCase):

    def test_main(self):
        with patch('GP1.displayEndPostActionMenu') as done:
            done.return_value = "test over"
            with patch('GP1.connection') as connection:
                connection.commit = unittest.mock.MagicMock()
                with patch('GP1.cursor') as cursor:
                    cursor.execute = unittest.mock.MagicMock()
                    cursor.fetchone = unittest.mock.Mock()
                    cursor.fetchone.side_effect = [("p200","p100"), ("p100","")]
                    user = GP1.CurrentUser("u100")
                    GP1.PostActionMarkAsTheAccepted(user, "p200")
                    self.assertEqual(cursor.execute.call_args_list[0], unittest.mock.call('select * from answers where pid=?;', ['p200']))
                    self.assertEqual(cursor.execute.call_args_list[1], unittest.mock.call('select * from questions where pid=?;', ['p100']))
                    self.assertEqual(cursor.execute.call_args_list[2], unittest.mock.call('update questions set theaid=? where pid=?;', ['p200', 'p100']))
                    connection.commit.assert_called_once()


    @patch('builtins.input', lambda _ : '1')
    def test_overwrite_yes(self):
        with patch('GP1.displayEndPostActionMenu') as done:
            done.return_value = "test over"
            with patch('GP1.connection') as connection:
                connection.commit = unittest.mock.MagicMock()
                with patch('GP1.cursor') as cursor:
                    cursor.execute = unittest.mock.MagicMock()
                    cursor.fetchone = unittest.mock.Mock()
                    cursor.fetchone.side_effect = [("p200", "p100"), ("p100", "p300")]
                    user = GP1.CurrentUser("u100")
                    GP1.PostActionMarkAsTheAccepted(user, "p200")
                    print(cursor.execute.call_args_list)
                    self.assertEqual(cursor.execute.call_args_list, [unittest.mock.call('select * from answers where pid=?;', ['p200']), unittest.mock.call('select * from questions where pid=?;', ['p100']), unittest.mock.call('update questions set theaid=? where pid=?;', ['p200', 'p100'])])
                    connection.commit.assert_called_once()

    @patch('builtins.input', lambda _ : '2')
    def test_overwrite_no(self):
        with patch('GP1.displayEndPostActionMenu') as done:
            done.return_value = "test over"
            with patch('GP1.connection') as connection:
                connection.commit = unittest.mock.MagicMock()
                with patch('GP1.cursor') as cursor:
                    cursor.execute = unittest.mock.MagicMock()
                    cursor.fetchone = unittest.mock.Mock()
                    cursor.fetchone.side_effect = [("p200", "p100"), ("p100", "p300")]
                    user = GP1.CurrentUser("u100")
                    GP1.PostActionMarkAsTheAccepted(user, "p200")
                    print(cursor.execute.call_args_list)
                    self.assertEqual(cursor.execute.call_args_list, [unittest.mock.call('select * from answers where pid=?;', ['p200']), unittest.mock.call('select * from questions where pid=?;', ['p100'])])
                    connection.commit.assert_not_called()


if __name__ == "__main__":
    unittest.main()