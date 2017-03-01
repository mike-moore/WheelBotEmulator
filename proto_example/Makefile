# See README.txt.

.PHONY: all python clean

all: python

python: add_person_python list_people_python

clean:
	rm -f add_person_python list_people_python
	rm -f protoc_middleman addressbook_pb2.py
	rm -f *.pyc

protoc_middleman: addressbook.proto
	protoc --python_out=. addressbook.proto
	@touch protoc_middleman

add_person_python: add_person.py protoc_middleman
	@echo "Writing shortcut script add_person_python..."
	@echo '#! /bin/sh' > add_person_python
	@echo './add_person.py "$$@"' >> add_person_python
	@chmod +x add_person_python

list_people_python: list_people.py protoc_middleman
	@echo "Writing shortcut script list_people_python..."
	@echo '#! /bin/sh' > list_people_python
	@echo './list_people.py "$$@"' >> list_people_python
	@chmod +x list_people_python
