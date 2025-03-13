import face_recognition
import cv2
import numpy as np
import csv
from datetime import datetime
from threading import Thread
import pickle

# === THREADING CLASS FOR VIDEO CAPTURE ===
class VideoStream:
    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src)
        self.ret, self.frame = self.stream.read()
        self.stopped = False

    def start(self):
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        while not self.stopped:
            self.ret, self.frame = self.stream.read()

    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True
        self.stream.release()


# === LOAD KNOWN FACE ENCODINGS ===
def load_encodings(names, photos_path):
    """Load or generate known face encodings."""
    try:
        with open('encodings.pickle', 'rb') as f:
            known_face_encodings = pickle.load(f)
    except FileNotFoundError:
        known_face_encodings = []
        for name in names:
            img_path = f"{photos_path}/{name}.jpg"
            img = face_recognition.load_image_file(img_path)
            encoding = face_recognition.face_encodings(img)[0]
            known_face_encodings.append(encoding)
        # Save encodings for future use
        with open('encodings.pickle', 'wb') as f:
            pickle.dump(known_face_encodings, f)
    return known_face_encodings


# === INITIALIZE VARIABLES ===
known_faces_names = ["akshat", "mann", "vastani", "dave", "heman"]
photos_path = "C:\\Users\\aksha\\OneDrive\\Desktop\\ProjectC\\photos"
known_face_encodings = load_encodings(known_faces_names, photos_path)
attendance = {name: {"check_in": None, "check_out": None, "total_hours": None} for name in known_faces_names}

# CSV file for attendance
now = datetime.now()
current_date = now.strftime("%Y-%m-%d")
csv_file = open(current_date + '.csv', 'a+', newline='')
csv_writer = csv.writer(csv_file)

# Write header to CSV if it's a new file
csv_file.seek(0)
if not csv_file.read(1):  # Check if file is empty
    csv_writer.writerow(["Name", "Check-in", "Check-out", "Total Working Hours"])

# Face recognition variables
face_locations = []
face_encodings = []
face_names = []

# Start video stream
video_capture = VideoStream().start()

# Skip frames for better performance
frame_skip = 5
frame_count = 0

while True:
    frame = video_capture.read()
    frame_count += 1

    # Resize frame for faster processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    if frame_count % frame_skip == 0:
        # Detect faces and get encodings
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = ""
            face_distance = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distance)
            if matches[best_match_index]:
                name = known_faces_names[best_match_index]

            face_names.append(name)

            if name in known_faces_names:
                current_time = datetime.now().strftime("%H:%M:%S")
                if not attendance[name]["check_in"]:
                    # Mark check-in time
                    attendance[name]["check_in"] = current_time
                else:
                    # Update check-out time and calculate total hours
                    attendance[name]["check_out"] = current_time
                    check_in_time = datetime.strptime(attendance[name]["check_in"], "%H:%M:%S")
                    check_out_time = datetime.strptime(current_time, "%H:%M:%S")
                    total_time = check_out_time - check_in_time
                    attendance[name]["total_hours"] = str(total_time)

                # Write to CSV
                csv_writer.writerow([
                    name, 
                    attendance[name]["check_in"], 
                    attendance[name]["check_out"], 
                    attendance[name]["total_hours"]
                ])

    # Annotate the frame
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up since the frame is resized
        top *= 2
        right *= 2
        bottom *= 2
        left *= 2

        # Draw rectangle around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        # Draw name label below the rectangle
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
        cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

    # Display the frame
    cv2.imshow("Attendance System", frame)

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
video_capture.stop()
cv2.destroyAllWindows()
csv_file.close()
