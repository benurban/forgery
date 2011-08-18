# tracer.py

# Copyright (c) 2011 by Ben Urban <benurban@users.sourceforge.net>.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

from functools import wraps
import sys
import inspect

class Tracer(object):
	depth = 0
	tracing = True
	
	def traced(self, func):
		
		class Unobtainium:
			pass
		
		args, varargs, keywords, defaults = inspect.getargspec(func)
		total = len(args or ())
		optional = len(defaults or ())
		required = total - optional
		if varargs or keywords:
			raise TypeError("Cannot trace function %r which uses * or **" % (func, ))
		elif total == func.__name__.count('_') + 1 and not optional:
			pyobjc = True
			format = u'[%%r %s]' % (func.__name__.replace('_', ':%r ').rstrip(' '), )
		else:
			pyobjc = False
			formats = (None, ) * required + tuple(u'%s(%s)' % (func.__name__, ', '.join(('%r', ) * i)) for i in range(required, total + 1))
		
		# PyObjC complains about *args, so we have to call this indirectly
		@wraps(func)
		def wrapper(*args):
			if pyobjc:
				self.traceEntry(format, *args)
			else:
				for arg in list(reversed(args)):
					if arg is Unobtainium:
						args = args[:-1]
				self.traceEntry(formats[len(args)], *args)
			try:
				result = func(*args)
			except:
				sys.excepthook(*sys.exc_info())
				if pyobjc:
					self.traceException(format, sys.exc_info()[0], *args)
				else:
					self.traceException(formats[len(args)], sys.exc_info()[0], *args)
				raise
			else:
				if pyobjc:
					self.traceExit(format, result, *args)
				else:
					self.traceExit(formats[len(args)], result, *args)
				return result
		
		@wraps(func)
		def wrapper0_0():
			return wrapper()
		@wraps(func)
		def wrapper0_1(opt0 = Unobtainium):
			return wrapper(opt0)
		@wraps(func)
		def wrapper0_2(opt0 = Unobtainium, opt1 = Unobtainium):
			return wrapper(opt0, opt1)
		@wraps(func)
		def wrapper0_3(opt0 = Unobtainium, opt1 = Unobtainium, opt2 = Unobtainium):
			return wrapper(opt0, opt1, opt2)
		@wraps(func)
		def wrapper1_0(arg0):
			return wrapper(arg0)
		@wraps(func)
		def wrapper1_1(arg0, opt0 = Unobtainium):
			return wrapper(arg0, opt0)
		@wraps(func)
		def wrapper1_2(arg0, opt0 = Unobtainium, opt1 = Unobtainium):
			return wrapper(arg0, opt0, opt1)
		@wraps(func)
		def wrapper1_3(arg0, opt0 = Unobtainium, opt1 = Unobtainium, opt2 = Unobtainium):
			return wrapper(arg0, opt0, opt1, opt2)
		@wraps(func)
		def wrapper2_0(arg0, arg1):
			return wrapper(arg0, arg1)
		@wraps(func)
		def wrapper2_1(arg0, arg1, opt0 = Unobtainium):
			return wrapper(arg0, arg1, opt0)
		@wraps(func)
		def wrapper2_2(arg0, arg1, opt0 = Unobtainium, opt1 = Unobtainium):
			return wrapper(arg0, arg1, opt0, opt1)
		@wraps(func)
		def wrapper2_3(arg0, arg1, opt0 = Unobtainium, opt1 = Unobtainium, opt2 = Unobtainium):
			return wrapper(arg0, arg1, opt0, opt1, opt2)
		@wraps(func)
		def wrapper3_0(arg0, arg1, arg2):
			return wrapper(arg0, arg1, arg2)
		@wraps(func)
		def wrapper3_1(arg0, arg1, arg2, opt0 = Unobtainium):
			return wrapper(arg0, arg1, arg2, opt0)
		@wraps(func)
		def wrapper3_2(arg0, arg1, arg2, opt0 = Unobtainium, opt1 = Unobtainium):
			return wrapper(arg0, arg1, arg2, opt0, opt1)
		@wraps(func)
		def wrapper3_3(arg0, arg1, arg2, opt0 = Unobtainium, opt1 = Unobtainium, opt2 = Unobtainium):
			return wrapper(arg0, arg1, arg2, opt0, opt1, opt2)
		@wraps(func)
		def wrapper4_0(arg0, arg1, arg2, arg3):
			return wrapper(arg0, arg1, arg2, arg3)
		@wraps(func)
		def wrapper4_1(arg0, arg1, arg2, arg3, opt0 = Unobtainium):
			return wrapper(arg0, arg1, arg2, arg3, opt0)
		@wraps(func)
		def wrapper4_2(arg0, arg1, arg2, arg3, opt0 = Unobtainium, opt1 = Unobtainium):
			return wrapper(arg0, arg1, arg2, arg3, opt0, opt1)
		@wraps(func)
		def wrapper4_3(arg0, arg1, arg2, arg3, opt0 = Unobtainium, opt1 = Unobtainium, opt2 = Unobtainium):
			return wrapper(arg0, arg1, arg2, arg3, opt0, opt1, opt2)
		@wraps(func)
		def wrapper5_0(arg0, arg1, arg2, arg3, arg4):
			return wrapper(arg0, arg1, arg2, arg3, arg4)
		@wraps(func)
		def wrapper5_1(arg0, arg1, arg2, arg3, arg4, opt0 = Unobtainium):
			return wrapper(arg0, arg1, arg2, arg3, arg4, opt0)
		@wraps(func)
		def wrapper5_2(arg0, arg1, arg2, arg3, arg4, opt0 = Unobtainium, opt1 = Unobtainium):
			return wrapper(arg0, arg1, arg2, arg3, arg4, opt0, opt1)
		@wraps(func)
		def wrapper5_3(arg0, arg1, arg2, arg3, arg4, opt0 = Unobtainium, opt1 = Unobtainium, opt2 = Unobtainium):
			return wrapper(arg0, arg1, arg2, arg3, arg4, opt0, opt1, opt2)
		@wraps(func)
		def wrapper6_0(arg0, arg1, arg2, arg3, arg4, arg5):
			return wrapper(arg0, arg1, arg2, arg3, arg4, arg5)
		@wraps(func)
		def wrapper6_1(arg0, arg1, arg2, arg3, arg4, arg5, opt0 = Unobtainium):
			return wrapper(arg0, arg1, arg2, arg3, arg4, arg5, opt0)
		@wraps(func)
		def wrapper6_2(arg0, arg1, arg2, arg3, arg4, arg5, opt0 = Unobtainium, opt1 = Unobtainium):
			return wrapper(arg0, arg1, arg2, arg3, arg4, arg5, opt0, opt1)
		@wraps(func)
		def wrapper6_3(arg0, arg1, arg2, arg3, arg4, arg5, opt0 = Unobtainium, opt1 = Unobtainium, opt2 = Unobtainium):
			return wrapper(arg0, arg1, arg2, arg3, arg4, arg5, opt0, opt1, opt2)
		@wraps(func)
		def wrapper7_0(arg0, arg1, arg2, arg3, arg4, arg5, arg6):
			return wrapper(arg0, arg1, arg2, arg3, arg4, arg5, arg6)
		@wraps(func)
		def wrapper7_1(arg0, arg1, arg2, arg3, arg4, arg5, arg6, opt0 = Unobtainium):
			return wrapper(arg0, arg1, arg2, arg3, arg4, arg5, arg6, opt0)
		@wraps(func)
		def wrapper7_2(arg0, arg1, arg2, arg3, arg4, arg5, arg6, opt0 = Unobtainium, opt1 = Unobtainium):
			return wrapper(arg0, arg1, arg2, arg3, arg4, arg5, arg6, opt0, opt1)
		@wraps(func)
		def wrapper7_3(arg0, arg1, arg2, arg3, arg4, arg5, arg6, opt0 = Unobtainium, opt1 = Unobtainium, opt2 = Unobtainium):
			return wrapper(arg0, arg1, arg2, arg3, arg4, arg5, arg6, opt0, opt1, opt2)
		@wraps(func)
		def wrapper8_0(arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7):
			return wrapper(arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7)
		@wraps(func)
		def wrapper8_1(arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7, opt0 = Unobtainium):
			return wrapper(arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7, opt0)
		@wraps(func)
		def wrapper8_2(arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7, opt0 = Unobtainium, opt1 = Unobtainium):
			return wrapper(arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7, opt0, opt1)
		@wraps(func)
		def wrapper8_3(arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7, opt0 = Unobtainium, opt1 = Unobtainium, opt2 = Unobtainium):
			return wrapper(arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7, opt0, opt1, opt2)
		@wraps(func)
		def wrapper9_0(arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8):
			return wrapper(arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8)
		@wraps(func)
		def wrapper9_1(arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, opt0 = Unobtainium):
			return wrapper(arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, opt0)
		@wraps(func)
		def wrapper9_2(arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, opt0 = Unobtainium, opt1 = Unobtainium):
			return wrapper(arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, opt0, opt1)
		@wraps(func)
		def wrapper9_3(arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, opt0 = Unobtainium, opt1 = Unobtainium, opt2 = Unobtainium):
			return wrapper(arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, opt0, opt1, opt2)
		
		wrappers = (
			(wrapper0_0, wrapper0_1, wrapper0_2, wrapper0_3),
			(wrapper1_0, wrapper1_1, wrapper1_2, wrapper1_3),
			(wrapper2_0, wrapper2_1, wrapper2_2, wrapper2_3),
			(wrapper3_0, wrapper3_1, wrapper3_2, wrapper3_3),
			(wrapper4_0, wrapper4_1, wrapper4_2, wrapper4_3),
			(wrapper5_0, wrapper5_1, wrapper5_2, wrapper5_3),
			(wrapper6_0, wrapper6_1, wrapper6_2, wrapper6_3),
			(wrapper7_0, wrapper7_1, wrapper7_2, wrapper7_3),
			(wrapper8_0, wrapper8_1, wrapper8_2, wrapper8_3),
			(wrapper9_0, wrapper9_1, wrapper9_2, wrapper9_3),
		)
		
		return wrappers[required][optional]
	
	def traceEntry(self, format, *args):
		if self.tracing:
			self.indent(format, *args)
			self.depth += 1
	
	def traceException(self, format, exc, *args):
		if self.tracing:
			self.depth -= 1
			self.indent(' \'-raised %s', exc.__name__)
	
	def traceExit(self, format, result, *args):
		if self.tracing:
			self.depth -= 1
			self.indent(' \'-returned %r', result)
	
	def indent(self, format, *args):
		print (' | ' * self.depth) + (format % args)

_tracer = None
def tracer():
	global _tracer
	if not _tracer:
		_tracer = Tracer()
	return _tracer

def traced(func):
	return tracer().traced(func)

def log(format, *args):
	tracer().indent(format, *args)
