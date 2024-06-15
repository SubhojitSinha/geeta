# from models.yt_scrap_model import db_details, test_insert
def hello_world():
    return '<h1>Hello World</h1>'
    print("Start")
    Account().delete_on_thread({'name':"Avijit"})
    print("End")
    return f"delete_on_thread: {random.randint(1, 10)}"