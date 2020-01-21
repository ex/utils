Journal
=======

##### 2020

- [nodejs] pm2 process must start from app root directory to find paths!

	https://github.com/Unitech/pm2/issues/96
	
	cd /var/www/node/myapp; pm2 start myapp.js

##### 2017

- I keep forgetting that Tortoise SVN ignores by default *.a files and they can be required libraries.
- For CGIs to write files, the file needs to below to the apache group: chown www-data:sambagroup file.txt
- I keep forgetting CGI scripts don't like PC ending lines encoding and fail on linux
- Don't use Perl for web scrapping, wasted too much time trying to do something trivial with Python:
  maintain session cookies between calls, oh man I tryed all the cpan packages in disbelief...
