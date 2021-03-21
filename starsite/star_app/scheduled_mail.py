def scheduled_mail():
    subject = 'Djangoアプリから通知'
    massege = 'おはようございます。本日はhogehogeの予定があります。'
    from_mail = settings.DEFAULT_FROM_EMAIL
    recipient = ["startaiyo0104@gmail.com"]
    send_mail(subject, massege, from_mail, recipient)