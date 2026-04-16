from setuptools import find_packages, setup

package_name = 'secure_connection'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools', 'pycryptodome'],
    zip_safe=True,
    maintainer='mohamed',
    maintainer_email='mohamedlafram004@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            "generate_key = secure_connection.generate_key:main"
        ],
    },
)
