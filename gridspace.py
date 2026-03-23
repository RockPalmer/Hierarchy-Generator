import tkinter as tk
import json
from typing import Callable

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

		# left click down event
		self.canvas.bind(
			'<ButtonPress-1>',
			self.left_click_down,
		)
		# left click up event
		self.canvas.bind(
			'<ButtonRelease-1>',
			self.left_click_up,
		)
		# left click drag event
		self.canvas.bind(
			'<B1-Motion>',
			self.left_click_move,
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
		# right click up event
		self.canvas.bind(
			'<ButtonRelease-3>',
			self.right_click_up,
		)
		self.create_rectangle(
			40,
			40,
			16,
			12,
			fill = "white",
			text = 'Type A',
		)
		self.create_rectangle(
			80,
			80,
			16,
			12,
			fill = "white",
			text = 'Type B',
		)
	def get_attributes(self,eid : int) -> dict:
		attrs = {}
		for tag in self.canvas.gettags(eid):
			if '=' not in tag:
				continue
			index = tag.index('=')
			attrs[tag[:index]] = json.loads(tag[index + 1:])
		return attrs
	def get_types(self,eid : int) -> set[str]:
		return {
			tag for tag in self.canvas.gettags(eid) if '=' not in tag
		}
	def get_children(self,eid : int) -> set[int]:
		return set(
			self.canvas.find_withtag('parent=' + str(eid))
		)
	def get_true_points(self,eid : int) -> set[tuple[int,int]]:
		match self.canvas.type(eid):
			case 'rectangle':
				(x1,y1,x2,y2) = self.canvas.coords(eid)
				return {
					(x1,y1),
					(x1,y2),
					(x2,y1),
					(x2,y2),
				}
			case _:
				raise TypeError
	def check_contains(self,eid : int,x : int,y : int) -> bool:
		match self.canvas.type(eid):
			case 'rectangle':
				(x1,y1,x2,y2) = self.canvas.coords(eid)
				return (
					x >= x1 and
					x < x2 and
					y >= y1 and
					y < y2
				)
			case _:
				raise TypeError
	def create_rectangle(self,x : int,y : int,xlen : int,ylen : int,**attributes) -> int:
		if 'text' in attributes:
			text = attributes['text']
			del attributes['text']
		else:
			text = None
		(x1,y1,x2,y2) = (x,y,x + xlen,y + ylen)
		if xlen > 1:
			x1 -= xlen // 2
			x2 -= xlen // 2
		if ylen > 1:
			x1 -= xlen // 2
			x2 -= xlen // 2
		(x1,y1) = self.get_true_coords(x1,y1)
		(x2,y2) = self.get_true_coords(x2,y2)
		eid = self.canvas.create_rectangle(
			x1,
			y1,
			x2,
			y2,
			**attributes,
			tags = ('type="element"','element_type="block"','minwidth=16','minheight=12'),
		)
		if text is not None:
			self.canvas.create_text(
				(x1 + x2) / 2,
				(y1 + y2) / 2,
				text = text,
				tags = ('type="text"','parent=' + str(eid)),
			)
		self.canvas.create_rectangle(
			x1 - 15,
			y1 - 15,
			x1 - 1,
			y1 - 1,
			fill = '',
			outline = '',
			tags = ('type="border"','border_type="corner"','top=true','left=true','parent=' + str(eid)),
		)
		self.canvas.create_rectangle(
			x1 - 15,
			y2 + 1,
			x1 - 1,
			y2 + 15,
			fill = '',
			outline = '',
			tags = ('type="border"','border_type="corner"','top=false','left=true','parent=' + str(eid)),
		)
		self.canvas.create_rectangle(
			x2 + 1,
			y1 - 15,
			x2 + 15,
			y1 - 1,
			fill = '',
			outline = '',
			tags = ('type="border"','border_type="corner"','top=true','left=false','parent=' + str(eid)),
		)
		self.canvas.create_rectangle(
			x2 + 1,
			y2 + 1,
			x2 + 15,
			y2 + 15,
			fill = '',
			outline = '',
			tags = ('type="border"','border_type="corner"','top=false','left=false','parent=' + str(eid)),
		)
		self.canvas.create_rectangle(
			x1 - 15,
			y1,
			x1 - 1,
			y2,
			fill = '',
			outline = '',
			tags = ('type="border"','border_type="edge"','edge_type="left"','parent=' + str(eid)),
		)
		self.canvas.create_rectangle(
			x2 + 1,
			y1,
			x2 + 15,
			y2,
			fill = '',
			outline = '',
			tags = ('type="border"','border_type="edge"','edge_type="right"','parent=' + str(eid)),
		)
		self.canvas.create_rectangle(
			x1,
			y1 - 15,
			x2,
			y1 - 1,
			fill = '',
			outline = '',
			tags = ('type="border"','border_type="edge"','edge_type="top"','parent=' + str(eid)),
		)
		self.canvas.create_rectangle(
			x1,
			y2 + 1,
			x2,
			y2 + 15,
			fill = '',
			outline = '',
			tags = ('type="border"','border_type="edge"','edge_type="bottom"','parent=' + str(eid)),
		)
		return eid
	def get_grid_coords(self,*vals):
		return tuple(
			round(val / self.grid_size) for val in vals
		)
	def get_true_coords(self,*vals):
		return tuple(
			val * self.grid_size for val in vals
		)
	def right_click_up(self,event):
		overlapping = set(
			self.canvas.find_overlapping(
				event.x,
				event.y,
				event.x,
				event.y,
			)
		)
		elements = set()
		for eid in overlapping:
			attrs = self.get_attributes(eid)
			if 'type' not in attrs:
				continue
			if 'parent' in attrs:
				atr = self.get_attributes(attrs['parent'])
				if 'type' in atr and atr['type'] == 'element':
					elements.add(attrs['parent'])
			elif attrs['type'] == 'element':
				elements.add(eid)
		self.tooltip.delete(0)
		add_tooltip = tk.Menu(
			self.tooltip,
			tearoff = 0,
		)
		if len(overlapping) == 0:
			add_tooltip.add_command(
				label = 'Block',
			)
			add_tooltip.add_command(
				label = 'Line',
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
			print('empty')
		else:
			eid = list(elements)[0]
			attrs = self.get_attributes(eid)
			match attrs['element_type']:
				case 'block':
					print('block')
					add_tooltip.add_command(
						label = 'Attribute',
					)
				case _:
					raise TypeError('Invalid element_type: ' + str(attrs['element_type']))
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
		self.tooltip.tk_popup(
			event.x_root - 10,
			event.y_root - 10
		)
		self.tooltip.focus_set()
	def place_rectangle(self,eid : int,x1 : int, y1 : int,x2 : int,y2 : int):
		attrs = self.get_attributes(eid)
		(minwidth,minheight) = (attrs['minwidth'],attrs['minheight'])
		(width,height) = (
			x2 - x1,
			y2 - y1
		)
		(xa,ya,xb,yb) = self.get_grid_coords(
			*self.canvas.coords(eid)
		)
		if width < minwidth:
			if xa != x1:
				x1 = x2 - minwidth
			elif xb != x2:
				x2 = x1 + minwidth
		if height < minheight:
			if ya != y1:
				y1 = y2 - minheight
			elif yb != y2:
				y2 = y1 + minheight
		(x1,y1,x2,y2) = self.get_true_coords(x1,y1,x2,y2)
		self.canvas.coords(
			eid,
			x1,
			y1,
			x2,
			y2
		)
		for element in self.get_children(eid):
			attrs = self.get_attributes(element)
			match attrs['type']:
				case 'border':
					match attrs['border_type']:
						case 'corner':
							if attrs['top']:
								if attrs['left']:
									self.canvas.coords(
										element,
										x1 - 15,
										y1 - 15,
										x1 - 1,
										y1 - 1,
									)
								else:
									self.canvas.coords(
										element,
										x2 + 1,
										y1 - 15,
										x2 + 15,
										y1 - 1,
									)
							else:
								if attrs['left']:
									self.canvas.coords(
										element,
										x1 - 15,
										y2 + 1,
										x1 - 1,
										y2 + 15,
									)
								else:
									self.canvas.coords(
										element,
										x2 + 1,
										y2 + 1,
										x2 + 15,
										y2 + 15,
									)
						case 'edge':
							match attrs['edge_type']:
								case 'left':
									self.canvas.coords(
										element,
										x1 - 15,
										y1,
										x1 - 1,
										y2,
									)
								case 'right':
									self.canvas.coords(
										element,
										x2 + 1,
										y1,
										x2 + 15,
										y2,
									)
								case 'top':
									self.canvas.coords(
										element,
										x1,
										y1 - 15,
										x2,
										y1 - 1,
									)
								case 'bottom':
									self.canvas.coords(
										element,
										x1,
										y2 + 1,
										x2,
										y2 + 15,
									)
								case _:
									raise TypeError
						case _:
							raise TypeError
				case 'text':
					self.canvas.coords(
						element,
						(x1 + x2) / 2,
						(y1 + y2) / 2,
					)
				case _:
					raise TypeError
	def left_click_down(self,event):
		# vals = elements being clicked
		vals = set(
			self.canvas.find_overlapping(
				event.x,
				event.y,
				event.x,
				event.y
			)
		) & (
			set(
				self.canvas.find_withtag('type="element"')
			) | set(
				self.canvas.find_withtag('type="border"')
			)
		)
		if len(vals) == 0:
			# if no elements being clicked
			'''
			self.canvas.itemconfigure(
				'element',
				outline = '',
				width = 1,
			)
			eid = self.canvas.create_rectangle(
				event.x,
				event.y,
				event.x,
				event.y,
				outline = 'black',
				dash = (2,2),
				tags = ('select_area'),
			)
			self.attributes['select_area_source'] = (event.x,event.y)
			'''
			pass
		else:
			# if element being clicked
			eid = list(vals)[0]
			tags = self.canvas.gettags(eid)
			self.canvas.addtag_withtag('selected=true',eid)
			self.attributes['selected_element_cursor_source'] = (event.x,event.y)
			match self.canvas.type(eid):
				case 'rectangle':
					attrs = self.get_attributes(eid)
					if 'parent' in attrs:
						self.attributes['selected_element_source_coords'] = self.get_grid_coords(
							*self.canvas.coords(attrs['parent'])
						)
					else:
						self.attributes['selected_element_source_coords'] = self.get_grid_coords(
							*self.canvas.coords(eid)
						)
				case _:
					raise TypeError
	def left_click_move(self,event):
		# vals = elements being clicked
		vals = self.canvas.find_withtag('selected=true')
		if len(vals) == 0:
			'''
			(x1,y1) = self.attributes['select_area_source']
			if event.x < x1:
				if x1 > event.x and (y1 - event.y)/(x1 - event.x) < 0:
					(x1,y1,x2,y2) = (event.x,event.y,x1,y1)
				else:
					(x1,y1,x2,y2) = (event.x,y1,x1,event.y)
			else:
				if event.x > x1 and (event.y - y1)/(event.x - x1) < 0:
					(x1,y1,x2,y2) = (x1,y1,event.x,event.y)
				else:
					(x1,y1,x2,y2) = (x1,event.y,event.x,y1)
			self.canvas.coords(
				'select_area',
				x1,
				y1,
				x2,
				y2,
			)
			self.canvas.itemconfigure(
				'select_area',
				state = 'normal',
			)
			xmin = min(x1,x2)
			xmax = max(x1,x2)
			ymin = min(y1,y2)
			ymax = max(y1,y2)
			for element in self.canvas.find_withtag('element'):
				match self.canvas.type(element):
					case 'rectangle':
						(xa,ya,xb,yb) = self.canvas.coords(element)
						points = {
							(xa,ya),
							(xa,yb),
							(xb,ya),
							(xb,yb),
						}
						if any(
							(
								x >= xmin and
								x <= xmax and
								y >= ymin and
								y <= ymax
							) for x,y in points
						):
							self.canvas.itemconfigure(
								element,
								outline = 'black',
								width = 5,
							)
						else:
							self.canvas.itemconfigure(
								element,
								activeoutline = 'black',
								activewidth = 5,
							)
					case _:
						raise TypeError
			'''
			pass
		else:
			(cx1,cy1) = self.attributes['selected_element_cursor_source']
			(cx2,cy2) = (event.x,event.y)
			true_vector = (cx2 - cx1,cy2 - cy1)
			grid_vector = self.get_grid_coords(*true_vector)
			for val in vals:
				match self.canvas.type(val):
					case 'rectangle':
						attrs = self.get_attributes(val)
						(x1,y1,x2,y2) = self.attributes['selected_element_source_coords']
						match attrs['type']:
							case 'element':
								self.place_rectangle(
									val,
									x1 + grid_vector[0],
									y1 + grid_vector[1],
									x2 + grid_vector[0],
									y2 + grid_vector[1],
								)
							case 'border':
								match attrs['border_type']:
									case 'edge':
										match attrs['edge_type']:
											case 'top':
												self.place_rectangle(
													attrs['parent'],
													x1,
													y1 + grid_vector[1],
													x2,
													y2,
												)
											case 'bottom':
												self.place_rectangle(
													attrs['parent'],
													x1,
													y1,
													x2,
													y2 + grid_vector[1],
												)
											case 'left':
												self.place_rectangle(
													attrs['parent'],
													x1 + grid_vector[0],
													y1,
													x2,
													y2,
												)
											case 'right':
												self.place_rectangle(
													attrs['parent'],
													x1,
													y1,
													x2 + grid_vector[0],
													y2,
												)
											case _:
												raise TypeError
									case 'corner':
										if attrs['top']:
											if attrs['left']:
												self.place_rectangle(
													attrs['parent'],
													x1 + grid_vector[0],
													y1 + grid_vector[1],
													x2,
													y2,
												)
											else:
												self.place_rectangle(
													attrs['parent'],
													x1,
													y1 + grid_vector[1],
													x2 + grid_vector[0],
													y2,
												)
										else:
											if attrs['left']:
												self.place_rectangle(
													attrs['parent'],
													x1 + grid_vector[0],
													y1,
													x2,
													y2 + grid_vector[1],
												)
											else:
												self.place_rectangle(
													attrs['parent'],
													x1,
													y1,
													x2 + grid_vector[0],
													y2 + grid_vector[1],
												)
									case _:
										raise TypeError
							case _:
								raise TypeError
					case _:
						raise TypeError
	def left_click_up(self,event):
		vals = self.canvas.find_withtag('selected=true')
		if len(vals) == 0:
			#self.canvas.delete(self.canvas.find_withtag('selected_area')[0])
			pass
		else:
			self.canvas.dtag('selected=true','selected=true')
			del self.attributes['selected_element_cursor_source']
			del self.attributes['selected_element_source_coords']
	def double_left_click(self,event):
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
			match self.canvas.type(parent):
				case 'rectangle':
					(x1,y1,x2,y2) = self.canvas.coords(parent)
					xlen = x2 - x1
				case _:
					raise TypeError('Invalid canvas type: ' + str(self.canvas.type(parent)))
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
				tags = ('type="entry"','parent=' + str(parent)),
				width = round(xlen // 3),
			)
			entry_box.insert(0,text)
			entry_box.bind(
				'<Return>',
				self.finish_entry,
			)
			self.attributes['entries'][canvas_window] = entry_box
	def enter_element(self,event):
		self.canvas.config(cursor = 'fleur')

		for eid in self.canvas.find_overlapping(
			event.x,
			event.y,
			event.x,
			event.y
		):
			print('ENTER')
			self.canvas.itemconfigure(
				'parent' + str(eid),
				state = 'normal',
			)
	def leave_element(self,event):
		self.canvas.config(cursor = 'left_ptr')

		for eid in self.canvas.find_overlapping(
			event.x,
			event.y,
			event.x,
			event.y
		):
			print('LEAVE')
			self.canvas.itemconfigure(
				'parent' + str(eid),
				state = 'hidden',
			)
	def mouse_move(self,event):
		overlapping = set(
			self.canvas.find_overlapping(
				event.x,
				event.y,
				event.x,
				event.y
			)
		)
		found = False
		elements = {}
		for eid in overlapping:
			elements[eid] = self.get_attributes(eid)
			if 'type' in elements[eid]:
				found = True
		if not found:
			self.canvas.config(cursor = 'left_ptr')
		else:
			if any(
				'type' in attrs and attrs['type'] == 'text' for attrs in elements.values()
			):
				self.canvas.config(cursor = 'xterm')
			else:
				vid = None
				for eid,attrs in elements.items():
					if 'type' in attrs and attrs['type'] == 'border':
						vid = eid
						break
				if vid is None:
					self.canvas.config(cursor = 'fleur')
				else:
					match elements[vid]['border_type']:
						case 'edge':
							match elements[vid]['edge_type']:
								case 'left':
									self.canvas.config(cursor = 'left_side')
								case 'right':
									self.canvas.config(cursor = 'right_side')
								case 'top':
									self.canvas.config(cursor = 'top_side')
								case 'bottom':
									self.canvas.config(cursor = 'bottom_side')
						case 'corner':
							if elements[vid]['top']:
								if elements[vid]['left']:
									self.canvas.config(cursor = 'top_left_corner')
								else:
									self.canvas.config(cursor = 'top_right_corner')
							else:
								if elements[vid]['left']:
									self.canvas.config(cursor = 'bottom_left_corner')
								else:
									self.canvas.config(cursor = 'bottom_right_corner')
						case _:
							raise TypeError('Invalid border_type: ' + str(elements[vid]['type']))
		elements = {
			attrs['parent'] for attrs in elements.values() if 'parent' in attrs
		} | {
			eid for eid,attrs in elements.items() if 'type' in attrs and attrs['type'] == 'element'
		}
		shown_borders = set()
		hidden_borders = set()
		all_borders = set(
			self.canvas.find_withtag('type="border"')
		)
		for eid in elements:
			shown_borders |= set(
				self.canvas.find_withtag('parent=' + str(eid))
			)
		shown_borders &= all_borders
		hidden_borders = set(
			self.canvas.find_withtag('type="border"')
		) - shown_borders
		for border in shown_borders:
			attrs = self.get_attributes(border)
			match attrs['border_type']:
				case 'edge':
					self.canvas.itemconfigure(
						border,
						fill = 'yellow',
						outline = 'black',
					)
				case 'corner':
					self.canvas.itemconfigure(
						border,
						fill = 'white',
						outline = 'black',
					)
				case _:
					raise TypeError
		for border in hidden_borders:
			self.canvas.itemconfigure(
				border,
				fill = '',
				outline = '',
			)
	def finish_entry(self,event):
		wid = None
		for window,entry in self.attributes['entries'].items():
			if str(entry) == str(event.widget):
				wid = window
				break
		if wid is None:
			raise TypeError('No window found for entry')
		text = event.widget.get()
		coords = self.canvas.coords(wid)
		attrs = self.get_attributes(wid)
		parent = attrs['parent']
		match self.canvas.type(parent):
			case 'rectangle':
				(x1,x2,y1,y2) = self.canvas.coords(parent)
				xlen = x2 - x1
			case _:
				raise TypeError
		event.widget.destroy()
		self.canvas.delete(wid)
		self.canvas.create_text(
			coords[0],
			coords[1],
			text = text,
			tags = ('type="text"','parent=' + str(parent)),
		)