# Project2_TCP

Partners (RUID)(NETID): Aditya Dhami (ad1409) Sebastian Gil-Avendano (sg1397)
1. Are there known issues or functions that aren't working currently in your
   attached code? If so, explain. (note that you will get half credit for any reasonably sized bug that is fully explained in the readme)
   As the code is running optimially and and is returning the correct code. To the best of our knowledge, there is nothing wrong with the project and it is experiencing no problems. 
   
2. What problems did you face developing code for this project? Around how long did you spend on this project (This helps me decide what I need to explain more clearly for the next projects)
    The problems that the group has encountered was setting the the structure of the program. At first we needed to find out how we were going to hold the ack, and required flags to determine if transmission was successful. After fully implementing a struct, a question that arised was how to implement a resubmission. It was known that after 3 continuous returns of the same ack will cause a transmission. It was a topic that was addressed over a span of several days. The project took will over a day, cumulative.
    
5. Why is stop and wait much faster?
Stop and wait is much faster as it is due to the accuracy. In the project, we did not experience packet loss and drops during the development. While in cumulative ack we were having various problems regarding packet loss. This is because Stop and Wait ensures the sending of the packet before sending another packet. This allows the code to be more efficient and run quicker.
  
