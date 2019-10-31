# API Usage Documentation

## Authentication

We use Django Rest Framework's [Token Authentication](https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication). To send authenticated request, include something like

`Authorization: Token 5d16226988e80e8e8d4a3b595585f0da148549d2`

in the HTTP header.

## users app

* `POST /users/register`

  Required fields: username, password, phone_number, org

  Other fields: email

  Authorization: no

  Success: `201 Created`

* `POST /users/login`

  Required fields: username, password

  Authorization: no

  Success: `200 OK`

  Return values: token

* `POST /users/logout`

  Authorization: yes

  Success: `200 OK`

* `GET /users/pickup-locations`

  Authorization: yes

  Success: `200 OK`

  Return values: list of pickup location objects

* `GET /users/organizations`

  Authorization: no

  Success: `200 OK`

  Return values: list of organization objects