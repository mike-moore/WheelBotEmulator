#ifndef TEST_VEHICLE_HH
#define TEST_VEHICLE_HH
/*************************************************************************
PURPOSE: ()
**************************************************************************/
#include "Guidance/include/point.hh"
#include "Control/include/vehicleController.hh"
#include "Control/include/differentialDriveController.hh"
#include "Motor/include/DCMotorSpeedController.hh"

class VehicleOne {
    public:
    Navigator *navigator;
    MotorSpeedController* rightMotorController;
    MotorSpeedController* leftMotorController;
    DCMotor* rightDCMotor;
    DCMotor* leftDCMotor;

    DifferentialDriveController* driveController;
    VehicleController* vehicleController;

    double distanceBetweenWheels;     /* m */
    double wheelRadius;               /* m */
    double vehicleMass;               /* kg */
    double ZAxisMomentofInertia;

    // Vehicle Controller Parameters
    double slowDownDistance;          /* m */
    double arrivalDistance;           /* m */
    double wheelSpeedLimit;           /* r/s */
    double headingRateLimit;          /* r/s */
    double wheelDragConstant;         /* */
    double corningStiffness;          /* */

    // DCMotor Parameters
    double DCMotorInternalResistance; /* ohm */
    double DCMotorTorqueConstant;     /* N*m/amp */

    double position[2];              /* m */
    double velocity[2];              /* m/s */
    double acceleration[2];          /* m/s2 */

    double heading;                  /* r */
    double headingRate;              /* r/s */
    double headingAccel;             /* r/s2 */

    double rightMotorSpeed;          /* r/s */
    double leftMotorSpeed;           /* r/s */

    // Forces
    double driveForce[2];            /* N */
    double lateralTireForce[2];      /* N */
    double rollingResistForce[2];    /* N */
    double forceTotal[2];            /* N */
    double vehicleZTorque;           /* N*m */

    double batteryVoltage;

    int default_data();
    int state_init();
    void control();
    int state_deriv();
    int state_integ();
};

#endif
