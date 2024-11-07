# src/friends.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas, crud, database

router = APIRouter()

@router.post("/create_friends/", response_model=schemas.Friend)
def add_friend(friend: schemas.FriendCreate, db: Session = Depends(database.get_db)):
    return crud.create_friend(db=db, friend=friend)

@router.post("/send_friend_requests/", response_model=schemas.FriendRequest)
def send_friend_request(request: schemas.FriendRequestCreate, db: Session = Depends(database.get_db)):
    return crud.create_friend_request(db=db, request=request)

@router.get("/get_friends/{user_id}", response_model=list[schemas.Friend])
def get_user_friends(user_id: int, db: Session = Depends(database.get_db)):
    return crud.get_friends(db=db, user_id=user_id)

@router.get("/get_friend_requests/{user_id}", response_model=list[schemas.FriendRequest])
def get_user_friend_requests(user_id: int, db: Session = Depends(database.get_db)):
    return crud.get_friend_requests(db=db, user_id=user_id)

@router.put("/update_friend_requests/{request_id}", response_model=schemas.FriendRequest)
def update_friend_request(request_id: int, status: str, db: Session = Depends(database.get_db)):
    updated_request = crud.update_friend_request_status(db=db, request_id=request_id, status=status)
    if not updated_request:
        raise HTTPException(status_code=404, detail="Request not found")
    if status == "accepted":
        crud.create_friend(
            db=db,
            friend=schemas.FriendCreate(
                user_id=updated_request.receiver_id,
                friend_id=updated_request.sender_id   
            )
        )

    crud.delete_friend_request(db=db, request_id=request_id)
    return updated_request



@router.delete("/delete/{friend_id}",response_model=schemas.Friend)
def delete_friend(friend_id:int, db: Session = Depends(database.get_db)):
    deleted_friend = crud.delete_friend(db=db, friend_id=friend_id)
    
    if not deleted_friend:
        raise HTTPException(status_code=404, detail="Friend not found")
    
    return deleted_friend