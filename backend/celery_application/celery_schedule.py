from celery_application.celery_app import celery_app

from celery.schedules import crontab

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    from celery_application.tasks import user_email_reminder,user_monthly_report
    sender.add_periodic_task(crontab(hour=8,minute=5), user_email_reminder.s(),name="Daily Reminder for User")
    
    sender.add_periodic_task(crontab(day_of_month=1,hour=8,minute=5),user_monthly_report.s(),name="Monthly Reports for User")
    
    
