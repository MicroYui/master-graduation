"""Crop unchanged vector panels from the published LEADR paper."""
from pathlib import Path
from copy import deepcopy
from pypdf import PdfReader, PdfWriter
ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT.parent / 'first problem.pdf'
reader = PdfReader(SOURCE)
# Pixel coordinates measured on Poppler's 110 dpi preview; charts only.
panels = {
 'num': (11, [(72,78,320,205),(342,77,584,205),(72,231,320,353),(342,231,584,353)]),
 'com': (12, [(84,77,342,205),(353,77,602,205),(84,233,342,355),(353,233,602,355)]),
 'speed':(13,[(65,76,320,205),(336,77,587,205),(65,233,320,355),(336,233,587,355)]),
}
for group, (page_number, boxes) in panels.items():
 for suffix, (x0,y0,x1,y1) in zip('abcd', boxes):
  page=deepcopy(reader.pages[page_number]); scale=110/72; height=float(page.mediabox.top)
  top_pad = 3 if suffix in 'ab' else 0
  if suffix in 'cd': y0 = max(y0, 234)
  rect=((x0-10)/scale,height-(y1+3)/scale,(x1+3)/scale,height-(y0-top_pad)/scale)
  page.cropbox.lower_left=rect[:2]; page.cropbox.upper_right=rect[2:]
  page.mediabox.lower_left=rect[:2]; page.mediabox.upper_right=rect[2:]
  writer=PdfWriter(); writer.add_page(page)
  writer.add_metadata({'/Title':f'Original LEADR {group} panel {suffix}', '/Subject':'Unchanged vector crop from the published study'})
  out=Path(__file__).parent/f'{group}_{suffix}.pdf'
  with out.open('wb') as f: writer.write(f)
