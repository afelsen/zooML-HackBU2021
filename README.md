For Hack BU 2021, we wanted to solve a problem facing today's Binghamton University community.

We ended up creating an overlay for Zoom which uses artificial intelligence to help teachers analyze how their students are doing, such that student-and-teacher interaction can be improved.

The code base exists in three parts:

1. An overlay using tkinter, which goes over Zoom (or any video conferencing app, such as Skype or Discord) to view the students and highlight them.

2. A facial recognition program, which analyzes student faces in a given image, and crops them out for the Convolutional Neural Network.

3. A Convolutional Neural Network, trained with a custom dataset that we made, which analyzes the features in a 128 x 128 grayscale image of a face (as cropped out by the facial recognition program) to output the state of a student.

The "state" of a student is one of four options:
- "talking"
- "attentive"
- "inattentive"
- "confused"

Combined, these three parts create an overlay which allows a teacher to see, in realtime, which students are confused, attentive, inattentive, and talking.