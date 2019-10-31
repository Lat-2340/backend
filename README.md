# API Usage Documentation

## Authentication

We use Django Rest Framework's [Token Authentication](https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication). To send authenticated request, include something like

`Authorization: Token 5d16226988e80e8e8d4a3b595585f0da148549d2`

in the HTTP header.

## users app

* `/users/register`
    * `POST`

      Required fields: username, password, email, org

      Other fields: email

      Authorization: no

      Success: `201 Created`

* `/users/update/<str username>`
    * `GET`

      Authorization: yes

      Success: `200 OK`

      Return values: user object

    * `PUT`

      Required fields: username, password, email, org

      Authorization: yes

      Success: `200 OK`

      Return values: (updated) user object

    * `PATCH`

      Authorization: yes

      Success: `200 OK`

      Return values: (updated) user object

    * `DELETE`

      Authorization: yes

      Success: `204 No Content`

* `/users/login`
    * `POST`

      Required fields: username, password

      Authorization: no

      Success: `200 OK`

      Return values: token

* `/users/logout`
  * `POST`

    Authorization: yes

    Success: `200 OK`

* `/users/pickup-locations`
  * `GET`

    Authorization: yes

    Success: `200 OK`

    Return values: list of pickup location objects

* `/users/organizations`
  * `GET`

    Authorization: no

    Success: `200 OK`

    Return values: list of organization objects

## lostandfound app

* `/lostandfound/add-lost-item`
    * `POST`

      Required fields: features

      Authorization: yes

      Success: 201 CREATED

* `/lostandfound/add-found-item`
    * `POST`

      Required fields: features

      Authorization: yes

      Success: 201 CREATED

* `/lostandfound/get-items`
    * `GET`

      Authorization: yes

      Success: 200 OK

      Return values: an object containing a list of lost_items and a list of found_items submitted by the current logged-in user