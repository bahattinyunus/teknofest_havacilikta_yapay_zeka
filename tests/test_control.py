import pytest
import sys
import os

# Add src to python path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.control.flight_controller import PIDController, FlightController

class TestPID:
    def test_proportional(self):
        pid = PIDController(kp=1.0, ki=0.0, kd=0.0, setpoint=10)
        output = pid.update(0)
        assert output == 10.0 # Error is 10, kp is 1 -> output 10

    def test_setpoint_change(self):
        pid = PIDController(kp=0.5, ki=0.0, kd=0.0)
        pid.setpoint = 100
        output = pid.update(50)
        assert output == 25.0 # Error 50 * 0.5 = 25

class TestFlightController:
    def test_initial_state(self):
        fc = FlightController()
        assert fc.state["mode"] == "DISARMED"
        assert fc.state["altitude"] == 0.0

    def test_arming(self):
        fc = FlightController()
        fc.arm()
        assert fc.state["mode"] == "ARMED"

    def test_motor_mixing(self):
        fc = FlightController()
        fc.update_state({"roll": 0, "pitch": 0, "yaw": 0, "altitude": 0})
        
        # Target hover at 0
        targets = {"roll": 0, "pitch": 0, "yaw": 0, "altitude": 0}
        outputs = fc.calculate_motor_outputs(targets)
        
        # Check if all motors have base throttle
        assert outputs["m1"] > 1000
        # In perfect hover, they should be roughly equal
        assert abs(outputs["m1"] - outputs["m2"]) < 1.0 
