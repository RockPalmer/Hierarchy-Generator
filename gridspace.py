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
		if isinstance(v,set):
			for u in v:
				vals.append(str(k) + '_eq_' + str(u))
		else:
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
		'outline',
		'border',
		'divider',
		'text',
	],
	'left-click' : [
		'text',
		'element',
		'outline',
		'border',
		'divider',
	],
	'right-click' : [
		'text',
		'element',
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
		self.create_type(
			self.type_width * 3, # 40
			self.type_height * 3, # 40
		)
		self.create_type(
			self.type_width * 6, # 80
			self.type_height * 6, # 80
		)
	def find(self,value):
		return self.canvas.find_withtag(TAG_(value))
	def event_hierarchy(self,event_type : str,*eids : tuple[int,...]):
		global hierarchies

		obj_types = {}
		for eid in eids:
			attrs = self.get_attributes(eid)
			if 'type' in attrs:
				if not isinstance(attrs['type'],set):
					attrs['type'] = {attrs['type']}
				vals = [hierarchies[event_type].index(t) for t in attrs['type'] if t in hierarchies[event_type]]
				if len(vals) > 0:
					obj_types[eid] = max(vals)
		if len(obj_types) == 0:
			return None
		max_val = max(obj_types.values())
		for eid,h in obj_types.items():
			if h == max_val:
				return eid
	def handle_hover(self,x : int,y : int,top : bool,*eids : tuple[int,...]):
		match len(eids):
			case 1:
				eid = eids[0]
			case 0:
				eid = None
			case _:
				eid = self.event_hierarchy('hover',*eids)
		for border in self.find(OR_(
			('type','border'),
			('type','outline'),
			('type','divider')
		)):
			self.canvas.itemconfigure(
				border,
				fill = '',
				outline = '',
			)
		if eid is not None:
			attrs = self.get_attributes(eid)
			if 'type' in attrs:
				if 'text' in attrs['type']:
					if top:
						self.canvas.config(cursor = 'xterm')
					self.handle_hover(x,y,False,attrs['parent'])
				elif 'border' in attrs['type']:
					if top:
						if 'edge' in attrs['type']:
							if 'left' in attrs['type']:
								self.canvas.config(cursor = 'left_side')
							elif 'right' in attrs['type']:
								self.canvas.config(cursor = 'right_side')
							elif 'top' in attrs['type']:
								self.canvas.config(cursor = 'top_side')
							elif 'bottom' in attrs['type']:
								self.canvas.config(cursor = 'bottom_side')
							else:
								raise TypeError('Invalid type: ' + str(attrs['type']))
						elif 'corner' in attrs['type']:
							if attrs['top']:
								if attrs['left']:
									self.canvas.config(cursor = 'top_left_corner')
								else:
									self.canvas.config(cursor = 'top_right_corner')
							else:
								if attrs['left']:
									self.canvas.config(cursor = 'bottom_left_corner')
								else:
									self.canvas.config(cursor = 'bottom_right_corner')
						else:
							raise TypeError('Invalid border_type: ' + str(attrs['border_type']))
					self.handle_hover(x,y,False,attrs['parent'])
				elif 'outline' in attrs['type']:
					self.handle_hover(x,y,top,attrs['parent'])
				elif 'element' in attrs['type']:
					if top:
						self.canvas.config(cursor = 'fleur')
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
						if 'border' in attrs['type']:
							if 'edge' in attrs['type']:
								self.canvas.itemconfigure(
									border,
									outline = 'black',
									fill = 'yellow'
								)
							elif 'corner' in attrs['type']:
								self.canvas.itemconfigure(
									border,
									outline = 'black',
									fill = 'white'
								)
							else:
								raise TypeError('Invalid type: ' + str(attrs['type']))
						elif 'outline' in attrs['type']:
							self.canvas.itemconfigure(
								border,
								outline = 'black',
								fill = 'black'
							)
						else:
							raise TypeError('Ivalid type: ' + str(attrs['type']))
				elif 'divider' in attrs['type']:
					if top:
						self.canvas.config(cursor = 'double_arrow')
					self.canvas.itemconfigure(
						eid,
						outline = 'black',
						fill = 'yellow',
					)
				else:
					raise TypeError('Invalid type: ' + str(attrs['type']))
			if top:
				selected = self.find(('selected',True))
				if len(selected) == 0:
					return
				val = selected[0]
				(cx1,cy1) = self.attributes['selected_element_cursor_source']
				(cx2,cy2) = (x,y)
				grid_vector = self.get_grid_coords(cx2 - cx1,cy2 - cy1)
				attrs = self.get_attributes(val)
				(x1,y1,x2,y2) = self.attributes['selected_element_source_coords']
				if 'type' in attrs['type']:
					self.place_type(
						val,
						x1 + grid_vector[0],
						y1 + grid_vector[1],
						x2 + grid_vector[0],
						y2 + grid_vector[1],
					)
				elif 'border' in attrs['type']:
					if 'edge' in attrs['type']:
						if 'top' in attrs['type']:
							self.place_type(
								attrs['parent'],
								x1,
								y1 + grid_vector[1],
								x2,
								y2,
							)
						elif 'bottom' in attrs['type']:
							self.place_type(
								attrs['parent'],
								x1,
								y1,
								x2,
								y2 + grid_vector[1],
							)
						elif 'left' in attrs['type']:
							self.place_type(
								attrs['parent'],
								x1 + grid_vector[0],
								y1,
								x2,
								y2,
							)
						elif 'right' in attrs['type']:
							self.place_type(
								attrs['parent'],
								x1,
								y1,
								x2 + grid_vector[0],
								y2,
							)
						else:
							raise TypeError('Invalid type: ' + str(attrs['type']))
					elif 'corner' in attrs['type']:
						if attrs['top']:
							if attrs['left']:
								self.place_type(
									attrs['parent'],
									x1 + grid_vector[0],
									y1 + grid_vector[1],
									x2,
									y2,
								)
							else:
								self.place_type(
									attrs['parent'],
									x1,
									y1 + grid_vector[1],
									x2 + grid_vector[0],
									y2,
								)
						else:
							if attrs['left']:
								self.place_type(
									attrs['parent'],
									x1 + grid_vector[0],
									y1,
									x2,
									y2 + grid_vector[1],
								)
							else:
								self.place_type(
									attrs['parent'],
									x1,
									y1,
									x2 + grid_vector[0],
									y2 + grid_vector[1],
								)
					else:
						raise TypeError('Invalid type: ' + str(attrs['type']))
				elif 'divider' in attrs['type']:
					(top,bottom) = (attrs['top'],attrs['bottom'])
					self.place_attribute(
						bottom,
						x1,
						y1 + grid_vector[1],
						(y2 - y1) - grid_vector[1],
					)
					top_attrs = self.get_attributes(top)
					if 'type' in top_attrs['type']:
						self.place_type(
							val,
							x1,
							y1,
							x2,
							y2 + grid_vector[1],
						)
					elif 'attribute' in top_attrs['type']:
						self.place_attribute(
							top,
							x1,
							y1,
							grid_vector[1],
						)
					else:
						raise TypeError('Invalid type: ' + str(top_attrs['type']))
				else:
					raise TypeError('Invalid type: ' + str(attrs['type']))
		else:
			self.canvas.config(cursor = 'left_ptr')
	def handle_left_click(self,x : int,y : int,top : bool,*eids : tuple[int,...]):
		self.finish_entries()
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
		else:
			self.attributes['selected_element_source_coords'] = self.get_grid_coords(
				*self.canvas.coords(eid)
			)
	def handle_right_click(self,x : int,y : int,top : bool,*eids : tuple[int,...]):
		self.finish_entries()
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
			if 'element' in attrs['type']:
				if 'type' in attrs['type']:
					add_tooltip.add_command(
						label = 'Attribute',
						command = self.tooltip_add_attribute,
					)
					add_tooltip.add_command(
						label = 'Connection',
					)
				else:
					raise TypeError('Invalid type: ' + str(attrs['type']))
			elif 'border' in attrs['type']:
				self.handle_right_click(
					x,
					y,
					False,
					attrs['parent']
				)
				return
			else:
				raise TypeError('Invalid type: ' + str(attrs['type']))
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
	def get_attributes(self,eid : int) -> dict:
		attrs = {}
		for tag in self.canvas.gettags(eid):
			if '_eq_' not in tag:
				continue
			index = tag.index('_eq_')
			if tag[:index] in attrs:
				if isinstance(attrs[tag[:index]],set):
					attrs[tag[:index]].add(
						VALUE_(tag[index + 4:])
					)
				else:
					attrs[tag[:index]] = {
						attrs[tag[:index]],
						VALUE_(tag[index + 4:])
					}
			else:
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
				type = {
					'element',
					'type'
				}
			),
			fill = 'white',
			outline = 'black',
		)
		self.canvas.create_text(
			(x1 + x2) / 2,
			(y1 + y2) / 2,
			text = '<Type>',
			tags = TAGS_(
				type = {
					'text'
				},
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
				type = {
					'border',
					'corner',
				},
				top = True,
				left = True,
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
				type = {
					'border',
					'corner',
				},
				top = False,
				left = True,
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
				type = {
					'border',
					'corner',
				},
				top = True,
				left = False,
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
				type = {
					'border',
					'corner',
				},
				top = False,
				left = False,
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
				type = {
					'border',
					'edge',
					'left',
				},
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
				type = {
					'border',
					'edge',
					'right',
				},
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
				type = {
					'border',
					'edge',
					'top',
				},
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
				type = {
					'border',
					'edge',
					'bottom',
				},
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
				type = {
					'element',
					'attribute',
				},
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
				type = {
					'text'
				},
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
				type = {
					'divider'
				},
				top = container,
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
				type = {
					'outline',
					'left',
				},
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
				type = {
					'outline',
					'right',
				},
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
				type = {
					'outline',
					'top',
				},
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
				type = {
					'outline',
					'bottom',
				},
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
				('type','edge'),
				('type','left'),
				('parent',container),
			))
		)[0]
		right_border = list(
			self.find(AND_(
				('type','border'),
				('type','edge'),
				('type',"right"),
				('parent',container),
			))
		)[0]
		bottom_border = list(
			self.find(AND_(
				('type','border'),
				('type','edge'),
				('type','bottom'),
				('parent',container),
			))
		)[0]
		bottom_left_corner = list(
			self.find(AND_(
				('type','border'),
				('type','corner'),
				('top',False),
				('left',True),
				('parent',container),
			))
		)[0]
		bottom_right_corner = list(
			self.find(AND_(
				('type','border'),
				('type','corner'),
				('top',False),
				('left',False),
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
		width = x2 - x1
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
						('type','attribute'),
						('container',eid),
						('index',i)
					)
				)
			)[0]
			(xa,ya,xb,yb) = self.canvas.coords(attribute)
			self.place_attribute(
				attribute,
				x1,
				y1 + height,
				yb - ya
			)
			height += yb - ya
		y2 = y1 + height
		for element in self.find(('parent',eid)):
			attrs = self.get_attributes(element)
			if 'border' in attrs['type']:
				if 'corner' in attrs['type']:
					if attrs['top']:
						if attrs['left']:
							self.canvas.coords(
								element,
								x1,
								y1,
								x1 + self.type_border_thickness,
								y1 + self.type_border_thickness,
							)
						else:
							self.canvas.coords(
								element,
								x2 - self.type_border_thickness,
								y1,
								x2,
								y1 + self.type_border_thickness,
							)
					else:
						if attrs['left']:
							self.canvas.coords(
								element,
								x1,
								y2 - self.type_border_thickness,
								x1 + self.type_border_thickness,
								y2,
							)
						else:
							self.canvas.coords(
								element,
								x2 - self.type_border_thickness,
								y2 - self.type_border_thickness,
								x2,
								y2,
							)
				elif 'edge' in attrs['type']:
					if 'left' in attrs['type']:
						self.canvas.coords(
							element,
							x1,
							y1 + self.type_border_thickness,
							x1 + self.type_border_thickness,
							y2 - self.type_border_thickness,
						)
					elif 'right' in attrs['type']:
						self.canvas.coords(
							element,
							x2 - self.type_border_thickness,
							y1 + self.type_border_thickness,
							x2,
							y2 - self.type_border_thickness,
						)
					elif 'top' in attrs['type']:
						self.canvas.coords(
							element,
							x1 + self.type_border_thickness,
							y1,
							x2 - self.type_border_thickness,
							y1 + self.type_border_thickness,
						)
					elif 'bottom' in attrs['type']:
						self.canvas.coords(
							element,
							x1 + self.type_border_thickness,
							y2 - self.type_border_thickness,
							x2 - self.type_border_thickness,
							y2,
						)
					else:
						raise TypeError('Invalid type: ' + str(attrs['type']))
				else:
					raise TypeError('Invalid type: ' + str(attrs['type']))
			elif 'text' in attrs['type']:
				self.canvas.coords(
					element,
					(x1 + x2) / 2,
					(y1 + y2) / 2,
				)
			else:
				raise TypeError('Invalid type: ' + str(attrs['type']))
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
			if 'outline' in attrs['type']:
				if 'left' in attrs['type']:
					self.canvas.coords(
						element,
						x1,
						y1,
						x1 + self.attribute_border_thickness,
						y2,
					)
				elif 'right' in attrs['type']:
					self.canvas.coords(
						element,
						x2 - self.attribute_border_thickness,
						y1,
						x2,
						y2,
					)
				elif 'top' in attrs['type']:
					self.canvas.coords(
						element,
						x1,
						y1,
						x2,
						y1 + self.attribute_border_thickness,
					)
				elif 'bottom' in attrs['type']:
					self.canvas.coords(
						element,
						x1,
						y2 - self.attribute_border_thickness,
						x2,
						y2,
					)
				else:
					raise TypeError('Invalid type: ' + str(attrs['type']))
			elif 'text' in attrs['type']:
				self.canvas.coords(
					element,
					(x1 + x2) / 2,
					(y1 + y2) / 2,
				)
			elif 'divider' in attrs['type']:
				self.canvas.coords(
					element,
					x1,
					y1,
					x2,
					y1 + self.attribute_border_thickness,
				)
			else:
				raise TypeError('Invalid type: ' + str(attrs['type']))
	def right_click(self,event):
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
					type = {
						'entry'
					},
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
				type = {
					'text'
				},
				parent = parent
			),
		)