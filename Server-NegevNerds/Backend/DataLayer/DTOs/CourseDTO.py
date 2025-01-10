from Backend.BusinessLayer.Course.Course import Course


class CourseDTO:
    def __init__(self, course_id= None, name= None, course: Course = None):
        if course:
            self._course_id = course.get_id()
            self._name = course.get_name() or name
            #self._course_topics = course.get_topics() or course_topics
        else:
            self._course_id = course_id
            self._name = name
            #self._course_topics = course_topics

            # Getter and Setter for course_id

    def get_course_id(self):
        return self._course_id


    def set_course_id(self, value):
        if not value:
            raise ValueError("Course ID cannot be empty.")
        self._course_id = value

    # Getter and Setter for name

    def get_name(self):
        return self._name

    def set_name(self, value):
        if not value:
            raise ValueError("Course name cannot be empty.")
        self._name = value


    # Getter and Setter for course_topics
    # @property
    # def get_course_topics(self):
    #     return self._course_topics


    # def set_course_topics(self, value):
    #     if not isinstance(value, list):
    #         raise ValueError("Course topics must be a list.")
    #     self._course_topics = value

    def to_dict(self):
        return {
            'course_id': self._course_id,
            'name': self._name,
        }
