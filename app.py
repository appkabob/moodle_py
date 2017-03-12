from models.moodle_utils import Moodle
from models.course import Course

course = Course('Beyond Compliance Part 3', 12)
course.fetch_interactions()
print(course.interactions)