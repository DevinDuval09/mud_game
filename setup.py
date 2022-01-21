from setuptools import setup

setup(
        name='MUD_game',
        version='0.0.1',
        author='Devin Duval',
        author_email='DevinDuval09@gmail.com',
        package_dir={'':'.'},
        packages=['MUD_game', 'MUD_game.client', 'MUD_game.server'],
        package_data={"":['*.css', '*.js', '*.html', '*.tsx', '*.jsx']},
        include_package_data=True,
        install_requires=['pymongo'],
        entry_points={'console_scripts': ['MUD_game=game_server:main']},
        )
