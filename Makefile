.PHONY: all update_interface clean

all: update_interface run_tests

clean:
	rm -f wb_comm_if_pb2.py
	rm -f *.pyc

update_interface: wb_comm_if.proto
	protoc --python_out=. wb_comm_if.proto
	@echo "WheelBot communication interface has been updated."

run_tests:
	@echo "Running Command and Tracking System Unit-Tests"
	./UtCommandAndTracking.py

