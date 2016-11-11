[![Build Status](https://travis-ci.org/andela-dmigwi/A-BucketList.svg?branch=develop)](https://travis-ci.org/andela-dmigwi/A-BucketList)
[![Coverage Status](https://coveralls.io/repos/github/andela-dmigwi/A-BucketList/badge.svg?branch=develop)](https://coveralls.io/github/andela-dmigwi/A-BucketList?branch=develop)
[![CircleCI](https://circleci.com/gh/andela-dmigwi/A-BucketList/tree/develop.svg?style=svg)](https://circleci.com/gh/andela-dmigwi/A-BucketList/tree/develop)

### [A-BucketList]

Items to be put in a bucket are items that will need to be done by the owner in the near future.  

*"It is a list of all the goals you want to achieve, dreams you want to fulfill and life experiences you desire to experience before you die."*


| **Functionality** | **Method** | **Route** |
|:---------------------------------:|:------:|:---------------------------------------------------:|
| Logs a user in | POST | `/api/v1/auth/login` |
| Register a user | POST | `/api/v1/auth/register` |
| Create a new bucket list | POST | `/api/v1/bucketlists` |
| List all the created bucket lists | GET | `/api/v1/bucketlists/int:id` |
| Get single bucket list | GET | `/api/v1/bucketlists/int:id` |
| Update this bucket list | PUT | `/api/v1/bucketlists/int:id` |
| Delete this single bucket list | DELETE | `/api/v1/bucketlists/int:id` |
| Create a bucket list item | POST | `/api/v1/bucketlists/int:id/items` |
| Update a bucket list item | PUT | `/api/v1/bucketlists/int:id/items/int:id` |
| Delete a bucket list item | DELETE | `/api/v1/bucketlists/int:id/items/int:id` |

### A-BucketList Project Setup

-  **Installation:**
            1. Create a virtual environment by running the command.
            ``virtualenv --python=python3 venv-flask``

            2. Activate the virtualenv by running
            ``source venv-flask/bin/activate``

-  **Clone the repo**
            ``https://github.com/andela-dmigwi/A-BucketList.git``

- **Database setup**
Run the following commands:
           1. ``python manage.py db init``
           2. ``python manage.py db migrate``
           3. ``python manage.py db upgrade``

- **Launch the system**
Run the following commands:
            1. ``python manage.py runserver``

- **Run Tests**
Run : 
            1. tox

*The api's input is mainly a JSON file, apart from the login/registation section where form data can be passed*

### Register a User
This section allows a new user to be created:

            **Content-Type**: ``application/json`` or ``application/  x-www-form-urlencoded``
            **Valid Input**: ``{"username":"user1", "password":"pass1"}``
            **Expected Response**: 
                            - On success: Status Code 201
                            > {"Message" : "Registration successful"}
                            - On failure: status code 400
                            > {"Error" : "Your password or username is empty or wasn't found"}

### Login
This section allows a user to login:

            **Content-Type**: ``application/json`` or ``application/x-www-form-urlencoded``
            **Valid Input**: ``{"username":"user1", "password":"pass1"}``
            **Expected Response**: 
                            - On success: Status Code 201
                            >  {"Authorization" : "Bearer <your-token>"}
                            - On failure: status code 400
                            > {"Error" : "Your password or username is empty or wasn't found"}

### Create a New Bucket List
This section allows a new bucket list to be created:

            **Authorization**: ``Bearer <your-token>``
            **Content-Type**: ``application/json`` 
            **Valid Input**:  ``{"name": "BucketList 1"}``
            **Expected Response**: 
                            - On success: Status Code 200 OK
                            > {
                                  "created_by": "user1",
                                  "date_created": "2016-11-11 00:21:42",
                                  "date_modified": "2016-11-11 00:21:42",
                                  "id": 21,
                                  "item": [],
                                  "name": "BucketList 1"
                                }
                            - On failure: status code 400
                            > Bad Request  (*When no parameter is passed*)

### List all created bucket lists
This section allows all bucket list to be retrieved:

            **Authorization**: ``Bearer <your-token>``
            **Expected Response**: 
                            - On success: Status Code 200 OK
                            > {
                              "1": {
                                "created_by": "user1", 
                                "date_created": "2016-11-09 14:39:29", 
                                "date_modified": "2016-11-09 14:49:05", 
                                "id": 2, 
                                "item": [], 
                                "name": "That wasn't cool"
                                },
                              } 
                            - On failure: status code 400
                            > `{"Error" : "Your password or username is empty or wasn't found"}`  

### Get Single bucket list
This section allows a retreiving of a single bucket list:

            **Authorization**: ``Bearer <your-token>``
            **Expected Response**: 
                            - On success: Status Code 200 OK
                            >  {
                                    "created_by": "user1", 
                                    "date_created": "2016-11-09 14:45:40", 
                                    "date_modified": "2016-11-09 15:08:32", 
                                    "id": 10, 
                                    "item": [
                                      {
                                        "bucketlist_id": 10, 
                                        "date_created": "2016-11-09 15:08:32", 
                                        "date_modified": "2016-11-09 15:08:32", 
                                        "done": false, 
                                        "id": 7, 
                                        "name": "Clinton Win Postponed"
                                      }
                                    ], 
                                    "name": "She passed next to me"
                                  } 
                            - On failure: status code 400
                            > {"Error" : "Delete Failed: Bucketlist Id 1 was not found"

### Update this bucket list
This section allows a new user to be created:

            **Authorization**: ``Bearer <your-token>``
            **Content-Type**: ``application/json``
            **Valid input**: ``{"name": "edited bucketlist"}``
            **Expected Response**: 
                            - On success: Status Code 201
                            > {
                                "created_by": "user1", 
                                "date_created": "2016-11-09 14:39:29", 
                                "date_modified": "2016-11-09 14:49:05", 
                                "id": 2, 
                                "item": [], 
                                "name": "Editted bUcketlist"
                               } 
                            - On failure: status code 400
                            > {"Error" : "Update Failed: Bucketlist Id 1 was not found"  

### Delete this single bucket list
This section allows a single bucket list to be deleted:

            **Authorization**: ``Bearer <your-token>``
            **Expected Response**: 
                            - On success: Status Code 204
                            > 
                            - On failure: status code 400
                            > {"Error" : "Delete Failed: Bucketlist Id 1 was not found"  

### Create a bucket list item
This section allows a new bucket list item to be created:

            **Authorization**: ``Bearer <your-token>``
            **Content-Type**: ``application/json``
            **Valid input**: ``{"name":" new item"}``
            **Expected Response**: 
                            - On success: Status Code 201
                            > {
                                "bucketlist_id": 10, 
                                "date_created": "2016-11-09 15:08:32", 
                                "date_modified": "2016-11-09 15:08:32", 
                                "done": false, 
                                "id": 7, 
                                "name": "Clinton Win Postponed"
                             } 
                            - On failure: status code 400
                            > {"Error" : "Create Failed: Bucketlist Id 1 was not found" 
 
### Update a bucket list item
This section allows a bucket list item to be updated:

            **Authorization**: ``Bearer <your-token>``
            **Content-Type**: ``application/json``
            **Valid input**: ``{"name":" editted"}`` or ``{"name":"edit", "done":true}``
            **Expected Response**: 
                            - On success: Status Code 201
                            > {
                                "bucketlist_id": 10, 
                                "date_created": "2016-11-09 15:08:32", 
                                "date_modified": "2016-11-09 15:08:32", 
                                "done": false, 
                                "id": 7, 
                                "name": "Clinton Win Postponed"
                              } 
                            - On failure: status code 400
                            > {"Error" : "Update Failed: Bucketlist Id 1 was not found"  

### Delete a bucket list item
This section allows a bucket list to be deleted:

            **Authorization**: ``Bearer <your-token>``
            **Expected Response**: 
                            - On success: Status Code 204
                            > 
                            - On failure: status code 400
                            > {"Error" : "Delete Failed: Bucketlist Id 1 was not found"} 
                            
### Search                
Works the same way as a GET method only that an argument has been added to the url, parameter q with name to be searched is provided.

    Request
    GET http://localhost:5555/bucketlists?q=bucket1

    Response
    Bucket lists with the string “bucket1” in their name.


### Paginate
Works by providing a limit paramater that specify the number of items that should be retrieved

    Request
    GET http://localhost:5555/bucketlists?limit=20

    Response
    20 bucket list records belonging to the logged in user.

Done By
[Migwi Ndung'u](https://github.com/andela-dmigwi/A-BucketList)
@2016


