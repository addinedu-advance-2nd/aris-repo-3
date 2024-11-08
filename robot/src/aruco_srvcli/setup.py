from setuptools import find_packages, setup

package_name = 'aruco_srvcli'

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
    maintainer='d',
    maintainer_email='kjw990204@gmail.com',
    description='aruco client server',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'aruco_server = aruco_srvcli.aruco_server:main',
            'aruco_client = aruco_srvcli.aruco_client:main',
        ],
    },
)
