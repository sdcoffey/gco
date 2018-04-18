default: test

test:
	nosetests --nocapture

install:
	cp gco.py /usr/local/bin/gco
	chmod +x /usr/local/bin/gco
