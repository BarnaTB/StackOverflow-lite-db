import os


class Config(object):
    """Main configuration class."""
    DEBUG = False
    SECRET = os.getenv('SECRET')
    DATABASE_URL = "postgresql://##password@localhost:5432/stackoverflow"


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True


class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    DEBUG = True
    TESTING = True
    DATABASE_URL = "postgresql://##password@localhost:5432/test_db"


class StagingConfig(Config):
    """Configurations for Staging."""
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


app_config = {
    'TESTING': TestingConfig,
    'STAGING': StagingConfig,
    'DEVELOPMENT': DevelopmentConfig,
    'PRODUCTION': ProductionConfig
}
