

from email.mime.text import MIMEText


templates = {

# tutorship
"TUTORSHIP_REQUEST_SUBJECT": "Physics Tutoring - New Tutoring Request",
"TUTORSHIP_REQUEST_BODY": """{student_name} has just requested you as a tutor for {course_name}!
Check it out at <a href="https://www.princetonphysicstutoring.org/">https://www.princetonphysicstutoring.org</a>, or email <a href="mailto:pptutoringportal@gmail.com">pptutoringportal@gmail.com</a> if you have any questions or concerns.
""",

"TUTORSHIP_ACCEPT_SUBJECT": "Physics Tutoring - Your New Tutor",
"TUTORSHIP_ACCEPT_BODY": """{tutor_name} has accepted you as a student for {course_name}!
See their contact info at <a href="https://www.princetonphysicstutoring.org/">https://www.princetonphysicstutoring.org</a>, or email <a href="mailto:pptutoringportal@gmail.com">pptutoringportal@gmail.com</a>  if you have any questions or concerns.
""",

"TUTORSHIP_DENY_SUBJECT": "Physics Tutoring Notification",
"TUTORSHIP_DENY_BODY": """{tutor_name} has declined your request for a tutor in {course_name}.
See more available tutors at <a href="https://www.princetonphysicstutoring.org/">https://www.princetonphysicstutoring.org</a>, or email <a href="mailto:pptutoringportal@gmail.com">pptutoringportal@gmail.com</a> if you have any questions or concerns.
""",

# tutor_course
"TUTOR_COURSE_ACCEPT_FIRST_SUBJECT":"Physics Tutoring - You've Been Approved!",
"TUTOR_COURSE_ACCEPT_FIRST_BODY":"""Hi {tutor_name},
<br><br>
Thank you so much for signing up to tutor this semester! We're happy to let you know that you've been accepted as a tutor for {course_name}.
<br><br>
We would like to start the hiring process through Student Employment (SE) as soon as possible. To that end, if you haven't worked on campus before, please complete an I-9 form and enroll in Direct Deposit. Hopefully you'll soon be able to see the job in TimesheetX (accessible via TigerHub). That is where you will log your hours. Please let us know by replying to this email if you aren't notified by SE about your hire within the next few days.
<br><br>
Tutees have already begun to sign up—this year, we're doing things a little differently, so tutees will request a specific tutor via the <a href="https://www.princetonphysicstutoring.org/">tutoring portal</a>. If a tutee requests you, you will get an email notification (which may go to your spam folder, so please keep an eye out!) at which point you can go to the portal and accept or reject the request. Please do this in a timely manner! The tutee will be notified if you accept or reject their request.
<br><br>
Once you accept a tutee, please make sure you reach out to them within 24 hours to set up a time to start meeting.
<br><br>
You may find yourself with more requests than you have capacity for—that's okay! Until we implement a button/checkbox for you to mark whether or not you're available, you may use your tutor biography to indicate whether or not you're currently accepting new tutees. In any event, your bio is a useful place for you to describe your experience with physics, teaching, and anything else that may be relevant for students to know as they choose a tutor.
<br><br>
We also want to remind everyone of a few logistical/policy things—you're expected to be available at least one hour per week per student; if you need more than two hours per week per student you need approval from Karen (see our policies linked below), and you're not expected to tutor during midterms/finals/breaks. Please also remember that tutors and tutees must adhere to the Physics Department's Code of Conduct in all interactions. Finally (obviously), please make sure you don't give tutees the answers or tell them how to solve a problem! 
<br><br>
A full list of our policies can be found <a href="https://docs.google.com/document/d/1JIH6_cUSozt7KLOcld7FoW4Zs5U5atYPmVb5JyhhKrU/edit?usp=sharing">here</a>; please take a couple minutes to read through these policies before you begin accepting tutees. If you would like to view a syllabus for the course(s) you're tutoring, syllabi can be found <a href="https://drive.google.com/drive/folders/1aEI2gH0r-wX238R4bHr0LDCvj2WutBG6">here</a>.
<br><br>
Lastly, if at any point you decide that you are unable to continue tutoring, please let us know immediately. Your health and well-being (academic, mental, and emotional) are far more important! You can reach out to our team at <a href="mailto:pptutoringportal@gmail.com">pptutoringportal@gmail.com</a> or directly to Hanako Helton, the undergraduate manager, at <a href="mailto:hhelton@princeton.edu">hhelton@princeton.edu</a>. 
<br><br>
Please let us know if you have any questions!
<br><br>
Wishing you a fun and fulfilling semester,<br>
Hanako and the PPT Team""",

"TUTOR_COURSE_ACCEPT_SUBJECT":"Physics Tutoring - You've Been Approved!",
"TUTOR_COURSE_ACCEPT_BODY":"""You have been officially approved as a tutor for {course_name}! Check it out at <a href="https://www.princetonphysicstutoring.org/">https://www.princetonphysicstutoring.org</a>, or email <a href="mailto:pptutoringportal@gmail.com">pptutoringportal@gmail.com</a> if you have any questions or concerns.""",


"TUTOR_COURSE_DENY_SUBJECT":"Physics Tutoring - Notification",
"TUTOR_COURSE_DENY_BODY":"""Your application to be a tutor for {course_name} has been declined. If you think this decision was made in error, you may re-apply at <a href="https://www.princetonphysicstutoring.org/">https://www.princetonphysicstutoring.org</a> if you have any questions or concerns.""",
}