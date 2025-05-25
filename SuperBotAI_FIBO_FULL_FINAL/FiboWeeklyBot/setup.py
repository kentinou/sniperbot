
from setuptools import setup, find_packages

setup(
    name='fibo_weekly_bot',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'requests',
        'matplotlib',
        'ta',
        'python-dotenv'
    ],
    entry_points={
        'console_scripts': [
            'fibo-bot=main_loop:run'
        ]
    },
    author='SuperBotAI',
    description='Bot de trading basé sur Fibonacci hebdomadaire avec alerte Telegram et suivi automatique.',
    include_package_data=True
)
