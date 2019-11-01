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

* `/lostandfound/lost-items`
    * `POST`

      Required fields: feature_color, feature_size, feature_category, date, location_lat, location_long

      Optional fields: description

      Authorization: yes

      Success: 201 CREATED

    * `GET`

      Authorization: yes

      Success: 200 OK

      Return values: list of lost items the request user posted

* `/lostandfound/update-lost-item/<int pk>`

    * `GET`

      Authorization: yes

      Success: `200 OK`

      Return values: lost item object

    * `PUT`

      Required fields: feature_color, feature_size, feature_category, date, location_lat, location_long

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

* `/lostandfound/found-items`

    Similar to `/lostandfound/lost-items`

* `/lostandfound/update-found-item/<int pk>`

    Similar to `/lostandfound/update-lost-item/<int pk>`