#include "Control/include/vehicleController.hh"
#include <iostream>

VehicleController::VehicleController( Navigator& theNavigator,
                                      DifferentialDriveController& theDriveController,
                                      double arrival_distance):
   navigator(theNavigator),
   driveController(theDriveController) {

    // Enforce minimum arrival distance.
    if (arrival_distance > 0.01) {
        arrivalDistance = arrival_distance;
    } else {
        arrivalDistance = 0.01;
    }
    destination = waypointQueue.begin();
    WayPointReached = false;
    printDestination();
}

int VehicleController::getCurrentDestination(Point& currentDestination) {
    if (destination != waypointQueue.end()) {
        currentDestination = *destination;
        return 0;
    }
    return 1;
}

void VehicleController::printDestination() {
    if (destination != waypointQueue.end()) {
        std::cout << "Destination = (" << destination->x << "," << destination->y << ")." << std::endl;
    } else {
        std::cout << "No Destination." << std::endl;
    }
}

void VehicleController::add_waypoint(double x, double y) {
    std::cout << "Adding way point: " << x << ", " << y << std::endl;
    Point wayPoint(x,y);
    if (waypointQueue.empty()){
       waypointQueue.push_back(wayPoint);
       destination = waypointQueue.begin();
    }else{
       waypointQueue.push_back(wayPoint);
    }
}

void VehicleController::update() {

    if (destination == waypointQueue.end()) {
        WayPointReached = 0;
        driveController.update(0.0, 0.0);
        driveController.stop();
    } else {
        WayPointReached = 0;
        double distance_err = navigator.distanceTo(*destination);
        if ( distance_err > arrivalDistance) {
            double heading_err = navigator.bearingTo(*destination);
            driveController.update(distance_err, heading_err);
        } else {
            std::cout << "Arrived at Destination." << std::endl;
            WayPointReached = 1;
            destination ++;
            if (destination == waypointQueue.end()){
                std::cout << "All way-points reached.... IDLING" << std::endl;
                waypointQueue.clear();
                destination = waypointQueue.end();
                driveController.update(0.0, 0.0);
                driveController.stop();
            }else{
                printDestination();
            }
        }
    }
}


