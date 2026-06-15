from setuptools import find_packages, setup

package_name = 'my_robot_controller'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Team Secure Swarm',
    maintainer_email='team@secureSWARM.com',
    description='Robot controller nodes with secure and unsecure communication',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'talker_secure   = my_robot_controller.talker_secure:main',
            'listener_secure = my_robot_controller.listener_secure:main',
            'talker_unsecure   = my_robot_controller.talker_unsecure:main',
            'listener_unsecure = my_robot_controller.listener_unsecure:main',
            'attacker_node = my_robot_controller.attacker_node:main',
            'first_node    = my_robot_controller.first_node:main',
        ],
    },
)
