#!/usr/bin/env python3

import argparse
import math

from svgwrite.container import Style
from svgwrite.drawing import Drawing

class DocumentProperties:
	def __init__(self, width, height):
		self.width = width
		self.height = height

	@classmethod
	def in_inches(cls, width_in_inches, height_in_inches, dpi):
		return cls(width_in_inches * dpi, height_in_inches  * dpi)

class HexagonProperties:
	def __init__(self, height):
		self.height = height
		self.edge = self.height / math.sqrt(3)
		self.width = self.edge * 2

	@classmethod
	def in_inches(cls, height_in_inches, dpi):
		return cls(height_in_inches * dpi)

class Hexagon:
	def __init__(self, center, properties):
		self.verticies = (
			(center[0] - properties.edge/2, center[1] - properties.height/2),
			(center[0] + properties.edge/2, center[1] - properties.height/2),
			(center[0] + properties.width/2, center[1]),
			(center[0] + properties.edge/2, center[1] + properties.height/2),
			(center[0] - properties.edge/2, center[1] + properties.height/2),
			(center[0] - properties.width/2, center[1])
		)

class HexagonDecorator:
	def draw(self, drawing, hexagon):
		polygon = drawing.polygon(hexagon.verticies)
		drawing.add(polygon)

class CrowsFootDecorator:
	def __init__(self, hexagon_properties):
		dash = hexagon_properties.edge * .25
		gap = hexagon_properties.edge - dash*2
		self._dash_array = '{},{},{}'.format(dash,gap,dash)

	def draw(self, drawing, hexagon):
		for index, vertex in enumerate(hexagon.verticies):
			prev_vertex = hexagon.verticies[int((index-1)%6)]
			line = drawing.line(start=vertex, end=prev_vertex)
			line['stroke-dasharray'] = self._dash_array
			drawing.add(line)

class HexagonalGrid:
	def __init__(self, document_properties, hexagon_properties, decorator):
		self._document_properties = document_properties
		self._hexagon_properties = hexagon_properties
		self._decorator = decorator

	def _columns(self):
		column_offset = self._hexagon_properties.width/2 + self._hexagon_properties.edge/2
		count = math.ceil(self._document_properties.width / column_offset)
		start = column_offset/2 - (count * column_offset - self._document_properties.width)/2

		columns = []
		for index in range(count):
			columns.append(start + index * column_offset)
		return columns

	def _rows(self, column):
		count = math.ceil(self._document_properties.height / self._hexagon_properties.height) + int(column % 2)
		start = self._hexagon_properties.height/2 - (count * self._hexagon_properties.height - self._document_properties.height)/2

		rows = []
		for index in range(count):
			rows.append(start + index * self._hexagon_properties.height)
		return rows

	def draw(self):
		drawing = Drawing(size=(self._document_properties.width, self._document_properties.height))
		drawing.add(Style(content='* { fill: none; stroke: #000000; stroke-width: 1 }'))

		for column, x in enumerate(self._columns()):
			for y in self._rows(column):
				hex = Hexagon((x, y), self._hexagon_properties)
				self._decorator.draw(drawing, hex)

		return drawing

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('width', help='document width', type=float)
	parser.add_argument('height', help='document height', type=float)
	parser.add_argument('hex_size', help='hex size, from flat to flat', type=float)
	parser.add_argument('-d', '--dpi', help='set output dpi and interpret dimensions as inches', type=float, default=1)
	parser.add_argument('-s', '--style', help='set the drawing style', default='hexes', choices=['hexes', 'crowsfeet'])
	parser.add_argument('-o', '--output', help='write to OUTPUT instead of stdout')
	args = parser.parse_args()

	document_properties = DocumentProperties.in_inches(args.width, args.height, args.dpi)
	hexagon_properties = HexagonProperties.in_inches(args.hex_size, args.dpi)
	decorator = HexagonDecorator() if args.style == 'hexes' else CrowsFootDecorator(hexagon_properties)
	drawing = HexagonalGrid(document_properties, hexagon_properties, decorator).draw()

	if args.output:
		drawing.saveas(args.output, pretty=True)
	else:
		print(drawing.tostring())

if __name__ == '__main__':
	main()
