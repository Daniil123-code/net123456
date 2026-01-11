from datetime import datetime

# The Moscow Times — Wednesday, October 2, 2002
m_times_date = 'Wednesday, October 2, 2002'
m_times_format = '%A, %B %d, %Y'

# The Guardian — Friday, 11.10.13
guardian_date = 'Friday, 11.10.13'
guardian_format = '%A, %d.%m.%y'

# Daily News — Thursday, 18 August 1977
daily_news_date = 'Thursday, 18 August 1977'
daily_news_format = '%A, %d %B %Y'

# Пример проверки:
dt_mt = datetime.strptime(m_times_date, m_times_format)
dt_tg = datetime.strptime(guardian_date, guardian_format)
dt_dn = datetime.strptime(daily_news_date, daily_news_format)

print(dt_mt)
print(dt_tg)
print(dt_dn)