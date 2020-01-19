import unittest
import birthdaybot
from datetime import datetime, date, timedelta
import os
from config import basedir
from app import app, db
from app.models import User

class TestBirthdaybot(unittest.TestCase):

    def setUp(self):
        '''
        crate test database
        '''
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        '''
        clean database after test
        '''
        db.session.remove()
        db.drop_all()

    def test_bad_date(self):
        '''
        check for bad date format exception
        '''
        with self.assertRaises(ValueError):
            birthdaybot.check_date('1988-03-088')
        self.assertTrue('Bad date format, should be YYYY-MM-DD')

    def test_future_date(self):
        '''
        check for date in the future exception
        '''
        with self.assertRaises(ValueError):
            birthdaybot.check_date('2988-03-08')
        self.assertTrue("You can't be born in the future!")

    def test_date_return(self):
        '''
        check that function returns correct date back
        '''
        t_date = birthdaybot.check_date(str(datetime.now().date()))
        self.assertEqual(t_date, str(datetime.now().date()))

    def test_user_exists(self):
        '''
        test if user_exists func returns true when user is already in the database
        '''
        u = User(name='Anton', b_date='08-03-1988')
        db.session.add(u)
        db.session.commit()
        self.assertTrue(birthdaybot.user_exists('Anton'))

    def test_save_to_db(self):
        '''
        check update and get user
        '''
        birthdaybot.save_to_db('Anton', '08-03-1988')
        db.session.commit()
        result1 = str(User.query.filter_by(name = 'Anton').first())
        birthdaybot.save_to_db('Anton', '12-12-1900')
        db.session.commit()
        result2 = str(User.query.filter_by(name = 'Anton').first())
        self.assertNotEqual(result1, result2)

    def test_get_user_birthday(self):
        '''
        check that exception is raised on unknown user error
        '''
        with self.assertRaises(ValueError):
            birthdaybot.get_user_birthday('test')
        self.assertTrue('no such user, please add')

    def test_make_resp(self):
        '''
        check that function returns correct days count
        '''
        new_day = datetime.now().date() + timedelta(days=42)
        birthdaybot.save_to_db('Anton', new_day)
        db.session.commit()
        resp = birthdaybot.make_resp('Anton')
        self.assertEqual('Hello, Anton! Your birthday is in 42 day(s)', resp)


if __name__ == '__main__':
    import xmlrunner
    runner = xmlrunner.XMLTestRunner(output='test-reports')
    unittest.main(testRunner=runner)
    unittest.main()
