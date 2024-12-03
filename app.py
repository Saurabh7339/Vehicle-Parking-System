from datetime import date, datetime
from fastapi import FastAPI,Request,Depends, HTTPException
# from models.common import User
from sqlalchemy import desc
from sqlalchemy.orm import Session
from pydantic import BaseModel, PositiveInt
from sqlmodel import SQLModel
from models.database import get_db, Base, engine,User,Parking, init_db


class UserCreate(BaseModel):
    name: str
    email: str
    age: int

class ParkingCreate(BaseModel):
    name: str
    vehicle_number: str
    # name: str
    parking_type : str



app = FastAPI()
@app.on_event("startup")
def on_startup():
    init_db()
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI"}


@app.post("/items")
async def create_item(request:Request):
    req_body = await request.json()     
    print(req_body)
    values  = User(**req_body)
    return values

@app.get("/user/")
def get_users(db: Session = Depends(get_db)):
    # print(db)
    return db.query(User).all()

@app.post("/user/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = User(name=user.name, email=user.email, age=user.age)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)  # Refresh to get the generated ID
        return {"id": db_user.id, "name": db_user.name, "email": db_user.email, "age": db_user.age}
    except Exception as e:
        print("Error Occured",str(e))
        raise HTTPException(status_code=400, detail=f"Error Occured while creating the user,{e}")

@app.post("/parking/")
def create_user(parking: Parking, db: Session = Depends(get_db)):
    try:
        PARKING_SIZE_LIMIT = 5
        current_datetime = datetime.now()
        parked_vehicle = db.query(Parking).filter(Parking.vehicle_number==parking.vehicle_number).order_by(desc(Parking.time_in)).first()
        if parked_vehicle:
            print(parked_vehicle.time_in,parked_vehicle.time_out)
        if parking.parking_type=="entry":
            today_start = datetime.combine(date.today(), datetime.min.time())
            today_end = datetime.combine(date.today(), datetime.max.time())
            todays_parked_vehicles = db.query(Parking).filter(
            Parking.time_in >= today_start, Parking.time_in <= today_end , Parking.time_out==None
            ).all()
            print("todays parked vehicles ",len(todays_parked_vehicles)) 
            if len(todays_parked_vehicles)==5:
                raise HTTPException(
                        status_code=400, 
                        detail="Parking limit is Reached , please park it somewhere else , but please follow the parking rules."
                    )  
            # return {"hey":"checking"}
            if parked_vehicle:
                if parked_vehicle.time_out==None:
                    raise HTTPException(
                        status_code=400, 
                        detail="Vehicle is already parked and cannot be parked again."
                    )  
            # parked_time = current_datetime.strptime("%Y-%m-%d %H:%M")
            new_parking = Parking(vehicle_number=parking.vehicle_number, time_in=current_datetime, name= parking.name)
            db.add(new_parking)
            db.commit()
            db.refresh(new_parking)

            return {
                "message":"your vehicle has been successfully parked",
                "details":[{"id": new_parking.id,
                "vehicle_number": new_parking.vehicle_number,
                "time_in": new_parking.time_in}]
                
            }
        elif parking.parking_type=="exit":
            if not parked_vehicle:
                raise HTTPException(
                    status_code=404,
                    detail=f"No parking record found for vehicle number {parking.vehicle_number}"
                )
            print("yes Vehicle is already parked")
            if parked_vehicle.time_out!=None:
                raise HTTPException(
                    status_code=404,
                    detail=f"{parking.vehicle_number}, this vehicle has already left the parking area"
                )
            parked_vehicle.time_out= current_datetime
            db.commit()
            db.refresh(parked_vehicle)
            return {
            "message": "Exit time updated successfully",
            "data": {
                "vehicle_number": parked_vehicle.vehicle_number,
                "time_in": parked_vehicle.time_in,
                "time_out": parked_vehicle.time_out,
                "name": parked_vehicle.name,
                "parking_type": parked_vehicle.parking_type,
            },
        }
            



    except Exception as e:
        print("Error Occurred:", str(e))
        raise HTTPException(status_code=500, detail=f"Error Occurred: {str(e)}")
    


@app.get("/parking/today")
def get_vehicles_parked_today(db: Session = Depends(get_db)):
    try:
        today_start = datetime.combine(date.today(), datetime.min.time())
        today_end = datetime.combine(date.today(), datetime.max.time())
        parked_vehicles = db.query(Parking).filter(
            Parking.time_in >= today_start, Parking.time_in <= today_end
        ).all()

        if not parked_vehicles:
            return {"message": "No vehicles parked today"}
        results = [
            {
                "vehicle_number": vehicle.vehicle_number,
                "name": vehicle.name,
                "time_in": vehicle.time_in,
                "time_out": vehicle.time_out,
                "parking_type": vehicle.parking_type,
            }
            for vehicle in parked_vehicles
        ]

        return {"message": "Vehicles parked today", "data": results}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error Occurred: {e}")



if __name__ == "__main__":
    print("Creating tables...")
    SQLModel.metadata.drop_all(bind=engine)
    SQLModel.metadata.create_all(engine)
    print("Tables created successfully!")

