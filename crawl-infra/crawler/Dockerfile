FROM python:3-slim

WORKDIR /crawler

# scrapy needs tkinter, we need cron for scheduling
RUN apt-get update && apt-get install -y --no-install-recommends\
    cron \
    python3-tk \
    wget \
    && rm -rf /etc/cron.*/* \
    && rm -rf /var/lib/apt/lists/*

# install python libraries
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# set up entry point to copy env variables to cron context
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

# place cron file defining crawl schedule
COPY crawl-schedule /etc/cron.d/crawl-schedule
# Give execution rights on cron job
RUN chmod 0644 /etc/cron.d/crawl-schedule
# Apply cron job
RUN crontab /etc/cron.d/crawl-schedule

COPY . .

# https://manpages.ubuntu.com/manpages/trusty/man8/cron.8.html
# -f | Stay in foreground mode, don't daemonize.
# -L loglevel | Tell  cron  what to log about jobs (errors are logged regardless of this value) as the sum of the following values:
CMD ["cron","-f", "-L", "2"]
