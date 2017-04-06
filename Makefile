.PHONY: all build_sim run_tests clean

all: build_sim run_tests

build_sim:
	@echo "Building WheelBot Trick sim."
	cd trick_sim; make spotless; trick-CP
	cd ../

run_tests:
	@echo "Running Command and Tracking System Unit-Tests"
	./UtEmulatedSerialComm.py
	./UtCommandAndTracking.py

clean:
	rm -f *.pyc
