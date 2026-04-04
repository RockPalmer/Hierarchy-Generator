import tkinter as tk
import json
from typing import Callable,Any

class CLAUSE_:
	pass
class AND_(CLAUSE_):
	def __init__(self,*args):
		self.values = []
		for arg in args:
			if isinstance(arg,tuple):
				self.values.append(
					str(arg[0]) + '_eq_' + str(arg[1])
				)
			elif isinstance(arg,CLAUSE_):
				self.values.append(
					'(' + str(arg) + ')'
				)
	def __str__(self) -> str:
		str_vals = ['(' + str(value) + ')' if isinstance(value,CLAUSE_) else str(value) for value in self.values]
		return '&&'.join(self.values)
class OR_(CLAUSE_):
	def __init__(self,*args):
		self.values = []
		for arg in args:
			if isinstance(arg,tuple):
				self.values.append(
					str(arg[0]) + '_eq_' + str(arg[1])
				)
			elif isinstance(arg,CLAUSE_):
				self.values.append(
					'(' + str(arg) + ')'
				)
	def __str__(self) -> str:
		str_vals = ['(' + str(value) + ')' if isinstance(value,CLAUSE_) else str(value) for value in self.values]
		return '||'.join(self.values)
class NOT_(CLAUSE_):
	def __init__(self,*args,**kargs):
		if len(args) > 0:
			self.value = args[0]
		else:
			(key,value) = list(kargs.items())[0]
			self.value = str(key) + '_eq_' + str(value)
	def __str__(self) -> str:
		if isinstance(self.value,CLAUSE_):
			return '!(' + str(self.value) + ')'
		return '!' + str(self.value)
def TAG_(arg):
	if isinstance(arg,tuple):
		return str(arg[0]) + '_eq_' + str(arg[1])
	return str(arg)
def TAGS_(**args):
	vals = []
	for k,v in args.items():
		vals.append(str(k) + '_eq_' + str(v))
	return tuple(vals)
def VALUE_(value : str) -> str | bool | int | float:
	if value == 'True':
		return True
	if value == 'False':
		return False
	try:
		return int(value)
	except:
		try:
			return float(value)
		except:
			return value
def create_gridded_canvas(root,grid_size : int):
	canvas = tk.Canvas(
		root,
		width = root.winfo_screenwidth(),
		height = root.winfo_screenheight(),
		scrollregion = (
			0,
			0,
			root.winfo_screenwidth(),
			root.winfo_screenheight()
		),
		bg = "#c7c7c7"
	)
	canvas.pack()
	for x in range(0,root.winfo_screenwidth(),grid_size):
		canvas.create_line(
			x,
			0,
			x,
			root.winfo_screenheight(),
			fill = "#ddd"
		)
	for y in range(0,root.winfo_screenheight(),grid_size):
		canvas.create_line(
			0,
			y,
			root.winfo_screenwidth(),
			y,
			fill = "#ddd"
		)
	return canvas

hierarchies = {
	'hover' : [
		'element',
		'line',
		'head',
		'outline',
		'border',
		'divider',
		'text',
	],
	'left-click' : [
		'text',
		'element',
		'line',
		'head',
		'outline',
		'border',
		'divider',
	],
	'right-click' : [
		'text',
		'element',
		'line',
		'head',
		'outline',
		'border',
		'divider',
	],
}

class GridSpace:
	def __init__(self,root,grid_size : int) -> None:
		self.grid_size = 10
		self.element_id = 0
		self.root = root
		self.root.title("Grid Space")
		self.tooltip = tk.Menu(
			self.root,
			tearoff = 0,
		)
		self.tooltip.add_command(
			label = 'Add',
		)
		self.tooltip.add_command(
			label = 'Edit',
		)
		self.tooltip.add_command(
			label = 'Delete',
		)
		self.canvas = create_gridded_canvas(self.root,self.grid_size)
		self.attributes = {
			'entries' : {}
		}

		# left click event
		self.canvas.bind(
			'<Button-1>',
			self.left_click,
		)
		# double left click event
		self.canvas.bind(
			'<Double-Button-1>',
			self.double_left_click,
		)
		# move mouse
		self.canvas.bind(
			'<Motion>',
			self.mouse_move,
		)
		# right click event
		self.canvas.bind(
			'<Button-3>',
			self.right_click,
		)
		self.win_width = self.root.winfo_screenwidth() // self.grid_size
		self.win_height = self.root.winfo_screenheight() // self.grid_size
		self.type_width = self.win_width // 8
		self.type_height = self.win_height // 8
		self.attr_width = self.type_width
		self.attr_height = self.win_height // 16
		self.type_border_thickness = 10
		self.attribute_border_thickness = 5
		self.arrow_height = self.grid_size * 2
		self.arrow_base = self.grid_size
	def find(self,value):
		return self.canvas.find_withtag(TAG_(value))
	def event_hierarchy(self,event_type : str,*eids : tuple[int,...]):
		global hierarchies

		obj_types = {}
		for eid in eids:
			attrs = self.get_attributes(eid)
			if 'type' in attrs:
				obj_types[eid] = hierarchies[event_type].index(attrs['type'])
		if len(obj_types) == 0:
			return None
		max_val = max(obj_types.values())
		for eid,h in obj_types.items():
			if h == max_val:
				return eid
	def get_bounds(self,eid : int) -> tuple[int,int,int,int]:
		(x1,y1,x2,y2) = self.canvas.coords(eid)
		attributes = self.find(
			AND_(
				('type','element'),
				('container',eid)
			)
		)
		if len(attributes) > 0:
			last_attribute = self.find(
				AND_(
					('type','element'),
					('container',eid),
					('index',len(attributes) - 1)
				)
			)[0]
			(ax1,ay1,ax2,ay2) = self.canvas.coords(last_attribute)
			return (x1,y1,ax2,ay2)
		return (x1,y1,x2,y2)
	def handle_hover(self,x : int,y : int,top : bool,*eids : tuple[int,...]):
		match len(eids):
			case 1:
				eid = eids[0]
			case 0:
				eid = None
			case _:
				eid = self.event_hierarchy('hover',*eids)
		if 'link_state' in self.attributes:
			if 'link_start' not in self.attributes:
				# Handle cursor
				self.canvas.config(cursor = 'dot')
				if eid is None:
					return

				# Handle highlighting
				for border in self.find(AND_(
					OR_(
						('type','border'),
						('type','outline'),
					)
				)):
					attrs = self.get_attributes(border)
					if attrs.get('parent',None) == eid:
						self.canvas.itemconfigure(
							border,
							fill = attrs['fill'],
							outline = attrs['outline']
						)
					else:
						self.canvas.itemconfigure(
							border,
							fill = '',
							outline = ''
						)
			elif 'link_end' not in self.attributes:
				# Handle cursor
				(x1,y1,x2,y2) = self.canvas.coords(self.attributes['link_start'])
				if eid is None:
					self.canvas.coords(
						self.attributes['link_line'],
						(x1 + x2) / 2,
						(y1 + y2) / 2,
						x,
						y,
					)
					return
				(xa1,ya1,xa2,ya2) = self.canvas.coords(eid)
				self.canvas.coords(
					self.attributes['link_line'],
					(x1 + x2) / 2,
					(y1 + y2) / 2,
					(xa1 + xa2) / 2,
					(ya1 + ya2) / 2,
				)

				# Handle highlighting
				for border in self.find(AND_(
					OR_(
						('type','border'),
						('type','outline'),
					)
				)):
					attrs = self.get_attributes(border)
					if attrs.get('parent',None) == eid:
						self.canvas.itemconfigure(
							border,
							fill = attrs['fill'],
							outline = attrs['outline']
						)
					else:
						self.canvas.itemconfigure(
							border,
							fill = '',
							outline = ''
						)
		elif 'connected_start' in self.attributes:
			# Handling connection

			for border in self.find(AND_(
				('type','border'),
				('parent',self.attributes['connected_start'])
			)):
				attrs = self.get_attributes(border)
				self.canvas.itemconfigure(
					border,
					fill = attrs['fill'],
					outline = attrs['outline'],
				)
			# Handle cursor
			self.canvas.config(cursor = 'dot')
			# Get grid coordinates of cursor
			(gx,gy) = self.get_grid_coords(x,y)
			# Get attributes of connected element
			attributes = self.get_attributes(self.attributes['connected_start'])
			# Get type of connected element
			type_val = self.get_type(attributes,2)
			if ('element','type') != type_val:
				raise TypeError('Invalid type: ' + str(type_val))
			# Get grid coordinates of connected element
			(x1,y1,x2,y2) = self.get_grid_coords(
				*self.get_bounds(
					self.attributes['connected_start']
				)
			)

			# Get true coordinates of connected element and cursor
			(x1,y1,x2,y2,gx,gy) = self.get_true_coords(x1,y1,x2,y2,gx,gy)
			match self.attributes['connected_state']:
				case 1: # Start connection
					if gy > y1 and gy <= y2:
						if gx < x1:
							if 'temp_line' not in self.attributes:
								self.attributes['temp_line'] = self.canvas.create_line(
									x1,
									gy - self.grid_size / 2,
									gx,
									gy - self.grid_size / 2,
									dash = (3,3),
									tags = TAGS_(
										type = 'line',
										sub_type = 'west',
										start = self.attributes['connected_start'],
									)
								)
							else:
								self.canvas.coords(
									self.attributes['temp_line'],
									x1,
									gy - self.grid_size / 2,
									gx,
									gy - self.grid_size / 2,
								)
						elif gx > x2:
							if 'temp_line' not in self.attributes:
								self.attributes['temp_line'] = self.canvas.create_line(
									x2,
									gy - self.grid_size / 2,
									gx,
									gy - self.grid_size / 2,
									dash = (3,3),
									tags = TAGS_(
										type = 'line',
										sub_type = 'east',
										start = self.attributes['connected_start'],
									)
								)
							else:
								self.canvas.coords(
									self.attributes['temp_line'],
									x2,
									gy - self.grid_size / 2,
									gx,
									gy - self.grid_size / 2,
								)
						elif 'temp_line' in self.attributes:
							self.canvas.delete(self.attributes['temp_line'])
							del self.attributes['temp_line']
					elif gx > x1 and gx <= x2:
						if gy < y1:
							if 'temp_line' not in self.attributes:
								self.attributes['temp_line'] = self.canvas.create_line(
									gx - self.grid_size / 2,
									y1,
									gx - self.grid_size / 2,
									gy,
									dash = (3,3),
									tags = TAGS_(
										type = 'line',
										sub_type = 'north',
										start = self.attributes['connected_start'],
									)
								)
							else:
								self.canvas.coords(
									self.attributes['temp_line'],
									gx - self.grid_size / 2,
									y1,
									gx - self.grid_size / 2,
									gy,
								)
						elif gy > y2:
							if 'temp_line' not in self.attributes:
								self.attributes['temp_line'] = self.canvas.create_line(
									gx - self.grid_size / 2,
									y2,
									gx - self.grid_size / 2,
									gy,
									dash = (3,3),
									tags = TAGS_(
										type = 'line',
										sub_type = 'south',
										start = self.attributes['connected_start'],
									)
								)
							else:
								self.canvas.coords(
									self.attributes['temp_line'],
									gx - self.grid_size / 2,
									y2,
									gx - self.grid_size / 2,
									gy,
								)
						elif 'temp_line' in self.attributes:
							self.canvas.delete(self.attributes['temp_line'])
							del self.attributes['temp_line']
					elif gy <= y1 and gx <= x1:
						if 'temp_line' not in self.attributes:
							self.attributes['temp_line'] = self.canvas.create_line(
								x1,
								y1,
								gx,
								gy,
								dash = (3,3),
								tags = TAGS_(
									type = 'line',
									sub_type = 'west',
									start = self.attributes['connected_start'],
								)
							)
						else:
							self.canvas.coords(
								self.attributes['temp_line'],
								x1,
								y1,
								gx,
								gy,
							)
					elif gy <= y1 and gx > x2:
						if 'temp_line' not in self.attributes:
							self.attributes['temp_line'] = self.canvas.create_line(
								x2,
								y1,
								gx,
								gy,
								dash = (3,3),
								tags = TAGS_(
									type = 'line',
									sub_type = 'west',
									start = self.attributes['connected_start'],
								)
							)
						else:
							self.canvas.coords(
								self.attributes['temp_line'],
								x2,
								y1,
								gx,
								gy,
							)
					elif gy > y2 and gx <= x1:
						if 'temp_line' not in self.attributes:
							self.attributes['temp_line'] = self.canvas.create_line(
								x1,
								y2,
								gx,
								gy,
								dash = (3,3),
								tags = TAGS_(
									type = 'line',
									sub_type = 'west',
									start = self.attributes['connected_start'],
								)
							)
						else:
							self.canvas.coords(
								self.attributes['temp_line'],
								x1,
								y2,
								gx,
								gy,
							)
					elif gy > y2 and gx > x2:
						if 'temp_line' not in self.attributes:
							self.attributes['temp_line'] = self.canvas.create_line(
								x2,
								y2,
								gx,
								gy,
								dash = (3,3),
								tags = TAGS_(
									type = 'line',
									sub_type = 'west',
									start = self.attributes['connected_start'],
								)
							)
						else:
							self.canvas.coords(
								self.attributes['temp_line'],
								x2,
								y2,
								gx,
								gy,
							)
					elif 'temp_line' in self.attributes:
						self.canvas.delete(self.attributes['temp_line'])
						del self.attributes['temp_line']
				case 2:
					(x1,y1,x2,y2) = self.canvas.coords(self.attributes['temp_line'])
					self.canvas.coords(
						self.attributes['temp_line'],
						x1,
						y1,
						x,
						y,
					)
		else:
			# Not handling connection
			if eid is None:
				self.canvas.config(cursor = 'left_ptr')
				return
			attrs = self.get_attributes(eid)
			selected = self.find(('selected',True))
			if top and len(selected) > 0:
				# There is an item that is selected
				val = selected[0]
				# Cursor starting position
				(cx1,cy1) = self.attributes['selected_element_cursor_source']
				# Cursor current position
				(cx2,cy2) = (x,y)
				# Cursor movement vector
				vector = self.get_grid_coords(cx2 - cx1,cy2 - cy1)
				# Attributes of selected value
				attrs = self.get_attributes(val)
				# Type of selected value
				type_val = self.get_type(attrs,3)
				hold = set()
				match type_val:
					case ('divider',):
						hold.add(val)

						(top_coords,bottom_coords) = self.attributes['selected_element_source_coords']
						(tx1,ty1,tx2,ty2) = top_coords
						(bx1,by1,bx2,by2) = bottom_coords
						top_attrs = self.get_attributes(attrs['top'])
						self.place_attribute(
							attrs['bottom'],
							bx1,
							by1 + vector[1],
							by2 - by1 - vector[1],
						)
						match top_attrs.get('sub_type',None):
							case 'type':
								self.place_type(
									attrs['top'],
									tx1,
									ty1,
									tx2,
									ty2 + vector[1],
								)
							case 'attribute':
								self.place_attribute(
									attrs['top'],
									tx1,
									ty1,
									ty2 - ty1 + vector[1]
								)
							case _:
								raise TypeError('Invalid sub_type: ' + str(top_attrs.get('sub_type',None)))
					case ('element','type'):
						hold |= set(
							self.find(('parent',val))
						)
						(x1,y1,x2,y2) = self.attributes['selected_element_source_coords']
						self.place_type(
							val,
							x1 + vector[0],
							y1 + vector[1],
							x2 + vector[0],
							y2 + vector[1],
						)
					case ('border','edge','top'):
						hold |= set(
							self.find(('parent',attrs['parent']))
						)
						(x1,y1,x2,y2) = self.attributes['selected_element_source_coords']
						self.place_type(
							attrs['parent'],
							x1,
							y1 + vector[1],
							x2,
							y2,
						)
					case ('border','edge','bottom'):
						hold |= set(
							self.find(('parent',attrs['parent']))
						)
						(x1,y1,x2,y2) = self.attributes['selected_element_source_coords']
						self.place_type(
							attrs['parent'],
							x1,
							y1,
							x2,
							y2 + vector[1],
						)
					case ('border','edge','left'):
						hold |= set(
							self.find(('parent',attrs['parent']))
						)
						(x1,y1,x2,y2) = self.attributes['selected_element_source_coords']
						self.place_type(
							attrs['parent'],
							x1 + vector[0],
							y1,
							x2,
							y2,
						)
					case ('border','edge','right'):
						hold |= set(
							self.find(('parent',attrs['parent']))
						)
						(x1,y1,x2,y2) = self.attributes['selected_element_source_coords']
						self.place_type(
							attrs['parent'],
							x1,
							y1,
							x2 + vector[0],
							y2,
						)
					case ('border','corner','top_left'):
						hold |= set(
							self.find(('parent',attrs['parent']))
						)
						(x1,y1,x2,y2) = self.attributes['selected_element_source_coords']
						self.place_type(
							attrs['parent'],
							x1 + vector[0],
							y1 + vector[1],
							x2,
							y2,
						)
					case ('border','corner','top_right'):
						hold |= set(
							self.find(('parent',attrs['parent']))
						)
						(x1,y1,x2,y2) = self.attributes['selected_element_source_coords']
						self.place_type(
							attrs['parent'],
							x1,
							y1 + vector[1],
							x2 + vector[0],
							y2,
						)
					case ('border','corner','bottom_left'):
						hold |= set(
							self.find(('parent',attrs['parent']))
						)
						(x1,y1,x2,y2) = self.attributes['selected_element_source_coords']
						self.place_type(
							attrs['parent'],
							x1 + vector[0],
							y1,
							x2,
							y2 + vector[1],
						)
					case ('border','corner','bottom_right'):
						hold |= set(
							self.find(('parent',attrs['parent']))
						)
						(x1,y1,x2,y2) = self.attributes['selected_element_source_coords']
						self.place_type(
							attrs['parent'],
							x1,
							y1,
							x2 + vector[0],
							y2 + vector[1],
						)
				hidden = set(
					self.find(
						OR_(
							('type','border'),
							('type','outline'),
							('type','divider')
						)
					)
				) - hold
				for border in hidden:
					self.canvas.itemconfigure(
						border,
						fill = '',
						outline = ''
					)
			elif 'type' in attrs:
				# There is not an element that is selected
				for border in self.find(OR_(
					('type','border'),
					('type','outline'),
					('type','divider')
				)):
					self.canvas.itemconfigure(
						border,
						fill = '',
						outline = ''
					)
				# Set cursor
				if top:
					match self.get_type(attrs):
						case ('text',):
							self.canvas.config(cursor = 'xterm')
						case ('border','edge','left'):
							self.canvas.config(cursor = 'left_side')
						case ('border','edge','right'):
							self.canvas.config(cursor = 'right_side')
						case ('border','edge','top'):
							self.canvas.config(cursor = 'top_side')
						case ('border','edge','bottom'):
							self.canvas.config(cursor = 'bottom_side')
						case ('border','corner','top_left'):
							self.canvas.config(cursor = 'top_left_corner')
						case ('border','corner','top_right'):
							self.canvas.config(cursor = 'top_right_corner')
						case ('border','corner','bottom_left'):
							self.canvas.config(cursor = 'bottom_left_corner')
						case ('border','corner','bottom_right'):
							self.canvas.config(cursor = 'bottom_right_corner')
						case ('element','type') | ('element','attribute'):
							self.canvas.config(cursor = 'fleur')
						case ('divider',):
							self.canvas.config(cursor = 'double_arrow')
				# Set other behavior for eid
				match attrs.get('type',None):
					case 'text' | 'border':
						# Implies to hovering over parent element
						self.handle_hover(x,y,False,attrs['parent'])
					case 'outline':
						# Equivalent to hovering over parent element
						self.handle_hover(x,y,top,attrs['parent'])
					case 'element':
						for border in self.find(
							AND_(
								OR_(
									('type','border'),
									('type','outline')
								),
								('parent',eid)
							)
						):
							attrs = self.get_attributes(border)
							self.canvas.itemconfigure(
								border,
								outline = attrs['outline'],
								fill = attrs['fill']
							)
					case 'divider':
						self.canvas.itemconfigure(
							eid,
							outline = attrs['outline'],
							fill = attrs['fill'],
						)
					case _:
						raise TypeError('Invalid type: ' + str(attrs.get('type',None)))
			else:
				for border in self.find(OR_(
					('type','border'),
					('type','outline'),
					('type','divider')
				)):
					self.canvas.itemconfigure(
						border,
						fill = '',
						outline = ''
					)
	def handle_left_click(self,x : int,y : int,top : bool,*eids : tuple[int,...]):
		self.finish_entries()
		if 'link_state' in self.attributes:
			match len(eids):
				case 1:
					eid = eids[0]
				case 0:
					eid = None
				case _:
					eid = self.event_hierarchy('left-click',*eids)
			if eid is None:
				del self.attributes['link_state']
				if 'link_start' in self.attributes:
					del self.attributes['link_start']
				if 'link_end' in self.attributes:
					del self.attributes['link_end']
			else:
				if 'link_start' not in self.attributes:
					self.attributes['link_start'] = eid
					(x1,y1,x2,y2) = self.canvas.coords(eid)
					self.attributes['link_line'] = self.canvas.create_line(
						(x1 + x2) / 2,
						(y1 + y2) / 2,
						x,
						y,
						dash = (3,3),

						tags = TAGS_(
							type = 'line',
							start = eid,
						)
					)
				elif 'link_end' not in self.attributes:
					self.attributes['link_end'] = eid
				else:
					del self.attributes['link_state']
					del self.attributes['link_start']
					del self.attributes['link_end']
		elif 'connected_start' in self.attributes:
			match self.attributes['connected_state']:
				case 1:
					if 'temp_line' in self.attributes:
						self.attributes['connected_state'] = 2
					else:
						del self.attributes['connected_state']
				case 2:
					del self.attributes['connected_state']
		else:
			if len(
				self.find(
					('selected',True)
				)
			) > 0:
				self.canvas.dtag(
					TAG_(('selected',True)),
					TAG_(('selected',True))
				)
				return
			match len(eids):
				case 1:
					eid = eids[0]
				case 0:
					eid = None
				case _:
					eid = self.event_hierarchy('left-click',*eids)
			if eid is None:
				return
			attrs = self.get_attributes(eid)
			if 'type' not in attrs:
				return
			self.canvas.addtag_withtag(
				TAG_(('selected',True)),
				eid
			)
			self.attributes['selected_element_cursor_source'] = (x,y)
			attrs = self.get_attributes(eid)
			if 'parent' in attrs:
				self.attributes['selected_element_source_coords'] = self.get_grid_coords(
					*self.canvas.coords(attrs['parent'])
				)
			elif 'top' in attrs and 'bottom' in attrs:
				self.attributes['selected_element_source_coords'] = (
					self.get_grid_coords(
						*self.canvas.coords(attrs['top'])
					),
					self.get_grid_coords(
						*self.canvas.coords(attrs['bottom'])
					)
				)
			else:
				self.attributes['selected_element_source_coords'] = self.get_grid_coords(
					*self.canvas.coords(eid)
			)
	def handle_right_click(self,x : int,y : int,top : bool,*eids : tuple[int,...]):
		self.finish_entries()
		if 'link_state' in self.attributes:
			del self.attributes['link_state']
			if 'link_start' in self.attributes:
				del self.attributes['link_start']
			if 'link_end' in self.attributes:
				del self.attributes['link_end']
		elif 'connected_start' in self.attributes:
			del self.attributes['connected_start']
			if 'temp_line' in self.attributes:
				self.canvas.delete(self.attributes['temp_line'])
				del self.attributes['temp_line']
		else:
			self.attributes['tooltip_coords'] = self.get_grid_coords(x,y)
			match len(eids):
				case 1:
					eid = eids[0]
				case 0:
					eid = None
				case _:
					eid = self.event_hierarchy('right-click',*eids)
			if eid is None:
				self.tooltip.delete(0)
				add_tooltip = tk.Menu(
					self.tooltip,
					tearoff = 0,
				)
				if 'tooltip_element' in self.attributes:
					del self.attributes['tooltip_element']
				add_tooltip.add_command(
					label = 'Type',
					command = self.tooltip_create_type
				)
				add_tooltip.add_command(
					label = 'Link',
					command = self.tooltip_add_link
				)
				self.tooltip.insert_cascade(
					0,
					label = 'Add',
					state = 'normal',
					menu = add_tooltip
				)
				self.tooltip.entryconfigure(
					'Edit',
					state = 'disabled',
				)
				self.tooltip.entryconfigure(
					'Delete',
					state = 'disabled',
				)
			else:
				self.attributes['tooltip_element'] = eid
				attrs = self.get_attributes(eid)
				add_tooltip = tk.Menu(
					self.tooltip,
					tearoff = 0,
				)
				type_val = self.get_type(attrs,2)
				match type_val:
					case ('element','type'):
						add_tooltip.add_command(
							label = 'Attribute',
							command = self.tooltip_add_attribute,
						)
						add_tooltip.add_command(
							label = 'Connection',
							command = self.tooltip_add_connection,
						)
					case ('border','edge') | ('border','corner'):
						self.handle_right_click(
							x,
							y,
							False,
							attrs['parent']
						)
						return
					case ():
						raise TypeError('Invalid type: ' + str(attrs))
					case _:
						raise TypeError('Invalid type: ' + str(type_val))
				self.tooltip.delete(0)
				self.tooltip.insert_cascade(
					0,
					label = 'Add',
					state = 'normal',
					menu = add_tooltip
				)
				self.tooltip.entryconfigure(
					'Edit',
					state = 'normal',
				)
				self.tooltip.entryconfigure(
					'Delete',
					state = 'normal',
				)
	def finish_entries(self):
		entries = list(self.attributes['entries'].values())
		for entry in entries:
			self.finish_entry(entry)
	def get_type(self,attrs,start = None,end = None) -> tuple[str,...]:
		if isinstance(attrs,int):
			return self.get_type(
				self.get_attributes(attrs),start,end
			)
		if end is None:
			if start is None:
				start = 0
				end = float('inf')
			else:
				end = start
				start = 0
		vals = []
		i = 0
		while ('sub_'*i + 'type') in attrs:
			vals.append(attrs['sub_'*i + 'type'])
			i += 1
		if end == float('inf'):
			return tuple(vals[start:])
		return tuple(vals[start:end])
	def get_attributes(self,eid : int) -> dict:
		attrs = {}
		for tag in self.canvas.gettags(eid):
			if '_eq_' not in tag:
				continue
			index = tag.index('_eq_')
			attrs[tag[:index]] = VALUE_(tag[index + 4:])
		return attrs
	def get_children(self,eid : int) -> set[int]:
		return self.find(('parent',eid))
	def get_true_points(self,eid : int) -> set[tuple[int,int]]:
		(x1,y1,x2,y2) = self.canvas.coords(eid)
		return {
			(x1,y1),
			(x1,y2),
			(x2,y1),
			(x2,y2),
		}
	def create_type(self,x : int,y : int,**attributes) -> int:
		(x1,y1,x2,y2) = (x,y,x + self.type_width,y + self.type_height)
		if self.type_width > 1:
			x1 -= self.type_width // 2
			x2 -= self.type_width // 2
		if self.type_height > 1:
			y1 -= self.type_height // 2
			y2 -= self.type_height // 2
		(x1,y1) = self.get_true_coords(x1,y1)
		(x2,y2) = self.get_true_coords(x2,y2)
		eid = self.canvas.create_rectangle(
			x1,
			y1,
			x2,
			y2,
			tags = TAGS_(
				type = 'element',
				sub_type = 'type',
			),
			fill = 'white',
			outline = 'black',
		)
		self.canvas.create_text(
			(x1 + x2) / 2,
			(y1 + y2) / 2,
			text = '<Type>',
			tags = TAGS_(
				type = 'text',
				parent = eid
			),
		)
		# TOP LEFT
		self.canvas.create_rectangle(
			x1,
			y1,
			x1 + self.type_border_thickness,
			y1 + self.type_border_thickness,
			fill = '',
			outline = '',
			tags = TAGS_(
				type = 'border',
				sub_type = 'corner',
				sub_sub_type = 'top_left',
				fill = 'white',
				outline = 'black',
				parent = eid
			),
		)
		# BOTTOM LEFT
		self.canvas.create_rectangle(
			x1,
			y2 - self.type_border_thickness,
			x1 + self.type_border_thickness,
			y2,
			fill = '',
			outline = '',
			tags = TAGS_(
				type = 'border',
				sub_type = 'corner',
				sub_sub_type = 'bottom_left',
				fill = 'white',
				outline = 'black',
				parent = eid
			),
		)
		# TOP RIGHT
		self.canvas.create_rectangle(
			x2 - self.type_border_thickness,
			y1,
			x2,
			y1 + self.type_border_thickness,
			fill = '',
			outline = '',
			tags = TAGS_(
				type = 'border',
				sub_type = 'corner',
				sub_sub_type = 'top_right',
				fill = 'white',
				outline = 'black',
				parent = eid
			),
		)
		# BOTTOM RIGHT
		self.canvas.create_rectangle(
			x2 - self.type_border_thickness,
			y2 - self.type_border_thickness,
			x2,
			y2,
			fill = '',
			outline = '',
			tags = TAGS_(
				type = 'border',
				sub_type = 'corner',
				sub_sub_type = 'bottom_right',
				fill = 'white',
				outline = 'black',
				parent = eid
			),
		)
		# LEFT
		self.canvas.create_rectangle(
			x1,
			y1 + self.type_border_thickness,
			x1 + self.type_border_thickness,
			y2 - self.type_border_thickness,
			fill = '',
			outline = '',
			tags = TAGS_(
				type = 'border',
				sub_type = 'edge',
				sub_sub_type = 'left',
				fill = 'yellow',
				outline = 'black',
				parent = eid
			),
		)
		# RIGHT
		self.canvas.create_rectangle(
			x2 - self.type_border_thickness,
			y1 + self.type_border_thickness,
			x2,
			y2 - self.type_border_thickness,
			fill = '',
			outline = '',
			tags = TAGS_(
				type = 'border',
				sub_type = 'edge',
				sub_sub_type = 'right',
				fill = 'yellow',
				outline = 'black',
				parent = eid
			),
		)
		# TOP
		self.canvas.create_rectangle(
			x1 + self.type_border_thickness,
			y1,
			x2 - self.type_border_thickness,
			y1 + self.type_border_thickness,
			fill = '',
			outline = '',
			tags = TAGS_(
				type = 'border',
				sub_type = 'edge',
				sub_sub_type = 'top',
				fill = 'yellow',
				outline = 'black',
				parent = eid
			),
		)
		# BOTTOM
		self.canvas.create_rectangle(
			x1 + self.type_border_thickness,
			y2 - self.type_border_thickness,
			x2 - self.type_border_thickness,
			y2,
			fill = '',
			outline = '',
			tags = TAGS_(
				type = 'border',
				sub_type = 'edge',
				sub_sub_type = 'bottom',
				fill = 'yellow',
				outline = 'black',
				parent = eid
			),
		)
		return eid
	def create_attribute(self,container : int,x : int,y : int,**attributes) -> int:
		(x1,_,x2,_) = self.get_grid_coords(
			*self.canvas.coords(container)
		)
		(x1,y1,x2,y2) = (x,y,x + x2 - x1,y + self.attr_height)
		(x1,y1) = self.get_true_coords(x1,y1)
		(x2,y2) = self.get_true_coords(x2,y2)
		index = len(
			self.find(
				AND_(
					('container',container),
					('type','element'),
					('type','attribute'),
				)
			)
		)
		eid = self.canvas.create_rectangle(
			x1,
			y1,
			x2,
			y2,
			tags = TAGS_(
				type = 'element',
				sub_type = 'attribute',
				container = container,
				index = index,
			),
			fill = 'white',
			outline = 'black',
		)
		self.canvas.create_text(
			(x1 + x2) / 2,
			(y1 + y2) / 2,
			text = '<Attribute>',
			tags = TAGS_(
				type = 'text',
				parent = eid
			),
		)
		self.canvas.create_rectangle(
			x1,
			y1,
			x2,
			y1 + self.type_border_thickness,
			fill = '',
			outline = '',
			tags = TAGS_(
				type = 'divider',
				top = container,
				fill = 'blue',
				outline = 'black',
				bottom = eid
			),
		)
		self.canvas.create_rectangle(
			x1,
			y1,
			x1 + self.attribute_border_thickness,
			y2,
			fill = '',
			outline = '',
			tags = TAGS_(
				type = 'outline',
				sub_type = 'left',
				fill = 'black',
				outline = 'black',
				parent = eid
			),
		)
		self.canvas.create_rectangle(
			x2 - self.attribute_border_thickness,
			y1,
			x2,
			y2,
			fill = '',
			outline = '',
			tags = TAGS_(
				type = 'outline',
				sub_type = 'right',
				fill = 'black',
				outline = 'black',
				parent = eid
			),
		)
		self.canvas.create_rectangle(
			x1,
			y1,
			x2,
			y1 + self.attribute_border_thickness,
			fill = '',
			outline = '',
			tags = TAGS_(
				type = 'outline',
				sub_type = 'top',
				fill = 'black',
				outline = 'black',
				parent = eid
			),
		)
		self.canvas.create_rectangle(
			x1,
			y2 - self.attribute_border_thickness,
			x2,
			y2,
			fill = '',
			outline = '',
			tags = TAGS_(
				type = 'outline',
				sub_type = 'bottom',
				fill = 'black',
				outline = 'black',
				parent = eid
			),
		)
		# Adjust container borders
		(x1,y1,x2,y2) = self.canvas.coords(container)
		height = y2 - y1
		for element in self.find(('container',container)):
			(xa,ya,xb,yb) = self.canvas.coords(element)
			height += yb - ya
		left_border = list(
			self.find(AND_(
				('type','border'),
				('sub_type','edge'),
				('sub_sub_type','left'),
				('parent',container),
			))
		)[0]
		right_border = list(
			self.find(AND_(
				('type','border'),
				('sub_type','edge'),
				('sub_sub_type','right'),
				('parent',container),
			))
		)[0]
		bottom_border = list(
			self.find(AND_(
				('type','border'),
				('sub_type','edge'),
				('sub_sub_type','bottom'),
				('parent',container),
			))
		)[0]
		bottom_left_corner = list(
			self.find(AND_(
				('type','border'),
				('sub_type','corner'),
				('sub_sub_type','bottom_left'),
				('parent',container),
			))
		)[0]
		bottom_right_corner = list(
			self.find(AND_(
				('type','border'),
				('sub_type','corner'),
				('sub_sub_type','bottom_right'),
				('parent',container),
			))
		)[0]
		(x1,y1,x2,y2) = (x1,y1,x2,y1 + height)
		# BOTTOM LEFT
		self.canvas.coords(
			bottom_left_corner,
			x1,
			y2 - self.type_border_thickness,
			x1 + self.type_border_thickness,
			y2,
		)
		# BOTTOM RIGHT
		self.canvas.coords(
			bottom_right_corner,
			x2 - self.type_border_thickness,
			y2 - self.type_border_thickness,
			x2,
			y2,
		)
		# LEFT
		self.canvas.coords(
			left_border,
			x1,
			y1 + self.type_border_thickness,
			x1 + self.type_border_thickness,
			y2 - self.type_border_thickness,
		)
		# RIGHT
		self.canvas.coords(
			right_border,
			x2 - self.type_border_thickness,
			y1 + self.type_border_thickness,
			x2,
			y2 - self.type_border_thickness,
		)
		# BOTTOM
		self.canvas.coords(
			bottom_border,
			x1 + self.type_border_thickness,
			y2 - self.type_border_thickness,
			x2 - self.type_border_thickness,
			y2,
		)
		self.canvas.tag_raise(bottom_left_corner)
		self.canvas.tag_raise(bottom_right_corner)
		self.canvas.tag_raise(left_border)
		self.canvas.tag_raise(right_border)
		self.canvas.tag_raise(bottom_border)
		return eid
	def tooltip_create_type(self):
		self.create_type(
			self.attributes['tooltip_coords'][0],
			self.attributes['tooltip_coords'][1],
		)
	def tooltip_add_attribute(self):
		(x1,y1,x2,y2) = self.get_grid_coords(
			*self.canvas.coords(
				self.attributes['tooltip_element']
			)
		)
		self.create_attribute(
			self.attributes['tooltip_element'],
			x1,
			y2,
		)
	def tooltip_add_connection(self):
		self.attributes['connected_start'] = self.attributes['tooltip_element']
		self.attributes['connected_state'] = 1
	def tooltip_add_link(self):
		self.attributes['link_state'] = 0
	def get_grid_coords(self,*vals):
		return tuple(
			round(val / self.grid_size) for val in vals
		)
	def get_true_coords(self,*vals):
		return tuple(
			val * self.grid_size for val in vals
		)
	def place_type(self,eid : int,x1 : int, y1 : int,x2 : int,y2 : int):
		attrs = self.get_attributes(eid)
		(x1,y1,x2,y2) = self.get_true_coords(x1,y1,x2,y2)
		self.canvas.coords(
			eid,
			x1,
			y1,
			x2,
			y2
		)
		for text in self.find(
			AND_(
				('type','text'),
				('parent',eid)
			)
		):
			self.canvas.coords(
				text,
				(x1 + x2) / 2,
				(y1 + y2) / 2,
			)
		attributes = self.find(
			AND_(
				('type','element'),
				('container',eid)
			)
		)
		height = y2 - y1
		for i in range(len(attributes)):
			attribute = list(
				self.find(
					AND_(
						('type','element'),
						('sub_type','attribute'),
						('container',eid),
						('index',i)
					)
				)
			)[0]
			(xa,ya,xb,yb) = self.canvas.coords(attribute)
			(m,n,p,q) = self.get_grid_coords(
				x1,y1 + height,yb,ya
			)
			self.place_attribute(
				attribute,
				m,
				n,
				p - q
			)
			height += yb - ya
		y2 = y1 + height
		for element in self.find(('parent',eid)):
			attrs = self.get_attributes(element)
			type_val = self.get_type(attrs,3)
			match type_val:
				case ('border','corner','top_left'):
					self.canvas.coords(
						element,
						x1,
						y1,
						x1 + self.type_border_thickness,
						y1 + self.type_border_thickness,
					)
				case ('border','corner','top_right'):
					self.canvas.coords(
						element,
						x2 - self.type_border_thickness,
						y1,
						x2,
						y1 + self.type_border_thickness,
					)
				case ('border','corner','bottom_left'):
					self.canvas.coords(
						element,
						x1,
						y2 - self.type_border_thickness,
						x1 + self.type_border_thickness,
						y2,
					)
				case ('border','corner','bottom_right'):
					self.canvas.coords(
						element,
						x2 - self.type_border_thickness,
						y2 - self.type_border_thickness,
						x2,
						y2,
					)
				case ('border','edge','left'):
					self.canvas.coords(
						element,
						x1,
						y1 + self.type_border_thickness,
						x1 + self.type_border_thickness,
						y2 - self.type_border_thickness,
					)
				case ('border','edge','right'):
					self.canvas.coords(
						element,
						x2 - self.type_border_thickness,
						y1 + self.type_border_thickness,
						x2,
						y2 - self.type_border_thickness,
					)
				case ('border','edge','top'):
					self.canvas.coords(
						element,
						x1 + self.type_border_thickness,
						y1,
						x2 - self.type_border_thickness,
						y1 + self.type_border_thickness,
					)
				case ('border','edge','bottom'):
					self.canvas.coords(
						element,
						x1 + self.type_border_thickness,
						y2 - self.type_border_thickness,
						x2 - self.type_border_thickness,
						y2,
					)
				case ('text',):
					pass
				case _:
					raise TypeError('Invalid type: ' + str(type_val))
	def place_attribute(self,eid : int,x1 : int,y1 : int,height : int):
		attrs = self.get_attributes(eid)
		container = attrs['container']
		(xa,_,xb,yb) = self.get_grid_coords(
			*self.canvas.coords(container)
		)
		width = xb - xa
		x2 = x1 + width
		y2 = y1 + height
		(xa,ya,xb,yb) = self.get_grid_coords(
			*self.canvas.coords(eid)
		)
		(x1,y1,x2,y2) = self.get_true_coords(x1,y1,x2,y2)
		self.canvas.coords(
			eid,
			x1,
			y1,
			x2,
			y2
		)
		for element in self.find(
			OR_(
				AND_(
					OR_(
						('type','outline'),
						('type','text')
					),
					('parent',eid)
				),
				AND_(
					('type','divider'),
					('bottom',eid)
				),
			)
		):
			attrs = self.get_attributes(element)
			type_val = self.get_type(attrs,2)
			match type_val:
				case ('outline','left'):
					self.canvas.coords(
						element,
						x1,
						y1,
						x1 + self.attribute_border_thickness,
						y2,
					)
				case ('outline','right'):
					self.canvas.coords(
						element,
						x2 - self.attribute_border_thickness,
						y1,
						x2,
						y2,
					)
				case ('outline','top'):
					self.canvas.coords(
						element,
						x1,
						y1,
						x2,
						y1 + self.attribute_border_thickness,
					)
				case ('outline','bottom'):
					self.canvas.coords(
						element,
						x1,
						y2 - self.attribute_border_thickness,
						x2,
						y2,
					)
				case ('text',):
					self.canvas.coords(
						element,
						(x1 + x2) / 2,
						(y1 + y2) / 2,
					)
				case ('divider',):
					self.canvas.coords(
						element,
						x1,
						y1,
						x2,
						y1 + self.attribute_border_thickness,
					)
				case _:
					raise TypeError('Invalid type: ' + str(type_val))
	def right_click(self,event):
		overlapping = set(
			self.canvas.find_overlapping(
				event.x,
				event.y,
				event.x,
				event.y
			)
		) & set(
			self.canvas.find((''))
		)
		self.handle_right_click(
			event.x,
			event.y,
			True,
			*self.canvas.find_overlapping(
				event.x,
				event.y,
				event.x,
				event.y
			)
		)
		self.tooltip.tk_popup(
			event.x_root - 10,
			event.y_root - 10
		)
		self.tooltip.focus_set()
	def left_click(self,event):
		self.handle_left_click(
			event.x,
			event.y,
			True,
			*self.canvas.find_overlapping(
				event.x,
				event.y,
				event.x,
				event.y
			)
		)
	def double_left_click(self,event):
		entries = list(self.attributes['entries'].values())
		for entry in entries:
			self.finish_entry(entry)
		elements = set(
			self.canvas.find_overlapping(
				event.x,
				event.y,
				event.x,
				event.y,
			)
		)
		eid = None
		for element in elements:
			attrs = self.get_attributes(element)
			if 'type' in attrs and attrs['type'] == 'text':
				eid = element
				break
		if eid is not None:
			parent = attrs['parent']
			text = self.canvas.itemcget(eid,'text')
			xlen = None
			(x1,y1,x2,y2) = self.canvas.coords(parent)
			xlen = x2 - x1
			coords = self.canvas.coords(eid)
			self.canvas.delete(eid)
			entry_box = tk.Entry(
				self.root,
				text = text,
				width = round(xlen // 3),
			)
			canvas_window = self.canvas.create_window(
				coords[0],
				coords[1],
				window = entry_box,
				tags = TAGS_(
					type = 'entry',
					parent = parent
				),
				width = round(xlen // 3),
			)
			entry_box.insert(0,text)
			entry_box.bind(
				'<Return>',
				self.finish_entry,
			)
			self.attributes['entries'][canvas_window] = entry_box
	def mouse_move(self,event):
		self.handle_hover(
			event.x,
			event.y,
			True,
			*self.canvas.find_overlapping(
				event.x,
				event.y,
				event.x,
				event.y
			)
		)
	def finish_entry(self,event):
		wid = None
		if isinstance(event,tk.Event):
			widget = event.widget
		else:
			widget = event
		for window,entry in self.attributes['entries'].items():
			if str(entry) == str(widget):
				wid = window
				break
		if wid is None:
			raise TypeError('No window found for entry')
		text = widget.get()
		coords = self.canvas.coords(wid)
		attrs = self.get_attributes(wid)
		parent = attrs['parent']
		(x1,x2,y1,y2) = self.canvas.coords(parent)
		xlen = x2 - x1
		widget.destroy()
		self.canvas.delete(wid)
		self.canvas.create_text(
			coords[0],
			coords[1],
			text = text,
			tags = TAGS_(
				type = 'text',
				parent = parent
			),
		)