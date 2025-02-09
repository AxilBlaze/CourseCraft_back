from app import mongo
from models.course import Course

def init_db():
    # Clear existing courses
    mongo.db.courses.delete_many({})
    
    # Sample courses
    courses = [
        Course(
            title="Python Programming Basics",
            description="Learn the fundamentals of Python programming",
            difficulty_level="beginner",
            topics=["programming", "python", "basics"],
            duration=120,
            prerequisites=[],
            skills_gained=["Basic Python syntax", "Variables", "Control flow"]
        ),
        # Add more sample courses...
    ]
    
    # Insert courses
    for course in courses:
        mongo.db.courses.insert_one(course.to_dict())

if __name__ == "__main__":
    init_db() 