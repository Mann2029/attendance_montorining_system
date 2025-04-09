#Project name
# Attendance_montorining_system
# Team Members
1. Mann Chavda (Ku2407u327)
2. Akshat Bansal (Ku2407u251)
3. Meet Dave (Ku2407u331)
4. Heman Darji (Ku2407u779)
5. Meet Vastani (Ku2407u451)

# Overview
- This is a Face Recognition Attendance System that uses a webcam to detect and recognize faces in real time. It logs each person's check-in, check-out, and total working hours into a daily CSV file. Known faces are preloaded from images, and performance is boosted using multithreading and encoded face caching.

# Table of content
1. Overview
2. Requirements
3. Libaries Required
4. Known Images
5. How it works
6. output
7. Future Enhancements
8. Conclusion
9. Author

## Requirements
 - Python(3.8)

## Libaries Required
- face_recongition
- cv2
- numpy
- csv
- datetime
- threading(Thread)
- pickle

## known Images
- Place .jpg photos of the people you want to recognize in the photos/ directory. Ensure the file names match the names in the known_faces_names list inside the script, e.g., akshat.jpg, mann.jpg, etc.

## How it works
- On first run, the script encodes each known face from photos/ and saves them in encodings.pickle.
- It uses the webcam to capture frames, downsizes for speed, and looks for faces every few frames.
- When a known face is recognized:
  - If not already checked in, the system logs a check-in time.
  - If already checked in, it logs a check-out and computes total working time.
- All records are saved to a CSV file named with the current date.

## Output
The system generates a daily CSV file named with the current date (e.g., 2025-04-09.csv) that stores attendance records. Each time a known face is detected by the webcam, the system checks whether a check-in time has already been recorded for that person. If not, it logs the current time as the check-in. If the person is seen again later in the session, it updates the check-out time and calculates the total working hours based on the difference between check-in and check-out times. Each row in the CSV file contains the person's name, check-in time, check-out time, and total working hours. This file acts as a timestamped attendance sheet and is automatically updated in real time during the session.

### Exit From the video
 - To stop the program, press the q key on the video window.
   
## Future Enhancements
- While the current system effectively tracks attendance using real-time face recognition, there are several enhancements that could make it more robust, user-friendly, and scalable. One key improvement would be integrating a graphical user interface (GUI) to allow users to easily add or remove known faces, view attendance records, and control the session without editing the code. Another enhancement could involve using a database (such as SQLite or MySQL) instead of CSV files to manage attendance data more efficiently, especially for long-term storage and retrieval. Additionally, incorporating duplicate detection prevention can help avoid multiple check-ins or check-outs for the same person within short timeframes. Expanding support to work with multiple camera feeds or network-based IP cameras could also make the system suitable for larger environments like offices or schools. Finally, adding features like face mask detection, real-time alerts, or a web-based dashboard could make the system more intelligent and adaptable for modern-day use cases.

## Conclusion
- This Face Recognition Attendance System offers a practical and efficient way to automate attendance tracking using real-time video and facial recognition technology. By leveraging libraries like face_recognition and OpenCV, it eliminates the need for manual sign-ins, reducing both time and human error. The system is lightweight, easy to deploy, and records attendance data in a structured format for daily use. While the current version is functional and accurate for small to medium-scale use, it also lays a strong foundation for future enhancements such as GUI integration, database support, and multi-camera capabilities. Overall, it provides a smart and scalable solution for modern attendance management.

## Author
- This Project is developed by Team StayTech
 
