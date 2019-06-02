import face_recognition
import cv2
import sys
import numpy as np
import configparser

# Jakub Podolak (jjp241) 2019, based on face_recognition module: https://github.com/ageitgey/face_recognition
# Totally OpenSource project, hope u all have fun!

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

#function to read paths to face images from config file
def get_faces(config):
    face_files = config.items("FACES")
    faces = [second for first,second in face_files]
    return faces

#function reads names of faces
def get_names(config):
    face_files = config.items("FACES")
    names = [first for first,second in face_files]
    return names

#function creates array of face encodings
def get_face_encodings(faces):
    known_face_encodings = []
    for face in faces:
        image = face_recognition.load_image_file(face)
        temp_encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(temp_encoding)
    return known_face_encodings

def run():
    #initialize config parser, read from config file passed as an argument
    config_file = sys.argv[1]
    config = configparser.ConfigParser()
    config.read(config_file)

    #read some settings from config file
    output_names_path = config['SETTINGS']['output']
    compression_factor = float(config['SETTINGS']['compression_factor'])
    webcam_port = int(config['SETTINGS']['webcam_port'])
    kill_key = config['SETTINGS']['kill_key']
    #create arrays for our face recognition
    face_paths = get_faces(config)
    known_face_names = get_names(config)
    known_face_encodings = get_face_encodings(face_paths)

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    # Get a reference to webcam on specified port (the default one)
    video_capture = cv2.VideoCapture(webcam_port)

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx= compression_factor, fy= compression_factor)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            #print(face_locations)
            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # Use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    #get the name of best matching face
                    name = known_face_names[best_match_index]
                    #write it to the buffer
                    buffer = open(output_names_path, "a")
                    buffer.write('\n' + name)
                    buffer.close()

                face_names.append(name)

        process_this_frame = not process_this_frame

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled
            top *= int(1/compression_factor)
            right *= int(1/compression_factor)
            bottom *= int(1/compression_factor)
            left *= int(1/compression_factor)

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit kill_key specified in config file on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord(kill_key):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()

run()
