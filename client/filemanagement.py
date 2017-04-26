# coding: utf-8
from __future__ import print_function
import threading
import sys
import termios
import tty

BUFFERSIZE=1024
class Reception(threading.Thread):

	def __init__(self, conn, emission):
		threading.Thread.__init__(self)
		self.conn = conn
		self.reception = True
		self.emission = emission

	def run(self):
		while self.reception:
			try:
				bufferrecep=self.conn.recv(BUFFERSIZE)
			except Exception as e:
				print (e)
				pass
			else:
				if bufferrecep:
					print(bufferrecep, end='')
					sys.stdout.flush()
				if bufferrecep == "endVim":
					self.emission.Stop()
					self.reception = False

class Emission(threading.Thread):

	def __init__(self, conn):
		threading.Thread.__init__(self)
		self.conn = conn
		self.edition = True


	def run(self):
		fd=sys.stdin.fileno()
		oSettings = termios.tcgetattr(fd)
		tty.setraw(sys.stdin.fileno())

		while self.edition:
			self.conn.send(sys.stdin.read(1))

		termios.tcsetattr(fd, termios.TCSADRAIN, oSettings)


	def Stop(self):
		self.edition=False
		print("stop edition")
