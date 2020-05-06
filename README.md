## File Structure

### backend_server.py:
	- background process
	- message queue

### frontend_server.py
	- do request to backend_server

### templates
	- home.html: homepage, input form (URL)
	- download.html: template complete with Stomp.js configuration

### cots.log: log produces by `wget`
