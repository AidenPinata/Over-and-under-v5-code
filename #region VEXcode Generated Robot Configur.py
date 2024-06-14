#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain=Brain()

# Robot configuration code
left_motor_a = Motor(Ports.PORT3, GearSetting.RATIO_18_1, False)
left_motor_b = Motor(Ports.PORT10, GearSetting.RATIO_18_1, False)
left_drive_smart = MotorGroup(left_motor_a, left_motor_b)
right_motor_a = Motor(Ports.PORT2, GearSetting.RATIO_18_1, True)
right_motor_b = Motor(Ports.PORT11, GearSetting.RATIO_18_1, True)
right_drive_smart = MotorGroup(right_motor_a, right_motor_b)
drivetrain = DriveTrain(left_drive_smart, right_drive_smart, 319.19, 295, 40, MM, 7)
Arm = Motor(Ports.PORT6, GearSetting.RATIO_36_1, False)
controller_2 = Controller(PRIMARY)
Shoot = Motor(Ports.PORT7, GearSetting.RATIO_6_1, False)
Shooter2 = Motor(Ports.PORT8, GearSetting.RATIO_6_1, False)
controller_1 = Controller(PARTNER)


# wait for rotation sensor to fully initialize
wait(30, MSEC)


def play_vexcode_sound(sound_name):
    # Helper to make playing sounds from the V5 in VEXcode easier and
    # keeps the code cleaner by making it clear what is happening.
    print("VEXPlaySound:" + sound_name)
    wait(5, MSEC)

# add a small delay to make sure we don't print in the middle of the REPL header
wait(200, MSEC)
# clear the console to make sure we don't have the REPL in the console
print("\033[2J")



# define variables used for controlling motors based on controller inputs
drivetrain_needs_to_be_stopped_controller_1 = False

def rc_auto_loop_function_controller_1():
    global drivetrain_needs_to_be_stopped_controller_1, remote_control_code_enabled
    while True:
        if remote_control_code_enabled:
            
            # calculate the drivetrain motor velocities from the controller joystick axies
            # left = axis3 - axis4
            # right = axis3 + axis4
            drivetrain_left_side_speed = controller_1.axis3.position() - controller_1.axis4.position()
            drivetrain_right_side_speed = controller_1.axis3.position() + controller_1.axis4.position()
            
            # check if the values are inside of the deadband range
            if abs(drivetrain_left_side_speed) < 5 and abs(drivetrain_right_side_speed) < 5:
                if drivetrain_needs_to_be_stopped_controller_1:
                    left_drive_smart.stop()
                    right_drive_smart.stop()
                    drivetrain_needs_to_be_stopped_controller_1 = False
            else:
                drivetrain_needs_to_be_stopped_controller_1 = True
            
            if drivetrain_needs_to_be_stopped_controller_1:
                left_drive_smart.set_velocity(drivetrain_left_side_speed, PERCENT)
                left_drive_smart.spin(FORWARD)
                right_drive_smart.set_velocity(drivetrain_right_side_speed, PERCENT)
                right_drive_smart.spin(FORWARD)

        wait(20, MSEC)


#endregion VEXcode Generated Robot Configuration
remote_control_code_enabled = True

rc_auto_loop_thread_controller_1 = Thread(rc_auto_loop_function_controller_1)

# ------------------------------------------
# 
# 	Project:      VEXcode Project
#	Author:       VEX
#	Created:
#	Description:  VEXcode V5 Python Project
# 
# ------------------------------------------

# Library imports
from vex import *

def Shooter():
    global Motor_control
    if controller_2.buttonB.pressing():
            Motor_control = True
            brain.screen.print("SPIN")
            Shoot.spin(FORWARD, 6.0, VOLT)
            Shooter2.spin(REVERSE, 6.0, VOLT)

    elif controller_2.buttonA.pressing():
        if Motor_control:
            Motor_control = False
            brain.screen.print("STOP")
            Shoot.stop()
            Shooter2.stop()
            wait(5, MSEC)

    
def controller_DOWN_Pressed():
    Arm.spin(REVERSE)
    while controller_2.buttonDown.pressing():
        brain.screen.print("ARM DOWN")
        wait(5, MSEC)
    Arm.stop()

def controller_UP_Pressed():
    Arm.spin(FORWARD)
    while controller_2.buttonUp.pressing():
        brain.screen.print("ARM UP")
        wait(5, MSEC)
    Arm.stop()


#Motor detection for if its on or off
Motor_control = False


#Arm controls
controller_2.buttonUp.pressed(controller_UP_Pressed)
controller_2.buttonDown.pressed(controller_DOWN_Pressed)
wait (10, MSEC)

Arm.set_stopping(HOLD)

while True:
    Shooter()


