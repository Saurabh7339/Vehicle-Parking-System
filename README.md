# Vehicle-Parking-System


A Parking System API built with **FastAPI**, **SQLModel**, and **Alembic** to handle vehicle parking operations. This API allows users to record parking entries and exits by providing necessary details.

## Features

- Record vehicle parking entries and exits.
- Manage vehicle details like vehicle number, owner name, and parking type (entry or exit).
- Database operations powered by **SQLModel**.
- Schema migrations managed with **Alembic**.
- RESTful API implementation using **FastAPI**.

## API Endpoint

### `/parking`
Handles vehicle parking entries and exits.

#### **Request Type**
- `POST`

#### **Request Parameters**
The endpoint expects a JSON body with the following fields:

| Field          | Type   | Description                                 |
|-----------------|--------|---------------------------------------------|
| `vehicle_number` | `str`  | The vehicle's registration number.         |
| `name`          | `str`  | Name of the vehicle owner.                 |
| `parking_type`  | `str`  | Type of parking operation: `entry` or `exit`.|

#### **Example Request**

```json
{
  "vehicle_number": "MH12AB1234",
  "name": "John Doe",
  "parking_type": "entry"
}