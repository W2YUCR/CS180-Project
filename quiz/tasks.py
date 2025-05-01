from dramatiq import actor


@actor
def start_quiz(pk):
    print("Starting quiz with pk {}".format(pk))
