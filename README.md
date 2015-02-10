Utils
=====

crontab
-------

http://kvz.io/blog/2007/07/29/schedule-tasks-on-linux-using-crontab/

    $ sudo crontab -e
    
    ## minute : hour : day_of_month : month : day_of_week : command
    15 10,13,17 * * 1-6 /usr/svn/back.pl > /usr/svn/back.log 2>&1
    0 23 * * 7 /usr/svn/backfull.pl > /usr/svn/backfull.log 2>&1
    30 2 1 * * /usr/svn/backold.pl > /usr/svn/backold.log 2>&1
    @reboot /usr/svn/utils/rebootmail.pl


