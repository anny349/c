from django.test import TestCase
from singletons.logger_singleton import LoggerSingleton

class SingletonTests(TestCase):
    def test_logger_singleton(self):
        logger1 = LoggerSingleton().get_logger()
        logger2 = LoggerSingleton().get_logger()
        self.assertIs(logger1, logger2)  # Ensure Singleton behavior

        logger1.info("This is a test log message.")
        logger2.warning("This is a warning message.")

        print("✅ LoggerSingleton test passed! Logs should appear above.")