from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from fabapp.schdulers import UserRating


# gunicorn fab.wsgi:application --bind=localhost
def Ratingjob():
    scheduler = BackgroundScheduler(timezone="Asia/Kolkata")
    # scheduler.add_job(UserRating, 'cron', hour=19, minute=44)
    scheduler.add_job(UserRating, trigger='interval',seconds=10000)
    scheduler.start()

#def Resetjob():
   # reset_scheduler = BackgroundScheduler(timezone="Asia/Kolkata")
   # reset_scheduler.add_job(CronReset, 'cron', hour=19, minute=58)
    # reset_scheduler.add_job(CronReset, trigger='interval',seconds=3)
   # reset_scheduler.start()

#def DisableExijob():
   # disable_scheduler = BackgroundScheduler(timezone="Asia/Kolkata")
   # disable_scheduler.add_job(DisableExi, 'cron', hour=17, minute=19)
    # reset_scheduler.add_job(CronReset, trigger='interval',seconds=3)
   # disable_scheduler.start()
