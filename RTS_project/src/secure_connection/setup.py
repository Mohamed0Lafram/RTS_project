from setuptools import find_packages, setup

package_name = 'secure_connection'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools', 'cryptography'],
    zip_safe=True,
    maintainer='Team Secure Swarm',
    maintainer_email='team@secureSWARM.com',
    description='Security primitives: AES-GCM, RSA, HMAC, key management, IDS',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'generate_key = secure_connection.generate_key:main',
            'ids_node      = secure_connection.ids_node:main',
            'test_security = secure_connection.test:main',
        ],
    },
)
