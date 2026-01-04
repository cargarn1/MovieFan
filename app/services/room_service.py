"""Room management service."""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from app.models import Room, User, Invitation, room_members


class RoomService:
    """Service for room management operations."""

    @staticmethod
    def create_room(
        db: Session,
        creator_id: int,
        name: str,
        movie_id: int,
        description: Optional[str] = None,
        is_private: bool = False,
        max_members: int = 50
    ) -> Room:
        """Create a new room."""
        room = Room(
            name=name,
            description=description,
            movie_id=movie_id,
            creator_id=creator_id,
            is_private=is_private,
            max_members=max_members
        )
        db.add(room)
        db.flush()
        
        # Add creator as member
        creator = db.query(User).filter(User.id == creator_id).first()
        if creator:
            room.members.append(creator)
        
        db.commit()
        db.refresh(room)
        return room

    @staticmethod
    def join_room(db: Session, room_id: int, user_id: int) -> tuple[bool, str]:
        """
        Join a room.
        Returns (success: bool, message: str)
        """
        room = db.query(Room).filter(Room.id == room_id).first()
        if not room:
            return False, "Room not found"
        
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False, "User not found"
        
        # Check if user is already a member
        if user in room.members:
            return False, "Already a member of this room"
        
        # Check if room is full
        if len(room.members) >= room.max_members:
            return False, "Room is full"
        
        # Add user to room
        room.members.append(user)
        
        # Update any pending invitations
        invitation = db.query(Invitation).filter(
            and_(
                Invitation.room_id == room_id,
                Invitation.invitee_id == user_id,
                Invitation.status == "pending"
            )
        ).first()
        
        if invitation:
            invitation.status = "accepted"
        
        db.commit()
        return True, "Successfully joined room"

    @staticmethod
    def leave_room(db: Session, room_id: int, user_id: int) -> tuple[bool, str]:
        """
        Leave a room.
        Returns (success: bool, message: str)
        """
        room = db.query(Room).filter(Room.id == room_id).first()
        if not room:
            return False, "Room not found"
        
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False, "User not found"
        
        # Check if user is creator
        if room.creator_id == user_id:
            return False, "Room creator cannot leave. Transfer ownership or delete room."
        
        # Remove user from room
        if user in room.members:
            room.members.remove(user)
            db.commit()
            return True, "Successfully left room"
        
        return False, "Not a member of this room"

    @staticmethod
    def invite_user(
        db: Session,
        room_id: int,
        inviter_id: int,
        invitee_id: int,
        message: Optional[str] = None
    ) -> tuple[Optional[Invitation], str]:
        """
        Invite a user to a room.
        Returns (invitation: Optional[Invitation], message: str)
        """
        room = db.query(Room).filter(Room.id == room_id).first()
        if not room:
            return None, "Room not found"
        
        inviter = db.query(User).filter(User.id == inviter_id).first()
        invitee = db.query(User).filter(User.id == invitee_id).first()
        
        if not inviter or not invitee:
            return None, "User not found"
        
        # Check if inviter is a member
        if inviter not in room.members:
            return None, "You must be a member to invite others"
        
        # Check if invitee is already a member
        if invitee in room.members:
            return None, "User is already a member"
        
        # Check if invitation already exists
        existing = db.query(Invitation).filter(
            and_(
                Invitation.room_id == room_id,
                Invitation.invitee_id == invitee_id,
                Invitation.status == "pending"
            )
        ).first()
        
        if existing:
            return None, "Invitation already sent"
        
        # Create invitation
        invitation = Invitation(
            room_id=room_id,
            inviter_id=inviter_id,
            invitee_id=invitee_id,
            message=message,
            status="pending"
        )
        db.add(invitation)
        db.commit()
        db.refresh(invitation)
        
        return invitation, "Invitation sent successfully"

    @staticmethod
    def get_user_rooms(db: Session, user_id: int) -> List[Room]:
        """Get all rooms a user is a member of."""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return []
        return user.room_memberships

    @staticmethod
    def get_available_rooms(
        db: Session,
        user_id: Optional[int] = None,
        movie_id: Optional[int] = None,
        search: Optional[str] = None,
        limit: int = 20
    ) -> List[Room]:
        """Get available rooms (public rooms user hasn't joined)."""
        query = db.query(Room).filter(Room.is_private == False)
        
        if movie_id:
            query = query.filter(Room.movie_id == movie_id)
        
        if search:
            query = query.filter(
                or_(
                    Room.name.ilike(f"%{search}%"),
                    Room.description.ilike(f"%{search}%")
                )
            )
        
        rooms = query.limit(limit).all()
        
        # Filter out rooms user is already a member of
        if user_id:
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                rooms = [r for r in rooms if user not in r.members]
        
        return rooms

