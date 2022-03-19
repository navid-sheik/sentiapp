from celery import shared_task



@shared_task(bind=True)
def test_func2 (self):
    for i in range(10):
        print(i)
    return "Done"