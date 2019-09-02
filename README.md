Utils
=====

#### Deleting temporary files in linux

https://serverfault.com/questions/232525/df-in-linux-not-showing-correct-free-space-after-file-removal/232526

    df
    lsof | grep deleted
    killall -9 gdrive
    du -hs * | sort -rh | head -10
    
#### Creating svn service in Windows

    sc create svnserve binpath="\"C:\pathTo\svnserve.exe\" --service -r D:\repoPath" displayname="SVN Server" depend=Tcpip start=auto

#### Compressing folder

    sudo apt-get install zip unzip -y
    zip -r OUTPUT.zip FOLDER

#### Show system info

    cat /var/run/motd.dynamic

#### Adding user to Samba

    sudo useradd NewUser
    sudo usermod -a -G sambagroup NewUser
    sudo smbpasswd -a NewUser

#### Logging crontab

https://www.cyberciti.biz/faq/how-to-check-cron-logs-in-ubuntu-linux/

    $ sudo nano /etc/rsyslog.d/50-default.conf

    Uncoment the line (i.e. remove #):
    cron.*                          /var/log/cron.log
    
    $ sudo service rsyslog restart
    $ sudo service cron restart    

#### Scheduling: crontab

http://kvz.io/blog/2007/07/29/schedule-tasks-on-linux-using-crontab/

    $ sudo crontab -e

    ## minute : hour : day_of_month : month : day_of_week : command
    15 10,13,17 * * 1-6 /usr/svn/back.pl > /usr/svn/back.log 2>&1
    1 1 * * 2-6 /home/utils/backup_mantis.pl 2>&1
    0 23 * * 7 /usr/svn/backfull.pl > /usr/svn/backfull.log 2>&1
    @reboot /home/utils/rebootmail.pl

#### Making file executable: chmod

    $ chmod +x script.pl

#### Disk usage: du

    $ du -sk /path/* | sort -nr | while read size fname; 
      do for unit in k M G T P E Z Y; do if [ $size -lt 1024 ]; 
      then echo -e "${size}${unit}\t${fname}"; break; fi; size=$((size/1024)); done; done
    
#### Change user and group owner (recursive)

    $ chown -R username:group /path/directory/

#### Send file by FTP

    $ curl -T my-local-file.txt ftp://ftp.example.com --user username:password

#### Log into remote Samba directory and mount remote disk

    $ smbclient -L 192.168.98.253 -Uuser%password
    $ mount -t cifs "//192.168.98.253/svn" "/mnt/svn" -ouser=USER,pass=PASSWORD,domain=YUMI,rw

#### Download file by FTP

    $ curl --user username:password 'ftp://ftp.host.com/file' -o '/path/to/download'

#### Backup

    $ rsync -aAXv --exclude={"/dev/*","/proc/*","/sys/*","/tmp/*","/run/*","/mnt/*","/media/*","/lost+found","/usr/svn","/backup/*","/www/deploy/debug/*" } /* /backup/

#### Simlinks
##### Windows

    $ mklink /D C:\xampp\htdocs\www C:\dev\html\project\build

##### Linux
    $ ln -s /path/target /path/symlink
    
