import tkinter as tk
import json
from tags import *
from typing import Callable,Any
from glb import *
'''
y = m1x + b1
y = m2x + b2
m1x + b1 = m2x + b2
m1x = m2x + b2 - b1
(m1 - m2)x = b2 - b1
x = (b2 - b1)/(m1 - m2)
'''

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
			fill = "#ddd",
			tags = TAGS_(
				important = False
			)
		)
	for y in range(0,root.winfo_screenheight(),grid_size):
		canvas.create_line(
			0,
			y,
			root.winfo_screenwidth(),
			y,
			fill = "#ddd",
			tags = TAGS_(
				important = False
			)
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

number = int | float
line = dict[str,number]

def get_slope(x1,y1,x2,y2):
	return (y2 - y1)/(x2 - x1)
def get_slope_intersect(x1,y1,x2,y2,x3,y3,m) -> tuple[number,number] | None:
	if x3 == x2:
		x = x2
		y = m * (x - x1) + y1
		return x, y
	mA = (y3 - y2) / (x3 - x2)
	if mA == m:
		return None
	x = (mA * x2 - m * x1 + y1 - y2) / (mA - m)
	y = m * (x - x1) + y1
	return x, y

SHAPE_KEYS = {
	'type' : {
		('border')
	}
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
		self.operation_width = 8
		self.type_width = 28
		self.type_height = 16
		self.attr_width = self.type_width
		self.attr_height = self.type_height // 2
		self.type_border_thickness = 10
		self.attribute_border_thickness = 5
		self.arrow_height = self.grid_size * 2
		self.arrow_base = self.grid_size

	def get_shape_coords(x : int,y : int,length : int,height : int):
		(x,y,length,height) = self.get_true_coords(x,y,length,height)
		

	def find(self,value):
		return self.canvas.find_withtag(TAGS_(value))
	def remove_property(self,query,tag):
		self.canvas.dtag(
			TAGS_(query) if not isinstance(query,int) else query,
			TAGS_(tag)
		)
	def add_property(self,query,tag):
		self.canvas.addtag_withtag(
			TAGS_(tag),
			TAGS_(query) if not isinstance(query,int) else query
		)
	def find_overlapping(self,x1 : int,y1 : int,x2 : int,y2 : int) -> set:
		return set(
			self.canvas.find_overlapping(
				x1,
				y1,
				x2,
				y2
			)
		) & set(
			self.find(~q('important','=',False))
		)
	def event_hierarchy(self,event_type : str,*eids : tuple[int,...]):
		global hierarchies

		obj_types = {}
		for eid in eids:
			props = self.get_properties(eid)
			if 'type' in props:
				obj_types[eid] = hierarchies[event_type].index(props['type'][0])
		if len(obj_types) == 0:
			return None
		max_val = max(obj_types.values())
		for eid,h in obj_types.items():
			if h == max_val:
				return eid
	def get_bounds(self,eid : int) -> tuple[int,int,int,int]:
		(x1,y1,x2,y2) = self.canvas.coords(eid)
		attributes = self.find(
			q('type[0]','=','element') &
			q('container','=',eid)
		)
		if len(attributes) > 0:
			last_attribute = self.find(
				q('type[0]','=','element') &
				q('container','=',eid) &
				q('index','=',len(attributes) - 1)
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
		if 'link_state' in self.attributes: # Handling link
			if 'link_start' not in self.attributes:
				# Handle cursor
				self.canvas.config(cursor = 'dot')
				if eid is None:
					return

				# Handle highlighting
				for border in self.find(
					q('type[0]','in',['border','outline'])
				):
					props = self.get_properties(border)
					if props.get('parent',None) == eid:
						self.canvas.itemconfigure(
							border,
							fill = props['fill'],
							outline = props['outline']
						)
					else:
						self.canvas.itemconfigure(
							border,
							fill = '',
							outline = ''
						)
			elif 'link_end' not in self.attributes:
				self.canvas.tag_lower(self.attributes['link_line'])
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
				for border in self.find(
					q('type[0]','in',['border','outline'])
				):
					props = self.get_properties(border)
					if props.get('parent',None) == eid:
						self.canvas.itemconfigure(
							border,
							fill = props['fill'],
							outline = props['outline']
						)
					else:
						self.canvas.itemconfigure(
							border,
							fill = '',
							outline = ''
						)
		else: # Not handling link
			selected = self.find(q('selected','=',True))
			if top and len(selected) > 0: # There is an element that is selected
				val = selected[0]
				# Cursor starting position
				(cx1,cy1) = self.attributes['selected_element_cursor_source']
				# Cursor current position
				(cx2,cy2) = (x,y)
				# Cursor movement vector
				vector = self.get_grid_coords(cx2 - cx1,cy2 - cy1)
				# Attributes of selected value
				props = self.get_properties(val)
				# Type of selected value
				hold = set()
				match props.get('type',[])[:3]:
					case ['divider']:
						hold.add(val)

						(top_coords,bottom_coords) = self.attributes['selected_element_source_coords']
						(tx1,ty1,tx2,ty2) = top_coords
						(bx1,by1,bx2,by2) = bottom_coords
						top_props = self.get_properties(props['top'])
						self.place_attribute(
							props['bottom'],
							bx1,
							by1 + vector[1],
							by2 - by1 - vector[1],
						)
						match top_props['type'][1]:
							case 'type':
								self.place_type(
									props['top'],
									tx1,
									ty1,
									tx2,
									ty2 + vector[1],
								)
							case 'attribute':
								self.place_attribute(
									props['top'],
									tx1,
									ty1,
									ty2 - ty1 + vector[1]
								)
							case _:
								raise TypeError('Invalid subtype: ' + str(top_props['type'][0]))
					case ['element','type']:
						hold |= set(
							self.find(q('parent','=',val))
						)
						(x1,y1,x2,y2) = self.attributes['selected_element_source_coords']
						self.place_type(
							val,
							x1 + vector[0],
							y1 + vector[1],
							x2 + vector[0],
							y2 + vector[1],
						)
					case ['element','attribute']:
						hold |= set(
							self.find(q('parent','=',val))
						)
						if eid is not None:
							hold.add(eid)
							properties = self.get_properties(eid)
							if 'type' in properties and properties['type'][0] == 'divider':
								self.canvas.itemconfigure(
									eid,
									fill = properties['fill'],
									outline = properties['outline'],
								)
					case ['element','operation']:
						hold |= set(
							self.find(q('parent','=',val))
						)
						(
							x1,y1,
							x2,y2,
							x3,y3,
							x4,y4,
							x5,y5
						) = self.attributes['selected_element_source_coords']
						self.place_operation(
							val,
							x1 + vector[0],
							y1 + vector[1],
							length = abs(x3 - x4),
							height = abs(y3 - y1),
						)
					case ['border','edge','top']:
						hold |= set(
							self.find(q('parent','=',props['parent']))
						)
						(
							x1,y1,
							x2,y2,
						) = self.attributes['selected_element_source_coords']
						self.place_type(
							props['parent'],
							x1,
							y1 + vector[1],
							x2,
							y2,
						)
					case ['border','edge','bottom']:
						hold |= set(
							self.find(q('parent','=',props['parent']))
						)
						(
							x1,y1,
							x2,y2,
						) = self.attributes['selected_element_source_coords']
						self.place_type(
							props['parent'],
							x1,
							y1,
							x2,
							y2 + vector[1],
						)
					case ['border','edge','left'] | ['border','corner','midleft']:
						hold |= set(
							self.find(q('parent','=',props['parent']))
						)
						parent_props = self.get_properties(props['parent'])
						match parent_props['type'][1]:
							case 'type':
								(
									x1,y1,
									x2,y2,
								) = self.attributes['selected_element_source_coords']
								self.place_type(
									props['parent'],
									x1 + vector[0],
									y1,
									x2,
									y2,
								)
							case 'operation':
								(
									x1,y1,
									x2,y2,
									x3,y3,
									x4,y4,
									x5,y5,
								) = self.attributes['selected_element_source_coords']
								x4 += vector[0]
								x5 += vector[0]
								length = x3 - x4
								if length % 2 == 0:
									x1 = x3 - length // 2
									self.place_operation(
										props['parent'],
										x1,
										y1,
										length,
										y3 - y1
									)
							case _:
								raise TypeError('Invalid subtype: ' + str(parent_props['type'][1]))
					case ['border','edge','right'] | ['border','corner','midright']:
						hold |= set(
							self.find(q('parent','=',props['parent']))
						)
						parent_props = self.get_properties(props['parent'])
						match parent_props['type'][1]:
							case 'type':
								(
									x1,y1,
									x2,y2,
								) = self.attributes['selected_element_source_coords']
								self.place_type(
									props['parent'],
									x1,
									y1,
									x2 + vector[0],
									y2,
								)
							case 'operation':
								(
									x1,y1,
									x2,y2,
									x3,y3,
									x4,y4,
									x5,y5,
								) = self.attributes['selected_element_source_coords']
								x2 += vector[0]
								x3 += vector[0]
								length = x3 - x4
								if length % 2 == 0:
									x1 = x3 - length // 2
									self.place_operation(
										props['parent'],
										x1,
										y1,
										length,
										y3 - y1
									)
							case _:
								raise TypeError('Invalid subtype: ' + str(parent_props['type'][1]))
					case ['border','corner','topleft']:
						hold |= set(
							self.find(q('parent','=',props['parent']))
						)
						(
							x1,y1,
							x2,y2,
						) = self.attributes['selected_element_source_coords']
						self.place_type(
							props['parent'],
							x1 + vector[0],
							y1 + vector[1],
							x2,
							y2,
						)
					case ['border','corner','topright']:
						hold |= set(
							self.find(q('parent','=',props['parent']))
						)
						(
							x1,y1,
							x2,y2,
						) = self.attributes['selected_element_source_coords']
						self.place_type(
							props['parent'],
							x1,
							y1 + vector[1],
							x2 + vector[0],
							y2,
						)
					case ['border','corner','bottomleft']:
						hold |= set(
							self.find(q('parent','=',props['parent']))
						)
						(
							x1,y1,
							x2,y2,
						) = self.attributes['selected_element_source_coords']
						self.place_type(
							props['parent'],
							x1 + vector[0],
							y1,
							x2,
							y2 + vector[1],
						)
					case ['border','edge','bottomleft']:
						hold |= set(
							self.find(q('parent','=',props['parent']))
						)
						(
							x1,y1,
							x2,y2,
							x3,y3,
							x4,y4,
							x5,y5,
						) = self.attributes['selected_element_source_coords']
						self.place_operation(
							props['parent'],
							x1 + vector[0],
							y1 + vector[1],
							length = abs(x2 - x5 - vector[0]),
							height = abs(y1 - vector[1] - y3)
						)
					case ['border','corner','bottomright']:
						hold |= set(
							self.find(q('parent','=',props['parent']))
						)
						(
							x1,y1,
							x2,y2,
						) = self.attributes['selected_element_source_coords']
						self.place_type(
							props['parent'],
							x1,
							y1,
							x2 + vector[0],
							y2 + vector[1],
						)
				hidden = set(
					self.find(
						q('type[0]','in',['border','outline','divider'])
					)
				) - hold
				for border in hidden:
					self.canvas.itemconfigure(
						border,
						fill = '',
						outline = ''
					)
			elif eid is not None: # There is an element that is highlighted
				props = self.get_properties(eid)
				for border in self.find(
					q('type[0]','in',['border','outline','divider'])
				):
					self.canvas.itemconfigure(
						border,
						fill = '',
						outline = ''
					)
				if top: # Set cursor
					if 'cursor' not in props:
						self.canvas.config(cursor = 'left_ptr')
					else:
						self.canvas.config(cursor = props['cursor'])
				match props.get('type',[])[:1]: # Set other behavior for eid
					case ['text'] | ['border']:
						# Implies hovering over parent element
						self.handle_hover(x,y,False,props['parent'])
					case ['outline']:
						# Equivalent to hovering over parent element
						self.handle_hover(x,y,top,props['parent'])
					case ['element']:
						borders = self.find(
							q('type[0]','in',['border','outline']) &
							q('parent','=',eid)
						)
						for border in borders:
							props = self.get_properties(border)
							self.canvas.itemconfigure(
								border,
								outline = props['outline'],
								fill = props['fill']
							)
					case ['divider']:
						self.canvas.itemconfigure(
							eid,
							outline = props['outline'],
							fill = props['fill'],
						)
					case _:
						raise TypeError('Invalid type: ' + str(props.get('type',[])[:1]))
			else:
				for border in self.find(
					q('type[0]','in',['border','outline','divider'])
				):
					self.canvas.itemconfigure(
						border,
						fill = '',
						outline = ''
					)
				self.canvas.config(cursor = 'left_ptr')
	def handle_left_click(self,x : int,y : int,top : bool,*eids : tuple[int,...]):
		self.finish_entries()
		match len(eids):
			case 1:
				eid = eids[0]
			case 0:
				eid = None
			case _:
				eid = self.event_hierarchy('left-click',*eids)
		if 'link_state' in self.attributes:
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
							type = [
								'line'
							],
							start = eid,
						)
					)
					self.canvas.tag_lower(self.attributes['link_line'])
				elif 'link_end' not in self.attributes:
					self.attributes['link_end'] = eid
				else:
					del self.attributes['link_state']
					del self.attributes['link_start']
					del self.attributes['link_end']
		else:
			selected = self.find(
				q('selected','=',True)
			)
			if len(selected) > 0:
				if eid is not None:
					sel_props = self.get_properties(selected[0])
					hov_props = self.get_properties(eid)
					if (
						'type' in sel_props and
						'type' in hov_props and
						sel_props['type'][:2] == ['element','attribute'] and
						hov_props['type'] == ['divider']
					):
						self.shift_attribute(
							container = sel_props['container'],
							index1 = sel_props['index'],
							index2 = self.get_properties(hov_props['bottom'])['index']
						)
				tag = q('selected','=',True)
				self.remove_property(tag,tag)
				return
			if eid is None:
				return
			props = self.get_properties(eid)
			if 'type' not in props:
				return
			self.add_property(
				eid,
				q('selected','=',True)
			)
			self.attributes['selected_element_cursor_source'] = (x,y)
			props = self.get_properties(eid)
			if 'parent' in props:
				self.attributes['selected_element_source_coords'] = self.get_grid_coords(
					*self.canvas.coords(props['parent'])
				)
			elif 'top' in props and 'bottom' in props:
				self.attributes['selected_element_source_coords'] = (
					self.get_grid_coords(
						*self.canvas.coords(props['top'])
					),
					self.get_grid_coords(
						*self.canvas.coords(props['bottom'])
					)
				)
			else:
				self.attributes['selected_element_source_coords'] = self.get_grid_coords(
					*self.canvas.coords(eid)
			)
	def handle_double_left_click(self,x : int,y : int,top : bool,*eids : tuple[int,...]):
		entries = list(self.attributes['entries'].values())
		for entry in entries:
			self.finish_entry(entry)
		elements = set(
			self.find_overlapping(
				event.x,
				event.y,
				event.x,
				event.y,
			)
		)
		eid = None
		for element in elements:
			props = self.get_properties(element)
			if 'type' in props and props['type'] == 'text':
				eid = element
				break
		if eid is not None:
			parent = props['parent']
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
					type = [
						'entry'
					],
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
	def handle_right_click(self,x : int,y : int,top : bool,*eids : tuple[int,...]):
		self.finish_entries()
		if 'link_state' in self.attributes:
			del self.attributes['link_state']
			if 'link_start' in self.attributes:
				del self.attributes['link_start']
			if 'link_end' in self.attributes:
				del self.attributes['link_end']
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
				add_tooltip.add_command(
					label = 'Operation',
					command = self.tooltip_create_operation
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
				props = self.get_properties(eid)
				add_tooltip = tk.Menu(
					self.tooltip,
					tearoff = 0,
				)
				match props.get('type',[])[:2]:
					case ['element','type']:
						add_tooltip.add_command(
							label = 'Attribute',
							command = self.tooltip_add_attribute,
						)
					case ['border','edge'] | ['border','corner']:
						self.handle_right_click(
							x,
							y,
							False,
							props['parent']
						)
						return
					case _:
						self.canvas.itemconfigure(eid,fill='yellow')
						raise TypeError('Invalid type: ' + str(props.get('type',[])[:2]))
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
	def get_properties(self,eid : int) -> dict:
		properties = [tag for tag in self.canvas.gettags(eid) if '_' in tag]
		if len(properties) > 0:
			return properties_to_type(properties)
		return {}
	def get_children(self,eid : int) -> set[int]:
		return self.find(q('parent','=',eid))
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
				type = [
					'element',
					'type'
				],
				cursor = 'fleur',
			),
			fill = 'white',
			outline = 'black',
		)
		self.canvas.create_text(
			(x1 + x2) / 2,
			(y1 + y2) / 2,
			text = '<Type>',
			tags = TAGS_(
				type = [
					'text'
				],
				cursor = 'xterm',
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
				type = [
					'border',
					'edge',
					'left'
				],
				cursor = 'left_side',
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
				type = [
					'border',
					'edge',
					'right'
				],
				cursor = 'right_side',
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
				type = [
					'border',
					'edge',
					'top'
				],
				cursor = 'top_side',
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
				type = [
					'border',
					'edge',
					'bottom'
				],
				cursor = 'bottom_side',
				fill = 'yellow',
				outline = 'black',
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
				type = [
					'border',
					'corner',
					'topleft'
				],
				cusror = 'top_left_corner',
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
				type = [
					'border',
					'corner',
					'bottomleft'
				],
				cursor = 'bottom_left_corder',
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
				type = [
					'border',
					'corner',
					'topright'
				],
				cursor = 'top_right_corner',
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
				type = [
					'border',
					'corner',
					'bottomright'
				],
				cursor = 'bottom_right_corner',
				fill = 'white',
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
				q('container','=',container) &
				q('type','=',['element','attribute'])
			)
		)
		eid = self.canvas.create_rectangle(
			x1,
			y1,
			x2,
			y2,
			tags = TAGS_(
				type = [
					'element',
					'attribute'
				],
				cursor = 'fleur',
				container = container,
				index = index,
			),
			fill = 'white',
			outline = 'black',
		)
		self.canvas.create_text(
			(x1 + x2) / 2,
			(y1 + y2) / 2,
			text = '<Attribute-' + str(index) + '>',
			tags = TAGS_(
				type = [
					'text'
				],
				cursor = 'xterm',
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
				type = [
					'divider'
				],
				cursor = 'double_arrow',
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
				type = [
					'outline',
					'left'
				],
				cursor = 'fleur',
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
				type = [
					'outline',
					'right'
				],
				cursor = 'fleur',
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
				type = [
					'outline',
					'top'
				],
				cursor = 'fleur',
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
				type = [
					'outline',
					'bottom'
				],
				cursor = 'fleur',
				fill = 'black',
				outline = 'black',
				parent = eid
			),
		)
		# Adjust container borders
		(x1,y1,x2,y2) = self.canvas.coords(container)
		height = y2 - y1
		for element in self.find(q('container','=',container)):
			(xa,ya,xb,yb) = self.canvas.coords(element)
			height += yb - ya
		left_border = list(
			self.find(
				q('type','=',['border','edge','left']) &
				q('parent','=',container)
			)
		)[0]
		right_border = list(
			self.find(
				q('type','=',['border','edge','right']) &
				q('parent','=',container)
			)
		)[0]
		bottom_border = list(
			self.find(
				q('type','=',['border','edge','bottom']) &
				q('parent','=',container)
			)
		)[0]
		bottomleft_corner = list(
			self.find(
				q('type','=',['border','corner','bottomleft']) &
				q('parent','=',container)
			)
		)[0]
		bottomright_corner = list(
			self.find(
				q('type','=',['border','corner','bottomright']) &
				q('parent','=',container)
			)
		)[0]
		(x1,y1,x2,y2) = (x1,y1,x2,y1 + height)
		# BOTTOM LEFT
		self.canvas.coords(
			bottomleft_corner,
			x1,
			y2 - self.type_border_thickness,
			x1 + self.type_border_thickness,
			y2,
		)
		# BOTTOM RIGHT
		self.canvas.coords(
			bottomright_corner,
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
		self.canvas.tag_raise(bottomleft_corner)
		self.canvas.tag_raise(bottomright_corner)
		self.canvas.tag_raise(left_border)
		self.canvas.tag_raise(right_border)
		self.canvas.tag_raise(bottom_border)
		return eid
	def create_operation(self,x : int,y : int,length : int):
		(x,y,length,height) = self.get_true_coords(x,y,length,self.operation_width)
		eid = self.canvas.create_polygon(
			x,y,
			x + length // 2,y - height // 2,
			x + length // 2,y - height,
			x - length // 2,y - height,
			x - length // 2,y - height // 2,
			fill = 'white',
			outline = 'black',
			tags = TAGS_(
				type = [
					'element',
					'operation',
				],
				cursor = 'fleur',
			)
		)
		# LEFT
		self.canvas.create_rectangle(
			x - length // 2,
			y - height,
			x - length // 2 + self.type_border_thickness,
			y - height // 2,
			fill = '',
			outline = '',
			tags = TAGS_(
				type = [
					'border',
					'edge',
					'left'
				],
				cursor = 'left_side',
				fill = 'yellow',
				outline = 'black',
				parent = eid
			),
		)
		# RIGHT
		self.canvas.create_rectangle(
			x + length // 2 - self.type_border_thickness,
			y - height,
			x + length // 2,
			y - height // 2,
			fill = '',
			outline = '',
			tags = TAGS_(
				type = [
					'border',
					'edge',
					'right'
				],
				cursor = 'right_side',
				fill = 'yellow',
				outline = 'black',
				parent = eid
			),
		)
		# TOP
		self.canvas.create_rectangle(
			x - length // 2,
			y - height,
			x + length // 2,
			y - height + self.type_border_thickness,
			fill = '',
			outline = '',
			tags = TAGS_(
				type = [
					'border',
					'edge',
					'top'
				],
				cursor = 'top_side',
				fill = 'yellow',
				outline = 'black',
				parent = eid
			),
		)
		# BOTTOM LEFT
		(xn,yn) = get_slope_intersect(
			x - length // 2 + self.type_border_thickness,
			y - height // 2 - self.type_border_thickness,
			x,
			y,
			x + length // 2,
			y - height // 2,
			get_slope(x - length // 2,y - height // 2,x,y),
		)
		self.canvas.create_polygon(
			x - length // 2,y - height // 2,
			x - length // 2 + self.type_border_thickness,y - height // 2 - self.type_border_thickness,
			xn,yn,
			x,y,
			fill = '',
			outline = '',
			tags = TAGS_(
				type = [
					'border',
					'edge',
					'bottomleft'
				],
				cursor = 'bottom_left_corner',
				fill = 'yellow',
				outline = 'black',
				parent = eid
			),
		)
		# BOTTOM RIGHT
		(xn,yn) = get_slope_intersect(
			x + length // 2 - self.type_border_thickness,
			y - height // 2 - self.type_border_thickness,
			x,
			y,
			x - length // 2,
			y - height // 2,
			get_slope(x,y,x + length // 2,y - height // 2),
		)
		self.canvas.create_polygon(
			x + length // 2,y - height // 2,
			x + length // 2 - self.type_border_thickness,y - height // 2 - self.type_border_thickness,
			xn,yn,
			x,y,
			fill = '',
			outline = '',
			tags = TAGS_(
				type = [
					'border',
					'edge',
					'bottomright'
				],
				cursor = 'bottom_right_corner',
				fill = 'yellow',
				outline = 'black',
				parent = eid
			),
		)
		# TOP LEFT
		self.canvas.create_rectangle(
			x - length // 2,
			y - height,
			x - length // 2 + self.type_border_thickness,
			y - height + self.type_border_thickness,
			fill = '',
			outline = '',
			tags = TAGS_(
				type = [
					'border',
					'corner',
					'topleft'
				],
				cusror = 'top_left_corner',
				fill = 'white',
				outline = 'black',
				parent = eid
			),
		)
		# TOP RIGHT
		self.canvas.create_rectangle(
			x + length // 2 - self.type_border_thickness,
			y - height,
			x + length // 2,
			y - height + self.type_border_thickness,
			fill = '',
			outline = '',
			tags = TAGS_(
				type = [
					'border',
					'corner',
					'topright'
				],
				cursor = 'top_right_corner',
				fill = 'white',
				outline = 'black',
				parent = eid
			),
		)
		# MID LEFT
		self.canvas.create_rectangle(
			x - length // 2,
			y - height // 2 - self.type_border_thickness,
			x - length // 2 + self.type_border_thickness,
			y - height // 2,
			fill = '',
			outline = '',
			tags = TAGS_(
				type = [
					'border',
					'corner',
					'midleft'
				],
				cusror = 'left_side',
				fill = 'white',
				outline = 'black',
				parent = eid
			),
		)
		# MID RIGHT
		self.canvas.create_rectangle(
			x + length // 2 - self.type_border_thickness,
			y - height // 2 - self.type_border_thickness,
			x + length // 2,
			y - height // 2,
			fill = '',
			outline = '',
			tags = TAGS_(
				type = [
					'border',
					'corner',
					'midright'
				],
				cursor = 'right_side',
				fill = 'white',
				outline = 'black',
				parent = eid
			),
		)
	def tooltip_create_type(self):
		self.create_type(
			self.attributes['tooltip_coords'][0],
			self.attributes['tooltip_coords'][1],
		)
	def tooltip_create_operation(self):
		self.create_operation(
			self.attributes['tooltip_coords'][0],
			self.attributes['tooltip_coords'][1],
			length = 10,
		)
	def tooltip_add_attribute(self):
		num_attrs = len(
			self.find(
				q('container','=',self.attributes['tooltip_element']) &
				q('type','=',['element','attribute'])
			)
		)
		(cx1,cy1,cx2,cy2) = self.get_grid_coords(
			*self.canvas.coords(
				self.attributes['tooltip_element']
			)
		)
		if num_attrs > 0:
			(ax1,ay1,ax2,ay2) = self.get_grid_coords(
				*self.canvas.coords(
					self.find(
						q('container','=',self.attributes['tooltip_element']) &
						q('type','=',['element','attribute']) &
						q('index','=',num_attrs - 1)
					)[0]
				)
			)
			(x,y) = (cx1,ay2)
		else:
			(x,y) = (cx1,cy2)
		self.create_attribute(
			self.attributes['tooltip_element'],x,y
		)
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
		props = self.get_properties(eid)
		(x1,y1,x2,y2) = self.get_true_coords(x1,y1,x2,y2)
		self.canvas.coords(
			eid,
			x1,
			y1,
			x2,
			y2
		)
		for text in self.find(
			q('type','=',['text']) &
			q('parent','=',eid)
		):
			self.canvas.coords(
				text,
				(x1 + x2) / 2,
				(y1 + y2) / 2,
			)
		attributes = self.find(
			q('type','=',['element','attribute']) &
			q('container','=',eid)
		)
		height = y2 - y1
		for i in range(len(attributes)):
			attribute = list(
				self.find(
					q('type','=',['element','attribute']) &
					q('container','=',eid) &
					q('index','=',i)
				)
			)[0]
			(xa,ya,xb,yb) = self.canvas.coords(attribute)
			(m,n,p,r) = self.get_grid_coords(
				x1,y1 + height,yb,ya
			)
			self.place_attribute(
				attribute,
				m,
				n,
				p - r
			)
			height += yb - ya
		y2 = y1 + height
		for element in self.find(q('parent','=',eid)):
			props = self.get_properties(element)
			match props.get('type',[])[:3]:
				case ['border','corner','topleft']:
					self.canvas.coords(
						element,
						x1,
						y1,
						x1 + self.type_border_thickness,
						y1 + self.type_border_thickness,
					)
				case ['border','corner','topright']:
					self.canvas.coords(
						element,
						x2 - self.type_border_thickness,
						y1,
						x2,
						y1 + self.type_border_thickness,
					)
				case ['border','corner','bottomleft']:
					self.canvas.coords(
						element,
						x1,
						y2 - self.type_border_thickness,
						x1 + self.type_border_thickness,
						y2,
					)
				case ['border','corner','bottomright']:
					self.canvas.coords(
						element,
						x2 - self.type_border_thickness,
						y2 - self.type_border_thickness,
						x2,
						y2,
					)
				case ['border','edge','left']:
					self.canvas.coords(
						element,
						x1,
						y1 + self.type_border_thickness,
						x1 + self.type_border_thickness,
						y2 - self.type_border_thickness,
					)
				case ['border','edge','right']:
					self.canvas.coords(
						element,
						x2 - self.type_border_thickness,
						y1 + self.type_border_thickness,
						x2,
						y2 - self.type_border_thickness,
					)
				case ['border','edge','top']:
					self.canvas.coords(
						element,
						x1 + self.type_border_thickness,
						y1,
						x2 - self.type_border_thickness,
						y1 + self.type_border_thickness,
					)
				case ['border','edge','bottom']:
					self.canvas.coords(
						element,
						x1 + self.type_border_thickness,
						y2 - self.type_border_thickness,
						x2 - self.type_border_thickness,
						y2,
					)
				case ['text']:
					pass
				case _:
					raise TypeError('Invalid type: ' + str(props.get('type',[])[:3]))
	def place_attribute(self,eid : int,x : int,y : int,height : int):
		props = self.get_properties(eid)
		container = props['container']
		(xa,_,xb,yb) = self.get_grid_coords(
			*self.canvas.coords(container)
		)
		width = xb - xa
		x2 = x + width
		y2 = y + height
		(xa,ya,xb,yb) = self.get_grid_coords(
			*self.canvas.coords(eid)
		)
		(x1,y1,x2,y2) = self.get_true_coords(x,y,x2,y2)
		self.canvas.coords(
			eid,
			x1,
			y1,
			x2,
			y2
		)
		for element in self.find(
			(
				q('type[0]','in',['outline','text']) &
				q('parent','=',eid)
			) | (
				q('type','=',['divider']) &
				q('bottom','=',eid)
			)
		):
			props = self.get_properties(element)
			match props.get('type',[])[:2]:
				case ['outline','left']:
					self.canvas.coords(
						element,
						x1,
						y1,
						x1 + self.attribute_border_thickness,
						y2,
					)
				case ['outline','right']:
					self.canvas.coords(
						element,
						x2 - self.attribute_border_thickness,
						y1,
						x2,
						y2,
					)
				case ['outline','top']:
					self.canvas.coords(
						element,
						x1,
						y1,
						x2,
						y1 + self.attribute_border_thickness,
					)
				case ['outline','bottom']:
					self.canvas.coords(
						element,
						x1,
						y2 - self.attribute_border_thickness,
						x2,
						y2,
					)
				case ['text']:
					self.canvas.coords(
						element,
						(x1 + x2) / 2,
						(y1 + y2) / 2,
					)
				case ['divider']:
					self.canvas.coords(
						element,
						x1,
						y1,
						x2,
						y1 + self.attribute_border_thickness,
					)
				case _:
					raise TypeError('Invalid type: ' + str(props.get('type',[])[:2]))
	def place_operation(self,eid : int,x : int,y : int,length : int,height : int):
		if length % 2 != 0:
			raise TypeError(length)
		(x,y,length,height) = self.get_true_coords(x,y,length,height)
		self.canvas.coords(
			eid,
			x,y,
			x + length // 2,y - height // 2,
			x + length // 2,y - height,
			x - length // 2,y - height,
			x - length // 2,y - height // 2,
		)
		for element in self.find(q('parent','=',eid)):
			props = self.get_properties(element)
			match props.get('type',[])[:3]:
				case ['border','edge','top']:
					self.canvas.coords(
						element,
						x - length // 2,
						y - height,
						x + length // 2,
						y - height + self.type_border_thickness,
					)
				case ['border','edge','left']:
					self.canvas.coords(
						element,
						x - length // 2,
						y - height,
						x - length // 2 + self.type_border_thickness,
						y - height // 2,
					)
				case ['border','edge','right']:
					self.canvas.coords(
						element,
						x + length // 2 - self.type_border_thickness,
						y - height,
						x + length // 2,
						y - height // 2,
					)
				case ['border','corner','topleft']:
					self.canvas.coords(
						element,
						x - length // 2,
						y - height,
						x - length // 2 + self.type_border_thickness,
						y - height + self.type_border_thickness,
					)
				case ['border','corner','topright']:
					self.canvas.coords(
						element,
						x + length // 2 - self.type_border_thickness,
						y - height,
						x + length // 2,
						y - height + self.type_border_thickness,
					)
				case ['border','corner','midleft']:
					self.canvas.coords(
						element,
						x - length // 2,
						y - height // 2 - self.type_border_thickness,
						x - length // 2 + self.type_border_thickness,
						y - height // 2,
					)
				case ['border','corner','midright']:
					self.canvas.coords(
						element,
						x + length // 2 - self.type_border_thickness,
						y - height // 2 - self.type_border_thickness,
						x + length // 2,
						y - height // 2,
					)
				case ['border','edge','bottomleft']:
					(xn,yn) = get_slope_intersect(
						x - length // 2 + self.type_border_thickness,
						y - height // 2 - self.type_border_thickness,
						x,
						y,
						x + length // 2,
						y - height // 2,
						get_slope(x - length // 2,y - height // 2,x,y),
					)
					self.canvas.coords(
						element,
						x - length // 2,y - height // 2,
						x - length // 2 + self.type_border_thickness,y - height // 2 - self.type_border_thickness,
						xn,yn,
						x,y,
					)
				case ['border','edge','bottomright']:
					(xn,yn) = get_slope_intersect(
						x + length // 2 - self.type_border_thickness,
						y - height // 2 - self.type_border_thickness,
						x,
						y,
						x - length // 2,
						y - height // 2,
						get_slope(x,y,x + length // 2,y - height // 2),
					)
					self.canvas.coords(
						element,
						x + length // 2,y - height // 2,
						x + length // 2 - self.type_border_thickness,y - height // 2 - self.type_border_thickness,
						xn,yn,
						x,y,
					)
				case _:
					raise TypeError('Invalid type: ' + str(props.get('type',[])[:3]))
	def shift_attribute(self,container : int,index1 : int,index2 : int):
		if index1 == index2:
			return
		if index1 < index2:
			# Grab attributes between index1 and index2
			attributes = self.find(
				q('index','between',index1,index2)
			)
			attributes = {
				attribute : self.get_properties(attribute) for attribute in attributes
			}
			attributes = {
				props['index'] : {
					'id' : attribute
				} | props for attribute,props in attributes.items()
			}
			(x,y,_,_) = self.get_grid_coords(
				*self.canvas.coords(
					attributes[index1]['id']
				)
			)
			for i in range(index1 + 1,index2 + 1):
				(_,y1,_,y2) = self.get_grid_coords(
					*self.canvas.coords(
						attributes[i]['id']
					)
				)
				height = y2 - y1
				self.remove_property(
					attributes[i]['id'],
					q('index','=',i)
				)
				self.add_property(
					attributes[i]['id'],
					q('index','=',i - 1)
				)
				self.place_attribute(
					attributes[i]['id'],
					x,
					y,
					height
				)
				y += height
			(_,y1,_,y2) = self.get_grid_coords(
				*self.canvas.coords(
					attributes[index1]['id']
				)
			)
			height = y2 - y1
			self.remove_property(
				attributes[index1]['id'],
				q('index','=',index1)
			)
			self.add_property(
				attributes[index1]['id'],
				q('index','=',index2)
			)
			self.place_attribute(
				attributes[index1]['id'],
				x,
				y,
				height
			)
		else:
			# Grab attributes between index1 and index2
			attributes = self.find(
				q('index','between',index2,index1)
			)
			attributes = {
				attribute : self.get_properties(attribute) for attribute in attributes
			}
			attributes = {
				props['index'] : {
					'id' : attribute
				} | props for attribute,props in attributes.items()
			}
			(x,y,_,_) = self.get_grid_coords(
				*self.canvas.coords(
					attributes[index1]['id']
				)
			)
			for i in range(index1 - 1,index2 - 1,-1):
				(_,y1,_,y2) = self.get_grid_coords(
					*self.canvas.coords(
						attributes[i]['id']
					)
				)
				height = y2 - y1
				self.remove_property(
					attributes[i]['id'],
					q('index','=',i)
				)
				self.add_property(
					attributes[i]['id'],
					q('index','=',i + 1)
				)
				self.place_attribute(
					attributes[i]['id'],
					x,
					y,
					height
				)
				y -= height
			(_,y1,_,y2) = self.get_grid_coords(
				*self.canvas.coords(
					attributes[index1]['id']
				)
			)
			height = y2 - y1
			self.remove_property(
				attributes[index1]['id'],
				q('index','=',index1)
			)
			self.add_property(
				attributes[index1]['id'],
				q('index','=',index2)
			)
			self.place_attribute(
				attributes[index1]['id'],
				x,
				y,
				height
			)
	def right_click(self,event):
		self.handle_right_click(
			event.x,
			event.y,
			True,
			*self.find_overlapping(
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
			*self.find_overlapping(
				event.x,
				event.y,
				event.x,
				event.y
			)
		)
	def double_left_click(self,event):
		self.handle_double_left_click(
			event.x,
			event.y,
			True,
			*self.find_overlapping(
				event.x,
				event.y,
				event.x,
				event.y
			)
		)
	def mouse_move(self,event):
		self.handle_hover(
			event.x,
			event.y,
			True,
			*self.find_overlapping(
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
		props = self.get_properties(wid)
		parent = props['parent']
		(x1,x2,y1,y2) = self.canvas.coords(parent)
		xlen = x2 - x1
		widget.destroy()
		self.canvas.delete(wid)
		self.canvas.create_text(
			coords[0],
			coords[1],
			text = text,
			tags = TAGS_(
				type = [
					'text'
				],
				cursor = 'xterm',
				parent = parent
			),
		)