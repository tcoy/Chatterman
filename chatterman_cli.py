from chatterbrain.chatterbrain import ChatterBrain
from chatterbrain.teachers.reddit import RedditTeacher

brain = ChatterBrain()
reddit_teacher = RedditTeacher(brain)

while True:
    line = input()

    if '.reddit' in line:
        print(reddit_teacher.teach(line.split()[1]))
        continue

    brain.learn(line)
    response = brain.get_response(line)

    if response is not None:
        print(response)
