


class PointsService:
    
    
    @staticmethod
    def award_point():

        # Create new point
        new_point = Point(
            issuer_id=current_user.id,
            recipient_id=user_id,
            value=point.value,
            reason=point.reason,
            type=point.type,
        )

        db.add(new_point)
        db.commit()

        existing_user.points.append(new_point)

        db.refresh(existing_user)

        return new_point