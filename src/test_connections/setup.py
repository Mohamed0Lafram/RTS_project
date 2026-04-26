from setuptools import find_packages, setup

package_name = 'test_connections'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='mohamed',
    maintainer_email='mohamedlafram004@gmail.com',
    description='TODO: Package description',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'talker   = test_connections.two_nodes_no_security.talker:main',
            'listener = test_connections.two_nodes_no_security.listener:main',
            's_talker   = test_connections.two_nodes_with_security.s_talker:main',
            's_listener = test_connections.two_nodes_with_security.s_listener:main',
            'ghost_listener = test_connections.two_nodes_with_security.ghost_listener:main',
            'ghost_talker = test_connections.two_nodes_with_security.ghost_talker:main'
        ]
    },
)
