from pyPS4Controller.controller import Controller
from move import move, steady, steady_X, dove, look_up, look_down, look_left, look_right, look_home
import Adafruit_PCA9685
from threading import Thread
from rpi_ws281x import *
import time
import LED
command = ""
speed = ""

class MyController(Controller, Thread):

	def __init__(self, **kwargs):
		Controller.__init__(self, **kwargs)
		self.step = 1
		self.led = LED.LED()
		self.color = 0


	def on_up_arrow_press(self):
		global command
		command = "no"

	def on_down_arrow_press(self):
		global command
		command = "s"

	def on_up_down_arrow_release(self):
		global command
		command = ""

	def on_left_arrow_press(self):
		global command
		command = "left"

	def on_right_arrow_press(self):
		global command
		command = "right"
			
	def on_left_right_arrow_release(self):
		global command
		command = ""

	def on_playstation_button_press(self):
		global command
		command = "reset"

	def on_playstation_button_release(self):
		global command
		command = ""

	def on_R1_press(self):
		global command
		command = "steady"

	def on_R1_release(self):
		global command
		command = ""

	def on_R2_press(self, value):
		global speed
		speed = "fast"
		
	def on_R2_release(self):
		global speed
		speed = ""
	
	def on_L2_press(self, value):
		global speed
		speed = "slow"
		
	def on_L2_release(self):
		global speed
		speed = ""
		
	def on_circle_press(self):
		global command
		command = "circle"
		
	def on_circle_release(self):
		global command
		command = ""

	def on_R3_up(self, value):
		global command
		command = "lookup"

	def on_R3_down(self, value):
		global command
		command = "lookdown"

	def on_R3_left(self, value):
		global command
		command = "lookleft"

	def on_R3_right(self, value):
		global command
		command = "lookright"

	def on_R3_y_at_rest(self):
		global command
		command = ""

	def on_R3_x_at_rest(self):
		global command
		command = ""

	def on_options_press(self):
		self.color += 1
		if self.color == 1:
			self.led.colorWipe(Color(255, 255, 255))
		if self.color == 2:
			self.led.colorWipe(Color(255, 0, 0))
		if self.color == 3:
			self.led.colorWipe(Color(255, 255, 0))
		if self.color == 4:
			self.led.colorWipe(Color(0, 255, 0))
		if self.color == 5:
			self.led.colorWipe(Color(0, 255, 255))
		if self.color == 6:
			self.led.colorWipe(Color(0, 0, 255))
		if self.color == 7:
			self.led.colorWipe(Color(255, 0, 255))
		if self.color == 8:
			self.led.colorWipe(Color(0, 0, 0))
			self.color = 0

	def on_options_release(self):
		pass


pwm =  Adafruit_PCA9685.PCA9685()
led = LED.LED()

if __name__ == '__main__':
	
	controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv = False, event_definition = None)

	t = Thread(target= controller.listen)
	t.start()

	def func():
		step = 1
		pwm.set_all_pwm(0,300)
		look_home()
		DPI = 17
		color = 0
		while 1:
			global command
			global speed
			if ((command == "no") or (command == "s") or (command == "left") or (command == "right")) and (speed == "fast"):
				move(step, 55, command)
				step += 1
				if step > 4:
					step = 1
				time.sleep(0.08)
			
			elif ((command == "no") or (command == "s") or (command == "left") or (command == "right")) and (speed == "slow"):
				if command == "s":
					dove(step, -35, 0.001, DPI, "no")
					step += 1
					if step > 4:
						step = 1

				else:
					dove(step, 35, 0.001, DPI, command)
					step += 1
					if step > 4:
						step = 1

			elif (command == "no") or (command == "s") or (command == "left") or (command == "right"):
				move(step, 25, command)
				step += 1
				if step > 4:
					step = 1
				time.sleep(0.08)
			
			if command == "reset":
				look_home()
				pwm.set_all_pwm(0,300)

			if command == "steady":
				steady_X()
				steady()

			if command == "circle":
				pwm.set_all_pwm(0,300)
				step = 1
				for _ in range(44):
					move(step, 55, "left")
					step += 1
					if step > 4:
						step = 1
					time.sleep(0.08)
			
			if command == "lookup":
				look_up()
				time.sleep(0.01)
			
			if command == "lookdown":
				look_down()
				time.sleep(0.01)

			if command == "lookleft":
				look_left()
				time.sleep(0.01)

			if command == "lookright":
				look_right()
				time.sleep(0.01)

	t2 = Thread(target = func) 
	t2.start()