"""Room management routes."""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Room, Invitation, User
from app.schemas import (
    RoomCreate, RoomResponse, RoomDetailResponse, RoomUpdate,
    InvitationCreate, InvitationResponse
)
from app.auth import get_current_user
from app.services.room_service import RoomService

router = APIRouter(prefix="/api/rooms", tags=["rooms"])


@router.post("", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
def create_room(
    room_data: RoomCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new room."""
    # Verify movie exists
    from app.models import Movie
    movie = db.query(Movie).filter(Movie.id == room_data.movie_id).first()
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found"
        )
    
    room = RoomService.create_room(
        db=db,
        creator_id=current_user.id,
        name=room_data.name,
        movie_id=room_data.movie_id,
        description=room_data.description,
        is_private=room_data.is_private,
        max_members=room_data.max_members
    )
    
    # Add member count for response
    room.member_count = len(room.members)
    return room


@router.get("", response_model=list[RoomResponse])
def list_rooms(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    movie_id: Optional[int] = Query(None),
    search: Optional[str] = Query(None),
    current_user: Optional[User] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List available rooms."""
    user_id = current_user.id if current_user else None
    rooms = RoomService.get_available_rooms(
        db=db,
        user_id=user_id,
        movie_id=movie_id,
        search=search,
        limit=limit
    )
    
    # Add member count
    for room in rooms:
        room.member_count = len(room.members)
    
    return rooms[skip:skip+limit]


@router.get("/my-rooms", response_model=list[RoomResponse])
def get_my_rooms(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all rooms the current user is a member of."""
    rooms = RoomService.get_user_rooms(db, current_user.id)
    
    # Add member count
    for room in rooms:
        room.member_count = len(room.members)
    
    return rooms


@router.get("/{room_id}", response_model=RoomDetailResponse)
def get_room(
    room_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get room details."""
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    # Check if user has access (public or member)
    if room.is_private and current_user not in room.members:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to private room"
        )
    
    room.member_count = len(room.members)
    return room


@router.put("/{room_id}", response_model=RoomResponse)
def update_room(
    room_id: int,
    room_update: RoomUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update room (only creator can update)."""
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    if room.creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only room creator can update"
        )
    
    if room_update.name is not None:
        room.name = room_update.name
    if room_update.description is not None:
        room.description = room_update.description
    if room_update.is_private is not None:
        room.is_private = room_update.is_private
    if room_update.max_members is not None:
        room.max_members = room_update.max_members
    
    db.commit()
    db.refresh(room)
    room.member_count = len(room.members)
    return room


@router.post("/{room_id}/join", response_model=RoomResponse)
def join_room(
    room_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Join a room."""
    success, message = RoomService.join_room(db, room_id, current_user.id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )
    
    room = db.query(Room).filter(Room.id == room_id).first()
    room.member_count = len(room.members)
    return room


@router.post("/{room_id}/leave", status_code=status.HTTP_200_OK)
def leave_room(
    room_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Leave a room."""
    success, message = RoomService.leave_room(db, room_id, current_user.id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )
    
    return {"message": message}


@router.post("/{room_id}/invite", response_model=InvitationResponse, status_code=status.HTTP_201_CREATED)
def invite_to_room(
    room_id: int,
    invitation_data: InvitationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Invite a user to a room."""
    # Verify room_id matches
    if invitation_data.room_id != room_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Room ID mismatch"
        )
    
    invitation, message = RoomService.invite_user(
        db=db,
        room_id=room_id,
        inviter_id=current_user.id,
        invitee_id=invitation_data.invitee_id,
        message=invitation_data.message
    )
    
    if not invitation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )
    
    return invitation


@router.get("/invitations/me", response_model=list[InvitationResponse])
def get_my_invitations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get invitations received by current user."""
    invitations = db.query(Invitation).filter(
        Invitation.invitee_id == current_user.id,
        Invitation.status == "pending"
    ).all()
    return invitations


@router.post("/invitations/{invitation_id}/accept", response_model=RoomResponse)
def accept_invitation(
    invitation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Accept a room invitation."""
    invitation = db.query(Invitation).filter(
        Invitation.id == invitation_id,
        Invitation.invitee_id == current_user.id
    ).first()
    
    if not invitation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invitation not found"
        )
    
    if invitation.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invitation already processed"
        )
    
    success, message = RoomService.join_room(
        db, invitation.room_id, current_user.id
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )
    
    room = db.query(Room).filter(Room.id == invitation.room_id).first()
    room.member_count = len(room.members)
    return room


@router.post("/invitations/{invitation_id}/decline", status_code=status.HTTP_200_OK)
def decline_invitation(
    invitation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Decline a room invitation."""
    invitation = db.query(Invitation).filter(
        Invitation.id == invitation_id,
        Invitation.invitee_id == current_user.id
    ).first()
    
    if not invitation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invitation not found"
        )
    
    if invitation.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invitation already processed"
        )
    
    invitation.status = "declined"
    db.commit()
    
    return {"message": "Invitation declined"}


