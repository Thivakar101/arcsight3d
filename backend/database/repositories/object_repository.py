from backend.models.detected_object import DetectedObject
from backend.models.wall import Wall
from backend.models.door import Door
from backend.models.window import Window
from backend.models.room import Room
from backend.extensions import db

class ObjectRepository:
    @staticmethod
    def save_detected_objects(project_id, objects_data):
        saved_objects = []
        for obj_data in objects_data:
            obj = DetectedObject(
                project_id=project_id,
                object_type=obj_data.get('object_type', 'UNKNOWN'),
                x=obj_data.get('x'),
                y=obj_data.get('y'),
                width=obj_data.get('width'),
                height=obj_data.get('height'),
                x1=obj_data.get('x1'),
                y1=obj_data.get('y1'),
                x2=obj_data.get('x2'),
                y2=obj_data.get('y2'),
                angle=obj_data.get('angle'),
                confidence=obj_data.get('confidence')
            )
            db.session.add(obj)
            saved_objects.append((obj, obj_data))
        
        db.session.flush() # To get the generated IDs
        
        # Save specific types
        for obj, obj_data in saved_objects:
            if obj.object_type == 'WALL':
                wall = Wall(
                    project_id=project_id,
                    detected_object_id=obj.id,
                    start_x=obj_data.get('x1', obj_data.get('x', 0)),
                    start_y=obj_data.get('y1', obj_data.get('y', 0)),
                    end_x=obj_data.get('x2', obj_data.get('x', 0) + obj_data.get('width', 0)),
                    end_y=obj_data.get('y2', obj_data.get('y', 0) + obj_data.get('height', 0)),
                    thickness=obj_data.get('thickness', 10),
                    confidence=obj.confidence
                )
                db.session.add(wall)
            elif obj.object_type == 'DOOR':
                door = Door(
                    project_id=project_id,
                    detected_object_id=obj.id,
                    center_x=obj_data.get('x', 0) + obj_data.get('width', 0)/2,
                    center_y=obj_data.get('y', 0) + obj_data.get('height', 0)/2,
                    width=obj_data.get('width', 0),
                    height=obj_data.get('height', 0),
                    confidence=obj.confidence
                )
                db.session.add(door)
                
        db.session.commit()
        return [obj[0] for obj in saved_objects]
