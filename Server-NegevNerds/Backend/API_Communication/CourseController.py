import ast
import json
import mimetypes
import os

from flask import Blueprint, request, jsonify, send_file
from flask_cors import cross_origin, CORS
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required, get_jwt_identity


from Backend.BusinessLayer.NegevNerds import NegevNerds
from Backend.BusinessLayer.PDFAnalyzer.FileManager import FileManager
from Backend.BusinessLayer.User.UserFacade import UserFacade
from Backend.DataLayer.DTOs.NotificationDTO import NotificationDTO
from Backend.DataLayer.DTOs.QuestionDTO import QuestionDTO
from Backend.ServiceLayer.ServiceLayer import ServiceLayer

course_controller = Blueprint('course_controller', __name__)




CORS(course_controller, resources={
    r"/api/*": {
        "origins": "*",  # Or specify exact origin like "http://localhost:3000"
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})


serviceLayer = ServiceLayer("../")


ALLOWED_EXTENSIONS = {'pdf', 'jpeg', 'jpg', 'png'}

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def parse_jsonify(parsed_result):
    # Check the status and return appropriate response
    if parsed_result['status'] == 'success':
        return jsonify({
            "success": True,
            "message": parsed_result['message']
        }), 200
    else:
        return jsonify({
            "success": False,
            "message": parsed_result['message']
        }), 400


@course_controller.route('/api/course/register_to_course', methods=['POST', 'GET', 'OPTIONS'])
@jwt_required()
@cross_origin()
def register_to_course():
    # Handle OPTIONS preflight request
    if request.method == 'OPTIONS':
        response = jsonify(success=True)
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response

    try:
        # Extract data from the request
        data = request.get_json()

        # Validate input
        if not all(key in data for key in ['course_id']):
            return jsonify({
                "success": False,
                "message": "Missing required fields"
            }), 400

        # Extract data
        course_id = data.get('course_id')
        user_id = get_jwt_identity()  # Get the user_id from JWT token

        # Call the service layer's register method directly
        result = serviceLayer.register_to_course(course_id, user_id)

        # Parse the JSON string
        parsed_result = json.loads(result)

        # Check the status and return appropriate response
        return parse_jsonify(parsed_result)

    except json.JSONDecodeError:
        # Handle JSON decoding error
        return jsonify({
            "success": False,
            "message": "Invalid JSON response from service"
        }), 500
    except Exception as e:
        print(f"Error in registration: {str(e)}")
        return jsonify({
            "success": False,
            "message": "An unexpected error occurred",
            "error": str(e)
        }), 500

@course_controller.route('/api/course/open_course', methods=['POST', 'OPTIONS'])
@cross_origin()
@jwt_required()
def open_course():
    if request.method == 'OPTIONS':
        response = jsonify(success=True)
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response

    try:
        print("Received a request to open_course.")

        # Check if all required form data is present
        if 'course_id' not in request.form or 'name' not in request.form:
            print("Missing required form fields.")
            return jsonify({"success": False, "message": "Missing required fields"}), 400

        if 'syllabus_content_pdf' not in request.files:
            print("Syllabus file not found in request.")
            return jsonify({"success": False, "message": "Syllabus file is required"}), 400

        # Extract data
        course_id = request.form.get('course_id')
        name = request.form.get('name')
        syllabus_file = request.files['syllabus_content_pdf']

        user_id = get_jwt_identity()

        # Save file to the specified directory
        base_dir = os.path.join(os.getcwd(), 'Backend', 'BusinessLayer', 'PDFAnalyzer')
        os.makedirs(base_dir, exist_ok=True)  # Ensure the directory exists
        file_path = os.path.join(base_dir, secure_filename(syllabus_file.filename))
        syllabus_file.save(file_path)
        print(f"File saved to {file_path}")
        print(f"user id {user_id}")

        # Call the service layer
        result = serviceLayer.open_course(user_id, course_id, name, file_path)
        parsed_result = json.loads(result)
        print(f"Service layer response: {parsed_result}")

        try:
            os.remove(file_path)
            print(f"Deleted file {file_path}")
        except Exception as delete_error:
            print(f"Error deleting file {file_path}: {str(delete_error)}")


        # Construct and return response
        return jsonify({
            "success": parsed_result.get("status") == "success",  # Set success as boolean
            "message": parsed_result.get("message")  # Return message from service layer
        }), 200

    except Exception as e:
        print(f"Error in open_course: {str(e)}")
        return jsonify({
            "success": False,
            "message": "An unexpected error occurred",
            "error": str(e)
        }), 500


@course_controller.route('/api/course/remove_course', methods=['POST', 'GET', 'OPTIONS'])
@cross_origin()
@jwt_required()
def remove_course():
    # Handle OPTIONS preflight request
    if request.method == 'OPTIONS':
        response = jsonify(success=True)
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response

    try:
        # Extract data from the request
        data = request.get_json()

        # Validate input
        if not all(key in data for key in ['course_id']):
            return jsonify({
                "success": False,
                "message": "Missing required fields"
            }), 400

        # Extract data
        course_id = data.get('course_id')

        user_id = get_jwt_identity()

        # Call the service layer's register method directly
        result = serviceLayer.remove_course(course_id, user_id)

        # Parse the JSON string
        parsed_result = json.loads(result)

        # Check the status and return appropriate response
        return parse_jsonify(parsed_result)

    except json.JSONDecodeError:
        # Handle JSON decoding error
        return jsonify({
            "success": False,
            "message": "Invalid JSON response from service"
        }), 500
    except Exception as e:
        print(f"Error in registration: {str(e)}")
        return jsonify({
            "success": False,
            "message": "An unexpected error occurred",
            "error": str(e)
        }), 500


@course_controller.route('/api/course/remove_student_from_course', methods=['POST', 'GET', 'OPTIONS'])
@cross_origin()
@jwt_required()
def remove_student_from_course():
    # Handle OPTIONS preflight request
    if request.method == 'OPTIONS':
        response = jsonify(success=True)
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response

    try:
        # Extract data from the request
        data = request.get_json()

        # Validate input
        if not all(key in data for key in ['course_id']):
            return jsonify({
                "success": False,
                "message": "Missing required fields"
            }), 400

        # Extract data
        course_id = data.get('course_id')

        user_id = get_jwt_identity()

        # Call the service layer's register method directly
        result = serviceLayer.remove_student_from_course(course_id, user_id)

        # Parse the JSON string
        parsed_result = json.loads(result)

        # Check the status and return appropriate response
        return parse_jsonify(parsed_result)

    except json.JSONDecodeError:
        # Handle JSON decoding error
        return jsonify({
            "success": False,
            "message": "Invalid JSON response from service"
        }), 500
    except Exception as e:
        print(f"Error in registration: {str(e)}")
        return jsonify({
            "success": False,
            "message": "An unexpected error occurred",
            "error": str(e)
        }), 500


@course_controller.route('/api/course/get_user_notifications', methods=['POST', 'GET', 'OPTIONS'])
@cross_origin()
@jwt_required()
def get_user_notifications():
    # Handle OPTIONS preflight request
    if request.method == 'OPTIONS':
        response = jsonify(success=True)
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response

    try:
        # Extract data from the request
        # data = request.get_json()

        user_id = get_jwt_identity()

        # Call the service layer's register method directly
        result = serviceLayer.get_user_notifications(user_id)

        # Parse the JSON string
        if isinstance(result, list):
            result = [notification.to_dict() if isinstance(notification, NotificationDTO) else notification for notification in result]
        else:
            result = result.to_dict() if isinstance(result, NotificationDTO) else result

        # Parse the JSON string
        parsed_result = json.loads(result)

        # Check the status and return appropriate response
        return parse_jsonify(parsed_result)

    except json.JSONDecodeError:
        # Handle JSON decoding error
        return jsonify({
            "success": False,
            "message": "Invalid JSON response from service"
        }), 500
    except Exception as e:
        print(f"Error in registration: {str(e)}")
        return jsonify({
            "success": False,
            "message": "An unexpected error occurred",
            "error": str(e)
        }), 500


@course_controller.route('/api/course/get_user_last_notifications', methods=['POST', 'GET', 'OPTIONS'])
@cross_origin()
@jwt_required()
def get_user_last_notifications():
    # Handle OPTIONS preflight request
    if request.method == 'OPTIONS':
        response = jsonify(success=True)
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response

    try:
        # Extract data from the request

        user_id = get_jwt_identity()

        # Call the service layer's register method directly
        result = serviceLayer.get_user_last_notifications(user_id, 5)

        # Parse the JSON string
        if isinstance(result, list):
            result = [notification.to_dict() if isinstance(notification, NotificationDTO) else notification for
                      notification in result]
        else:
            result = result.to_dict() if isinstance(result, NotificationDTO) else result

        # Parse the JSON string
        parsed_result = json.loads(result)

        # Check the status and return appropriate response
        return parse_jsonify(parsed_result)

    except json.JSONDecodeError:
        # Handle JSON decoding error
        return jsonify({
            "success": False,
            "message": "Invalid JSON response from service"
        }), 500
    except Exception as e:
        print(f"Error in registration: {str(e)}")
        return jsonify({
            "success": False,
            "message": "An unexpected error occurred",
            "error": str(e)
        }), 500


@course_controller.route('/api/course/get_all_courses', methods=['GET', 'OPTIONS'])
@cross_origin()
@jwt_required()
def get_all_courses():
    # Handle OPTIONS preflight request
    print(f"Received request from user: {get_jwt_identity()}")

    if request.method == 'OPTIONS':
        response = jsonify(success=True)
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET, OPTIONS')
        return response

    try:
        # Get the result from the service layer
        result = serviceLayer.get_all_courses()
        # Parse the JSON string into a dictionary
        result_dict = json.loads(result)
        # Ensure the response has the expected structure
        if result_dict.get("status") != "success":
            return jsonify({
                "success": False,
                "message": result_dict.get("message", "Unknown error")
            }), 500

        # Process the data
        parsed_result = result_dict["data"]
        print(parsed_result)  # Debugging

        # Final response
        return jsonify({
            "success": True,
            "data": parsed_result
        })

    except json.JSONDecodeError:
        # Handle JSON decoding errors
        return jsonify({
            "success": False,
            "message": "Invalid JSON response from service"
        }), 500
    except Exception as e:
        # Handle unexpected errors
        print(f"Error: {str(e)}")
        return jsonify({
            "success": False,
            "message": "An unexpected error occurred",
            "error": str(e)
        }), 500


@course_controller.route('/api/course/get_course_topics', methods=['GET', 'OPTIONS'])
@cross_origin()
@jwt_required()
def get_course_topics():
    # Handle OPTIONS preflight request
    if request.method == 'OPTIONS':
        response = jsonify(success=True)
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET')
        return response

    try:
        # Extract course_id from query parameters
        course_id = request.args.get('course_id')

        if not course_id:
            return jsonify({
                "status": "error",
                "message": "Course ID is required"
            }), 400

        # Get course topics
        result = serviceLayer.get_course_topics(course_id)

        # Parse the JSON string
        parsed_result = json.loads(result)

        # Check if the result has a success status
        if parsed_result.get('status') == 'success':
            return jsonify({
                "status": "success",
                "data": parsed_result.get('data', [])
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": parsed_result.get('message', 'Unknown error')
            }), 400

    except json.JSONDecodeError:
        return jsonify({
            "status": "error",
            "message": "Invalid JSON response"
        }), 500
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@course_controller.route('/api/course/get_question_pdf', methods=['GET', 'OPTIONS'])
@cross_origin()
@jwt_required()
def get_question_pdf():
    if request.method == 'OPTIONS':
        response = jsonify(success=True)
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET')
        return response
    try:
        # קבלת פרמטרים מ-Query String
        course_id = request.args.get('course_id')
        year = request.args.get('year')
        semester = request.args.get('semester')
        moed = request.args.get('moed')
        question_number = request.args.get('question_number')

        print(
            f"Received parameters: course_id={course_id}, year={year}, semester={semester}, moed={moed}, question_number={question_number}")

        # בדיקת פרמטרים
        if not all([course_id, year, semester, moed, question_number]):
            return jsonify({
                "status": "error",
                "message": "Missing required parameters"
            }), 400

        # בניית הנתיב של הקובץ
        question_path = serviceLayer.get_question_path(course_id, year, semester, moed, question_number)
        print(f"Generated file path: {question_path}")

        # בדיקה אם הקובץ קיים
        if not os.path.exists(question_path):
            return jsonify({
                "status": "error",
                "message": "File not found"
            }), 404

        # שליחת הקובץ ללקוח

        mime_type, _ = mimetypes.guess_type(question_path)

        if mime_type == 'application/pdf':
            # If it's a PDF, send as PDF
            return send_file(question_path, mimetype='application/pdf')
        elif mime_type and mime_type.startswith('image/'):
            # If it's an image (JPEG, PNG, etc.), send as an image

            return send_file(question_path, mimetype=mime_type)
        else:
            # Handle unsupported file types
            return 'Unsupported file type', 400
    except Exception as e:
        print(f"Error in get_pdf: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@course_controller.route('/api/course/get_answer_pdf', methods=['GET', 'OPTIONS'])
@cross_origin()
@jwt_required()
def get_answer_pdf():
    if request.method == 'OPTIONS':
        response = jsonify(success=True)
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET')
        return response
    try:
        # קבלת פרמטרים מ-Query String
        course_id = request.args.get('course_id')
        year = request.args.get('year')
        semester = request.args.get('semester')
        moed = request.args.get('moed')
        question_number = request.args.get('question_number')

        print(
            f"Received parameters: course_id={course_id}, year={year}, semester={semester}, moed={moed}, question_number={question_number}")

        # בדיקת פרמטרים
        if not all([course_id, year, semester, moed, question_number]):
            return jsonify({
                "status": "error",
                "message": "Missing required parameters"
            }), 400

        # בניית הנתיב של הקובץ
        answer_path = serviceLayer.get_answer_path(course_id, year, semester, moed, question_number)
        print(f"Generated file path: {answer_path}")

        # בדיקה אם הקובץ קיים
        if not os.path.exists(answer_path):
            return jsonify({
                "status": "error",
                "message": "File not found"
            }), 404

        # שליחת הקובץ ללקוח
        mime_type, _ = mimetypes.guess_type(answer_path)

        if mime_type == 'application/pdf':
            # If it's a PDF, send as PDF
            return send_file(answer_path, mimetype='application/pdf')
        elif mime_type and mime_type.startswith('image/'):
            # If it's an image (JPEG, PNG, etc.), send as an image

            return send_file(answer_path, mimetype=mime_type)

        #return send_file(answer_path, mimetype='application/pdf')
    except Exception as e:
        print(f"Error in get_pdf: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@course_controller.route('/api/course/get_course/<course_id>', methods=['GET', 'OPTIONS'])
@cross_origin()
@jwt_required()
def get_course(course_id):
    # Handle OPTIONS preflight request
    if request.method == 'OPTIONS':
        response = jsonify(success=True)
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET')
        return response

    try:
        # Extract course_id from query parameters
        # course_id = request.args.get('course_id')

        print(f"Received course_id from URL: {course_id}")

        if not course_id:
            return jsonify({
                "status": "error",
                "message": "Course ID is required"
            }), 400

        # Get course details from the service layer
        result = serviceLayer.get_course(course_id)

        # Parse the JSON string
        parsed_result = json.loads(result)

        print(f"Received course details: {parsed_result}")

        # Check if the result has a success status
        if parsed_result.get('status') == 'success':
            return jsonify({
                "status": "success",
                "data": parsed_result.get('data', {})
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": parsed_result.get('message', 'Unknown error')
            }), 400

    except json.JSONDecodeError:
        return jsonify({
            "status": "error",
            "message": "Invalid JSON response"
        }), 500
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# @course_controller.route('/api/course/add_question', methods=['POST', 'OPTIONS'])
# @cross_origin()
# def add_question():
#     if request.method == 'OPTIONS':
#         response = jsonify(success=True)
#         response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
#         response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
#         response.headers.add('Access-Control-Allow-Methods', 'POST')
#         return response

#     try:
#         # Parse the JSON data from the request
#         data = request.get_json()

#         # Validate input fields
#         required_fields = ['course_id', 'year', 'semester', 'moed', 'question_number', 'is_american', 'question_topics', 'pdf_question']
#         missing_fields = [field for field in required_fields if field not in data]
#         if missing_fields:
#             return jsonify({
#                 "success": False,
#                 "message": f"Missing required fields: {', '.join(missing_fields)}"
#             }), 400

#         # Extract the fields
#         course_id = data.get('course_id')
#         year = data.get('year')
#         semester = data.get('semester')
#         moed = data.get('moed')
#         question_number = data.get('question_number')
#         is_american = data.get('is_american')
#         question_topics = data.get('question_topics')
#         pdf_question = data.get('pdf_question')
#         pdf_answer = data.get('pdf_answer')  # Optional

#         # Call the service layer function
#         result = serviceLayer.add_question(
#             course_id, year, semester, moed, question_number,
#             is_american, question_topics, pdf_question, pdf_answer
#         )

#         # Parse the service response
#         parsed_result = json.loads(result)
#         return parse_jsonify(parsed_result)

#     except json.JSONDecodeError:
#         return jsonify({
#             "success": False,
#             "message": "Invalid JSON in request or response"
#         }), 500
#     except Exception as e:
#         return jsonify({
#             "success": False,
#             "message": "An unexpected error occurred",
#             "error": str(e)
#         }), 500

@course_controller.route('/api/course/add_question', methods=['POST', 'OPTIONS'])
@cross_origin()
@jwt_required()
def add_question():
    if request.method == 'OPTIONS':
        response = jsonify(success=True)
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response

    try:
        # Extract required fields from form data
        course_id = request.form.get('course_id')
        year = int(request.form.get('year'))
        semester = request.form.get('semester')
        moed = request.form.get('moed')
        question_number = int(request.form.get('question_number'))
        is_american = request.form.get('is_american')
        is_american_boolean = is_american.lower() == 'true'
        question_topics = request.form.get('question_topics')
        question_file = request.files.get('pdf_question')
        answer_file = request.files.get('pdf_answer')  # Optional

        # Validate required fields
        required_fields = [course_id, year, semester, moed, question_number, is_american, question_topics, question_file]
        if any(field is None for field in required_fields):
            return jsonify({
                "success": False,
                "message": "Missing required fields."
            }), 400

        if question_file and not allowed_file(question_file.filename):
            return jsonify({
                "success": False,
                "message": "Invalid file type for pdf_question. Allowed types are PDF, JPEG, PNG."
            }), 400

        if answer_file and not allowed_file(answer_file.filename):
            return jsonify({
                "success": False,
                "message": "Invalid file type for pdf_answer. Allowed types are PDF, JPEG, PNG."
            }), 400


        if isinstance(question_topics, str):
            try:
                question_topics = ast.literal_eval(question_topics)  # Safely convert string to list
                if not isinstance(question_topics, list):  # Ensure it's a list after conversion
                    question_topics = [question_topics]
            except (ValueError, SyntaxError):
                return jsonify({
                    "success": False,
                    "message": "Invalid format for question_topics."
                }), 400

        # Call the service layer
        result = serviceLayer.add_question(
            course_id, year, semester, moed, question_number,
            is_american_boolean, question_topics, question_file, answer_file
        )

        # Parse the service response
        parsed_result = json.loads(result)
        return jsonify({
            "success": parsed_result.get("status") == "success",
            "message": parsed_result.get("message")
        }), 200

    except Exception as e:
        print(f"Error in add_question: {str(e)}")
        return jsonify({
            "success": False,
            "message": "An unexpected error occurred.",
            "error": str(e)
        }), 500


@course_controller.route('/api/course/add_comment', methods=['POST', 'OPTIONS'])
@cross_origin()
@jwt_required()
def add_comment():
    if request.method == 'OPTIONS':
        response = jsonify(success=True)
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response

    try:
        # Extract required fields from form data
        course_id = request.form.get('course_id')
        year = int(request.form.get('year'))
        semester = request.form.get('semester')
        moed = request.form.get('moed')
        question_number = int(request.form.get('question_number'))
        writer_name = request.form.get('writer_name')
        writer_id = get_jwt_identity()
        prev_id = request.form.get('prev_id')
        comment_text = request.form.get('comment_text')  # Optional

        # Validate required fields
        required_fields = [course_id, year, semester, moed, question_number, writer_name, prev_id, comment_text]
        if any(field is None for field in required_fields):
            return jsonify({
                "success": False,
                "message": "Missing required fields."
            }), 400

        # Call the service layer
        result = serviceLayer.add_comment(
            course_id, year, semester, moed, question_number,
            writer_name, writer_id, prev_id, comment_text
        )

        # Parse the service response
        parsed_result = json.loads(result)
        return jsonify({
            "success": parsed_result.get("status") == "success",
            "message": parsed_result.get("message")
        }), 200

    except Exception as e:
        print(f"Error in add_comment: {str(e)}")
        return jsonify({
            "success": False,
            "message": "An unexpected error occurred.",
            "error": str(e)
        }), 500


@course_controller.route('/api/course/add_reaction', methods=['POST', 'OPTIONS'])
@cross_origin()
@jwt_required()
def add_reaction():
    if request.method == 'OPTIONS':
        response = jsonify(success=True)
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response

    try:
        # Extract required fields from form data
        course_id = request.form.get('course_id')
        year = int(request.form.get('year'))
        semester = request.form.get('semester')
        moed = request.form.get('moed')
        question_number = int(request.form.get('question_number'))
        comment_id = request.form.get('comment_id')
        user_id = get_jwt_identity()
        emoji = request.form.get('emoji')  # Optional

        # Validate required fields
        required_fields = [course_id, year, semester, moed, question_number, comment_id, emoji]
        if any(field is None for field in required_fields):
            return jsonify({
                "success": False,
                "message": "Missing required fields."
            }), 400

        # Call the service layer
        result = serviceLayer.add_reaction(
            course_id, year, semester, moed, question_number,
            comment_id, user_id, emoji
        )

        # Parse the service response
        parsed_result = json.loads(result)
        return jsonify({
            "success": parsed_result.get("status") == "success",
            "message": parsed_result.get("message")
        }), 200

    except Exception as e:
        print(f"Error in add_reaction: {str(e)}")
        return jsonify({
            "success": False,
            "message": "An unexpected error occurred.",
            "error": str(e)
        }), 500


@course_controller.route('/api/course/remove_reaction', methods=['POST', 'GET', 'OPTIONS'])
@cross_origin()
@jwt_required()
def remove_reaction():
    if request.method == 'OPTIONS':
        response = jsonify(success=True)
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response

    try:
        # Extract required fields from form data
        course_id = request.form.get('course_id')
        year = int(request.form.get('year'))
        semester = request.form.get('semester')
        moed = request.form.get('moed')
        question_number = int(request.form.get('question_number'))
        comment_id = request.form.get('comment_id')
        reaction_id = request.form.get('reaction_id')

        # Validate required fields
        required_fields = [course_id, year, semester, moed, question_number, comment_id, reaction_id]
        if any(field is None for field in required_fields):
            return jsonify({
                "success": False,
                "message": "Missing required fields."
            }), 400

        # Call the service layer
        result = serviceLayer.remove_reaction(
            course_id, year, semester, moed, question_number,
            comment_id, reaction_id
        )

        # Parse the service response
        parsed_result = json.loads(result)
        return jsonify({
            "success": parsed_result.get("status") == "success",
            "message": parsed_result.get("message")
        }), 200

    except Exception as e:
        print(f"Error in remove_reaction: {str(e)}")
        return jsonify({
            "success": False,
            "message": "An unexpected error occurred.",
            "error": str(e)
        }), 500


@course_controller.route('/api/course/search_question_by_specifics', methods=['OPTIONS', 'POST'])
@cross_origin()
@jwt_required()
def search_question_by_specifics():
    # Handle OPTIONS preflight request
    if request.method == 'OPTIONS':
        response = jsonify(success=True)
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response

    try:
        # Extract data from the request
        data = request.get_json()


        # הדפסת המידע שהתקבל מהלקוח
        print("Received data:", data)

        # Validate input
        if not all(key in data for key in ['course_id']):
            return jsonify({
                "success": False,
                "message": "Missing required fields"
            }), 400

        # Extract the data
        course_id = data.get('course_id')
        year = data.get('year')
        semester = data.get('semester') if data.get('semester') else None
        moed = data.get('moed') if data.get('moed') else None
        question_number = data.get('question_number') if data.get('question_number') else None

        # טיפול עם None על מנת למנוע שגיאות

        # הדפסת הנתונים שמתקבלים
        print(
            f"Extracted values: course_id={course_id}, year={year}, semester={semester}, moed={moed}, question_number={question_number}")

        # Call the service layer's search_question_by_specifics method
        if question_number is not None:
            question_number = int(question_number)  # המרת מספר אם קיים
        else:
            question_number = None  # או להשתמש בערך ברירת מחדל אם אין

        if year is not None:
            year = int(year)  # המרת מספר אם קיים
        else:
            year = None  # או להשתמש בערך ברירת מחדל אם אין
        result = serviceLayer.search_question_by_specifics(course_id, year, semester, moed, question_number)
        print(f"Service Layer Result: {result}")

        # Parse the JSON string
        if isinstance(result, list):
            result = [question.to_dict() if isinstance(question, QuestionDTO) else question for question in result]
        else:
            result = result.to_dict() if isinstance(result, QuestionDTO) else result

        # Return the response
        print(f"Formatted result: {result}")

        # Return the response
        return jsonify({
            "success": True,
            "data": result
        }), 200

    except json.JSONDecodeError:
        return jsonify({
            "success": False,
            "message": "Invalid JSON response"
        }), 500
    except Exception as e:
        print(f"Error: {str(e)}")  # הדפסת שגיאה אם התרחשה
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


@course_controller.route('/api/course/search_questions_by_text', methods=['OPTIONS', 'POST'])
@cross_origin()
@jwt_required()
def search_questions_by_text():
    # Handle OPTIONS preflight request
    if request.method == 'OPTIONS':
        response = jsonify(success=True)
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response

    try:
        # Extract data from the request
        data = request.get_json()

        print("Received data:", data)

        # Validate input
        if not all(key in data for key in ['text']):
            return jsonify({
                "success": False,
                "message": "Missing required fields"
            }), 400

        # Extract the data
        text = data.get('text')
        course_id = data.get('course_id')  # Optional

        result = serviceLayer.search_free_text(text=text, course_id=course_id)
        print(f"Service Layer Result: {result}")

        # Parse the JSON string
        if isinstance(result, list):
            result = [question.to_dict() if isinstance(question, QuestionDTO) else question for question in result]
        else:
            result = result.to_dict() if isinstance(result, QuestionDTO) else result

        # Return the response
        print(f"Formatted result: {result}")

        # Return the response
        return jsonify({
            "success": True,
            "data": result
        }), 200

    except json.JSONDecodeError:
        return jsonify({
            "success": False,
            "message": "Invalid JSON response"
        }), 500
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

@course_controller.route('/api/course/upload_answer', methods=['POST', 'OPTIONS'])
@cross_origin()
@jwt_required()
def upload_answer():
    if request.method == 'OPTIONS':
        response = jsonify(success=True)
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response

    try:
        # Extract required fields from form data
        course_id = request.form.get('course_id')
        year = int(request.form.get('year'))
        semester = request.form.get('semester')
        moed = request.form.get('moed')
        question_number = int(request.form.get('question_number'))
        pdf_answer = request.files.get('pdf_answer')  # Optional

        if not all([course_id, year, semester, moed, question_number, pdf_answer]):
            return jsonify({
                "status": "error",
                "message": "Missing required parameters"
            }), 400

        # Call the service layer
        result = serviceLayer.upload_answer(
            course_id, year, semester, moed, question_number, pdf_answer
        )

        # Parse the service response
        parsed_result = json.loads(result)
        return jsonify({
            "success": parsed_result.get("status") == "success",
            "message": parsed_result.get("message")
        }), 200

    except Exception as e:
        print(f"Error in upload_answer: {str(e)}")
        return jsonify({
            "success": False,
            "message": "An unexpected error occurred.",
            "error": str(e)
        }), 500


@course_controller.route('/api/checkExamFullPdf', methods=['POST', 'OPTIONS'])
@cross_origin()
@jwt_required()
def check_exam_full_pdf():
    if request.method == 'OPTIONS':
        response = jsonify(success=True)
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response

    try:
        # Extract required fields from the JSON body
        data = request.get_json()
        course_id = data.get('course_id')
        year = int(data.get('year'))
        semester = data.get('semester')
        moed = data.get('moed')

        # Validate required fields
        if not all([course_id, year, semester, moed]):
            return jsonify({
                "status": "error",
                "message": "Missing required parameters"
            }), 400

        # Call the service layer function
        result = serviceLayer.check_exam_full_pdf(course_id, year, semester, moed)

        # Parse the service response
        parsed_result = json.loads(result)
        return jsonify({
            "success": parsed_result.get("status") == "success",
            "message": parsed_result.get("message"),
            "has_link": parsed_result.get("has_link"),
            "link": parsed_result.get("link", None)
        }), 200

    except Exception as e:
        print(f"Error in check_exam_full_pdf: {str(e)}")
        return jsonify({
            "success": False,
            "message": "An unexpected error occurred.",
            "error": str(e)
        }), 500

@course_controller.route('/api/course/uploadFullExamPdf', methods=['POST', 'OPTIONS'])
@cross_origin()
@jwt_required()
def uploadFullExamPdf():
    if request.method == 'OPTIONS':
        response = jsonify(success=True)
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response

    try:
        # Validate that a file is included in the request
        if 'pdf_exam' not in request.files:
            return jsonify({
                "success": False,
                "message": "No file part in the request"
            }), 400

        pdf_exam = request.files['pdf_exam']

        # Validate file
        if pdf_exam.filename == '':
            return jsonify({
                "success": False,
                "message": "No file selected for upload"
            }), 400

        # Extract additional fields from the form data
        course_id = request.form.get('course_id')
        year = request.form.get('year')
        semester = request.form.get('semester')
        moed = request.form.get('moed')

        # Validate required fields
        if not all([course_id, year, semester, moed]):
            return jsonify({
                "success": False,
                "message": "Missing required parameters"
            }), 400

        # Call service layer to handle logic
        result = serviceLayer.upload_full_exam_pdf(course_id, int(year), semester, moed, pdf_exam)
        parsed_result = json.loads(result)

        return jsonify({
            "success": parsed_result.get("status") == "success",
            "message": parsed_result.get("message"),
            "has_link": parsed_result.get("has_link", False),
            "link": parsed_result.get("link", None)
        }), 200 if parsed_result.get("status") == "success" else 400

    except Exception as e:
        print(f"Error in upload_full_exam_pdf: {str(e)}")
        return jsonify({
            "success": False,
            "message": "An unexpected error occurred.",
            "error": str(e)
        }), 500
    

@course_controller.route('/api/course/downloadExamPdf', methods=['POST', 'OPTIONS'])
@cross_origin()
@jwt_required()
def download_exam_pdf():
    if request.method == 'OPTIONS':
        response = jsonify(success=True)
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response

    try:
        # Extract required fields
        data = request.get_json()
        course_id = data.get('course_id')
        year = int(data.get('year'))
        semester = data.get('semester')
        moed = data.get('moed')

        # Validate required fields
        if not all([course_id, year, semester, moed]):
            return jsonify({
                "success": False,
                "message": "Missing required parameters."
            }), 400

        # Call service layer to get the link
        result = serviceLayer.get_exam_pdf_link(course_id, year, semester, moed)
        parsed_result = json.loads(result)

        if parsed_result.get("has_link"):
            # If the file exists, send it
            file_path = parsed_result.get("link")
            if os.path.exists(file_path):
                filename = f"{course_id}_{year}_{semester}_{moed}.pdf"
                return send_file(file_path, as_attachment=True, download_name=filename, mimetype='application/pdf')
                # return send_file(file_path, as_attachment=True, mimetype='application/pdf')
            else:
                return jsonify({
                    "success": False,
                    "message": "The file path does not exist on the server."
                }), 404
        else:
            # No file link exists
            return jsonify({
                "success": True,
                "message": "המבחן המלא לא קיים במערכת.\n את/ה מוזמנ/ת לתרום לאתר ולהעלות אותה"
            }), 200

    except Exception as e:
        print(f"Error in download_exam_pdf: {str(e)}")
        return jsonify({
            "success": False,
            "message": "An unexpected error occurred.",
            "error": str(e)
        }), 500


@course_controller.route('/api/checkExistSolution', methods=['POST', 'OPTIONS'])
@cross_origin()
@jwt_required()
def checkExistSolution():
    if request.method == 'OPTIONS':
        response = jsonify(success=True)
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response

    try:
        # Extract required fields from the JSON body
        data = request.get_json()
        course_id = data.get('course_id')
        year = int(data.get('year'))
        semester = data.get('semester')
        moed = data.get('moed')
        question_number = data.get("question_number")

        # Validate required fields
        if not all([course_id, year, semester, moed,question_number]):
            return jsonify({
                "status": "error",
                "message": "Missing required parameters"
            }), 400

        # Call the service layer function
        result = serviceLayer.checkExistSolution(course_id, year, semester, moed,question_number)

        # Parse the service response
        parsed_result = json.loads(result)
        return jsonify({
            "success": parsed_result.get("status") == "success",
            "message": parsed_result.get("message"),
            "has_link": parsed_result.get("has_link"),
            "link": parsed_result.get("link", None)
        }), 200

    except Exception as e:
        print(f"Error in check_exam_full_pdf: {str(e)}")
        return jsonify({
            "success": False,
            "message": "An unexpected error occurred.",
            "error": str(e)
        }), 500


@course_controller.route('/api/course/uploadSolution', methods=['POST', 'OPTIONS'])
@cross_origin()
@jwt_required()
def uploadSolution():
    if request.method == 'OPTIONS':
        response = jsonify(success=True)
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response

    try:
        # Validate that a file is included in the request
        if 'solution_file' not in request.files:
            return jsonify({
                "success": False,
                "message": "No file part in the request"
            }), 400

        solution_file = request.files['solution_file']

        # Validate file
        if solution_file.filename == '':
            return jsonify({
                "success": False,
                "message": "No file selected for upload"
            }), 400

        # Extract additional fields from the form data
        course_id = request.form.get('course_id')
        year = request.form.get('year')
        semester = request.form.get('semester')
        moed = request.form.get('moed')
        question_number = request.form.get('question_number')

        # Validate required fields
        if not all([course_id, year, semester, moed, question_number]):
            return jsonify({
                "success": False,
                "message": "Missing required parameters"
            }), 400

        # Call service layer to handle logic
        result = serviceLayer.uploadSolution(course_id, int(year), semester, moed,question_number, solution_file)
        parsed_result = json.loads(result)

        return jsonify({
            "success": parsed_result.get("status") == "success",
            "message": parsed_result.get("message"),
            "has_link": parsed_result.get("has_link", False),
            "link": parsed_result.get("link", None)
        }), 200 if parsed_result.get("status") == "success" else 400

    except Exception as e:
        print(f"Error in upload_full_exam_pdf: {str(e)}")
        return jsonify({
            "success": False,
            "message": "An unexpected error occurred.",
            "error": str(e)
        }), 500


@course_controller.route('/api/course/is_course_manager', methods=['POST'])
@cross_origin()
@jwt_required()
def is_course_manager():
    try:
        data = request.get_json()
        course_id = data.get('course_id')

        if not course_id:
            return jsonify({"success": False, "message": "Missing parameters"}), 400

        user_id = get_jwt_identity()
        result = serviceLayer.is_user_manager(course_id, user_id)
        print(f"Is user manager result for course {course_id} and user {user_id}: {result}")

        return jsonify({"success": True, "is_manager": result}), 200
    except Exception as e:
        print(f"Error in is_course_manager: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500
    

@course_controller.route('/api/course/delete_question', methods=['DELETE'])
@cross_origin()
@jwt_required()
def delete_question():
    try:
        data = request.get_json()
        course_id = data.get('course_id')
        year = data.get('year')
        semester = data.get('semester')
        moed = data.get('moed')
        question_number = data.get('question_number')

        # Validate input
        if not all([course_id, year, semester, moed, question_number]):
            return jsonify({"success": False, "message": "Missing parameters"}), 400

        # Call the service layer to delete the question
        serviceLayer.delete_question(course_id, year, semester, moed, question_number)
        return jsonify({"success": True, "message": "Question deleted successfully."}), 200
    except Exception as e:
        print(f"Error in delete_question: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500


@course_controller.route('/api/course/get_comments_metadata', methods=['GET'])
@cross_origin()
@jwt_required()
def get_comments_metadata():
    try:
        # Extract the question_id from query parameters
        question_id = request.args.get('question_id')

        # Validate input
        if not question_id:
            return jsonify({
                "success": False,
                "message": "Missing required parameter: question_id"
            }), 400

        # Fetch comment metadata from the service layer
        result = serviceLayer.get_comments_metadata(question_id)

        # Parse the result from the service layer
        parsed_result = json.loads(result)  # Assuming the service layer returns a JSON string
        if parsed_result.get("status") != "success":
            return jsonify({
                "success": False,
                "message": parsed_result.get("message", "Unknown error")
            }), 500

        # Return only the required metadata
        return jsonify({
            "success": True,
            "comments_metadata": parsed_result.get("message")
        }), 200
    except Exception as e:
        print(f"Error in get_comments_metadata: {str(e)}")
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

@course_controller.route('/api/course/delete_comment', methods=['POST', 'OPTIONS'])
@cross_origin()
@jwt_required()
def delete_comment():
    if request.method == 'OPTIONS':
        response = jsonify(success=True)
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response

    try:
        # Extract required fields from form data
        course_id = request.form.get('course_id')
        year = int(request.form.get('year'))
        semester = request.form.get('semester')
        moed = request.form.get('moed')
        question_number = int(request.form.get('question_number'))
        comment_id = request.form.get('comment_id')

        # Validate required fields
        required_fields = [course_id, year, semester, moed, question_number, comment_id]
        if any(field is None for field in required_fields):
            return jsonify({
                "success": False,
                "message": "Missing required fields."
            }), 400

        # Call the service layer
        result = serviceLayer.delete_comment(
            course_id, year, semester, moed, question_number, comment_id
        )

        # Parse the service response
        parsed_result = json.loads(result)
        return jsonify({
            "success": parsed_result.get("status") == "success",
            "message": parsed_result.get("message")
        }), 200

    except Exception as e:
        print(f"Error in delete_comment: {str(e)}")
        return jsonify({
            "success": False,
            "message": "An unexpected error occurred.",
            "error": str(e)
        }), 500

# @course_controller.route('/api/course/delete_comment', methods=['DELETE'])
# @cross_origin()
# @jwt_required()
# def delete_comment():
#     if request.method == 'OPTIONS':
#         response = jsonify(success=True)
#         response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
#         response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
#         response.headers.add('Access-Control-Allow-Methods', 'POST')
#         return response
#     try:
#         data = request.get_json()
#         comment_id = data.get('comment_id')
#
#
#         # Validate input
#         if not all([comment_id]):
#             return jsonify({"success": False, "message": "Missing parameters"}), 400
#
#         # Call the service layer to delete the question
#         serviceLayer.delete_comment(comment_id)
#         return jsonify({"success": True, "message": "Comment deleted successfully."}), 200
#     except Exception as e:
#         print(f"Error in delete_comment: {str(e)}")
#         return jsonify({"success": False, "message": str(e)}), 500
