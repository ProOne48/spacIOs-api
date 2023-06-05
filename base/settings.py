from glob import glob

from dynaconf import Dynaconf, Validator


def load_validations(settings_obj):

    validators = [
        Validator(
            'DB_HOST', 'APP_NAME', 'OPENAPI_CONFIG', 'SECRET_KEY',
            'API_BASE_NAME', 'ENABLE_CORS', 'DB_NAME', 'DB_PORT', 'DB_USER', 'DB_PASSWORD', must_exist=True
        )
    ]

    settings_obj.validators.register(*validators)
    settings_obj.validators.validate()

    return settings_obj


CONFIG_DIR = 'configs'  # folder of configuration files

settings_files = glob(f'{CONFIG_DIR}/settings.*') + \
                 glob(f'{CONFIG_DIR}/*_config.*') + \
                 glob(f'{CONFIG_DIR}/.secrets.*')

settings = Dynaconf(
    settings_files=settings_files,
    environments=True,
    env_switcher='ENV_MODE',
    load_dotenv=False
)

settings = load_validations(settings)
