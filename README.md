[![Build Status](https://travis-ci.org/engineer47/code-rumble.svg)](https://travis-ci.org/engineer47/code-rumble)
[![Coverage Status](https://coveralls.io/repos/engineer47/code-rumble/badge.svg?branch=develop&service=github)](https://coveralls.io/github/engineer47/code-rumble?branch=develop)

# BW Shipping Portal
This portal was designed with the specific role of bridging the gap between the small scale 
shipping/goods transport business man and the customer who usually has difficulties getting their
goods to and from a place. This was apart of the requirement during the Code Rumble 2016 Hackathon.

# Design And Implementation
The portal was designed and implemented using python in combination with the django framework
(also python based). 

# Log In And User Creation
The system allows the user to log in with a pre-existing username and password or create an account
with email verification, during the account creation the user is required to specify their role in the
system, either Shipper who may also be referred to as the Carrier and the Individual whom in this scenario
refers to a person requiring shipping of their goods.
NB: Please note that as a future extension, the individual could also serve the role of the Shipper and the 
Shipper could also refer to a company.

# General Workflow
Once the both entities have identified their role in the system then the Individual, being the sender of the goods or cargo
can add a Job to the system, the Job describes the process of adding information defining the cargo to the system, and either
allowing the Carriers to competitively bid for the transport of the cargo or assign the Cargo to the Carrier of their choice, the payment for the
shipment is put on hold/pending until the cargo is delivered. The job is assigned different statuses in the system, from the point it is defined in the system to the point where it is delivered at the destination.

Future Extension: The Carrier could be rated based on the number of successful jobs completed.
Carriers could also be made available to the Individual based on the type of cargo to be shipped, e.g. Hazardous Materials, Perishables e.t.c.

Once a job has been assigned, the carrier will collect and transport the shipment to its designated destination. During the shipping period, the 
Individual will have access tracking of the goods through most conveniently, a tracking device in the Truck/Vehicle transporting the cargo. This data will be plotted to on a Google Map, available in the system. When the shipment has been safely delivered and verified, the payment process can now
be completed.

Adding to the scope: The recipient of the shipment could also be a player in the system act as the entity that completes the verification of the
goods once they are delivered, BUT the Individual that shipped the goods could also be the same person that receives and verifies. 

# Profile Management
The user has the freedom to manage their account by updating information about their account, this includes but is not limited to; changing of
passwords.

# Administration
The administration of the system can be done with the help of the Django framework which is very robust and highly customizable. Through framework the System Administrator has the ability to enable and disable users, allocate roles, generate reports, query records in all the tables, including all transactions and payments in the database, maintain the 
