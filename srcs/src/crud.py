# src/crud.py
from sqlalchemy.orm import Session
import model, schemas
from datetime import datetime

def create_friend(db: Session, friend: schemas.FriendCreate):
    db_friend = model.Friend(user_id=friend.user_id, friend_id=friend.friend_id)
    db.add(db_friend)
    db.commit()
    db.refresh(db_friend)
    return db_friend

def create_friend_request(db: Session, request: schemas.FriendRequestCreate):
    db_request = model.FriendRequest(
        sender_id=request.sender_id,
        receiver_id=request.receiver_id,
        status="pending",
        sent_at=datetime.utcnow()
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request

def get_friends(db: Session, user_id: int):
    return db.query(model.Friend).filter((model.Friend.user_id == user_id) | (model.Friend.friend_id == user_id)).all()

def get_friend_requests(db: Session, user_id: int):
    return db.query(model.FriendRequest).filter(model.FriendRequest.receiver_id == user_id).all()

def update_friend_request_status(db: Session, request_id: int, status: str):
    request = db.query(model.FriendRequest).filter(model.FriendRequest.id == request_id).first()
    if request:
        request.status = status
        request.responded_at = datetime.utcnow()
        db.commit()
        db.refresh(request)
    return request

def delete_friend_request(db: Session, request_id: int):
    db_request = db.query(model.FriendRequest).filter(model.FriendRequest.id == request_id).first()
    db.delete(db_request)
    db.commit()

def delete_friend(friend_id: int, db: Session):
    db_friend = db.query(model.Friend).filter(model.Friend.id == friend_id).first()
    if db_friend is None:
        return None  # Si l'ami n'existe pas, retourne None
    db.delete(db_friend)
    db.commit()
    return db_friend  # Retourne l'ami supprimé pour la confirmation
