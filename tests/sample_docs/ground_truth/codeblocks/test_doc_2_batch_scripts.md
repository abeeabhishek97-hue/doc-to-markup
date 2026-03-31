Batch

<!-- table: missing headers/rows -->
> Testing

and

Visualisation
Scripts
1.
batch_test_layout.py
Loops
over
every
PDF
in
tests/sample_docs/,
runs
the
full
pipeline
(ingest
OCR

layout),

and

saves
a

JSON

result

to

tests/layout_results/.

Run

this
after

any

change
to
layout.py.
scripts/batch_test_layout.py
import
json

from

pathlib
import
Path

from

src.ingestion
import

- load_document

from

src.ocr
import
extract_text_boxes

from

src.layout
import

- run_layout_inference
- TEST_DOCS
- Path('tests/sample_docs')
- RESULTS_OUT

<!-- table: missing headers/rows -->
> Path('tests/layout_results')

- RESULTS_OUT

.mkdir

- (exist_ok=True)

for

doc_path

- in
- TEST_DOCS.rglob('*.pdf'):

image_tensors

- load_document
- (doc_path)

ocr_output

- extract_text_boxes
- (image_tensors)
- layout_result
- run_layout_inference
- (ocr_output)
- out_file
- RESULTS_OUT

with

- open(out_file,
- 'w')
- as

f:

- json.dump
- (layout_result,

f,

indent=2)
print

(f'Done:

- {doc_path.name}')

2.

visualize_layout.py
Reads
a
page
image

and
its

# corresponding

### JSON

result,
then
draws
coloured
bounding
boxes
using
OpenCV

so

you
can

visually

## spot

misclassified

regions

at

#### a

glance.

- scripts/visualize_layout.py

import
json,

cv2

from

pathlib
import

<!-- table: missing headers/rows -->
> Path

COLORS
‘heading'
(255,
0,

- 0),
- ‘paragraph':

0,

200,

- 0),
- (0,
- 0,

<!-- table: missing headers/rows -->
> 255,

'table’

(255,
165,

- 0),

(128,

- 0,

128),

def
draw_layout

(image_path,

layout_json_path):
img

cv2.imread(str(image_path))
with

open(layout_json_path)

<!-- table: missing headers/rows -->
> as

f:

regions
json.load(f)

for

region

in

regions:
x1,
yl,

- x2,
- y2
- region['bbox']
- label
- region['class']

color

COLORS.get

- (label,
- (200,
- 200,
- 200))
- cv2.rectangle(img,
- (x1,yl),
- (x2,y2),

color,

2)
cv2.putText
(img,

- label,
- (x1,
- y1-5),
- cv2.FONT_HERSHEY_SIMPLEX,

0.5,

color,

1)

- out

f£'debug_{Path

- (image_path)

.stem}.png"

cv2.imwrite
(out,

img)

print

(f'Saved:
{out}')
3.

Running

the

scripts
Run
both
scripts
from
the
project
root.

Always

run

batch_test

first
to
regenerate
JSON
files,
then
visualize
to
inspect
results.
Regenerate
layout

<!-- table: missing headers/rows -->
> JSON

for

all

<!-- table: missing headers/rows -->
> docs

python
scripts/batch_test_layout.py
Visualise
a
specific
result
python

- scripts/visualize_layout.py
- Commit

when

satisfied
git

add

src/layout.py

- scripts/

tests/

git

commit

-m
'Day
5:

layout

<!-- table: missing headers/rows -->
> testing,

fixed

<!-- table: missing headers/rows -->
> edge

cases
git

<!-- table: missing headers/rows -->
> push