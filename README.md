# Nav2 Create 3
This is a minimal repository that spins up the nav2 stack for use on the Create 3 setups in the lab. NOTE: it depends on the base nav2. Currently, the only modifications this adds to nav2 are the implementations of nav2_bringup package, specifically allowing for topic renaming for the /odom topic for the controller_server and a self-contianed composable navigation_bringup.launch.

See the [nav2 repo](https://github.com/ros-navigation/navigation2) for more information: 
