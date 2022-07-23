#title           :Makefile
#description     :Create all executable script for kebabaser minecraft server
#author			 :Adrian Fernández Cintado <afercin@gmail.com>
#date            :20220723
#version         :1.0
#usage			 :makefile
#==============================================================================

all: simulatorSource

clean:
	rm -rf source/_build

simulatorSource:
	mkdir -p _build

	pyinstaller --onefile source/mcApi.py --distpath source/_build/ --workpath /tmp/