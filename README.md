Utils
=====

#### Downloading a file from Google Drive

https://stackoverflow.com/questions/25010369/wget-curl-large-file-from-google-drive

    Replace FILEID and FILENAME:
    
    $ wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=FILEID' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=FILEID" -O FILENAME && rm -rf /tmp/cookies.txt

#### Deleting full directories recursively and forcefully (DON'T USE THIS IN ROOT)

    $ sudo rm -rf dirs_*

#### Silently extracting protected 7z file

    $ nohup 7z x file.7z -o"/mnt/efs/fs1/" -pPASSWORD -y &

#### Keep process running after SSH disconnection

    $ nohup long-running-process &
    to see the log:
    $ tail -f nohup.out

#### Check if a process is running

    $ ps -ef | grep backup

#### Install 7zip in AWS Linux

https://gist.github.com/marcesher/7168642

    $ sudo yum-config-manager --enable epel
    $ sudo yum install -y p7ip
    $ sudo cp /usr/bin/7za /usr/bin/7z

#### Disk usage: du

    $ du -h -d1 /usr/svn/

#### HTTP SVN server

http://northwaygames.com/setting-up-subversion-on-amazon-ec2-for-free/

http://crazyadmins.com/tag/how-to-install-svn-server-on-amazon-ec2/

	LoadModule dav_svn_module     modules/mod_dav_svn.so
	LoadModule authz_svn_module   modules/mod_authz_svn.so
	LoadModule dontdothat_module  modules/mod_dontdothat.so
	<Location /svn>
	   DAV svn
	   SVNParentPath /var/www/svn
	   AuthType Basic
	   AuthName "Authorization SVN"
	   AuthzSVNReposRelativeAccessFile authz
	   AuthUserFile /etc/svn-auth-users
	   Require valid-user
	</Location>

https://askubuntu.com/questions/767504/permissions-problems-with-var-www-html-and-my-own-home-directory-for-a-website

	sudo chgrp -R apache /var/www/svn
	sudo find /var/www/svn -type d -exec chmod g+rx {} +
	sudo find /var/www/svn -type f -exec chmod g+r {} +
        
    sudo htpasswd -m /etc/svn-auth-users newuser

#### Testing POST apis with curl

    curl -d "{\"key1\":\"value1\"}" -H "Content-Type: application/json" -X POST http://localhost:8085/echo
    
    router.post( '/echo', ( req, res ) => {
        logger.debug( `echo/ ${JSON.stringify( req.body )}` );
        res.send( req.body );
    } );    

#### Adding mysql super user with remote access

https://stackoverflow.com/questions/6239131/how-to-grant-remote-access-permissions-to-mysql-server-for-user/27644973

    CREATE USER 'user'@'localhost' IDENTIFIED BY 'pwd';
    GRANT ALL PRIVILEGES ON *.* TO 'user'@'localhost' WITH GRANT OPTION;

    CREATE USER 'user'@'%' IDENTIFIED BY 'pwd';
    GRANT ALL PRIVILEGES ON *.* TO 'user'@'%' WITH GRANT OPTION;

    SHOW GRANTS FOR user;
    FLUSH PRIVILEGES;

#### Ignoring a directory on a checked out SVN repo

    svn update --set-depth exclude folderToIgnore

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

#### Change user and group owner (recursive)

    $ chown -R username:group /path/directory/

#### Send file by FTP

    $ curl -T my-local-file.txt ftp://ftp.example.com --user username:password

#### Log into remote Samba directory and mount remote disk

    $ smbclient -L 192.168.98.253 -Uuser%password
    $ mount -t cifs "//192.168.98.253/svn" "/mnt/svn" -ouser=USER,pass=PASSWORD,domain=YUMI,rw

#### Download file by FTP

    $ curl --user username:password 'ftp://ftp.host.com/file' -o '/path/to/download'

#### Simlinks
##### Windows

    mklink [[/d] | [/h] | [/j]] <Link> <Target>
    $ mklink /D C:\xampp\htdocs\www C:\dev\html\project\build

##### Linux
    $ ln -s /path/target /path/symlink
    
