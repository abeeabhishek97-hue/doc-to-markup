Layout
Detection
Module
1.
refine_classification()
Takes
raw
LayoutLMv3
output

and

applies

rule-based

corrections
to
fix
common
misclassifications
such

- as

small

headings
labelled

### as

paragraphs,

or

single-column

tables
labelled
as
lists.
def
refine

- classification(regions,

ocr_boxes):

for

region

in

regions:

text

region.get('text',
bbox

region['bbox']
height

- bbox[3]
- bbox[1]

<!-- table: missing headers/rows -->
> Short

tall
lines

are
likely
headings

if

region['class']

- 'paragraph':

if
height

<!-- table: missing headers/rows -->

40

and

len(text.split())

10:

- region['class']
- 'heading'

Monospace

regions

are
code

blocks

- if
- region['class']
- 'paragraph':
- if
- is_monospace

(region):

- Single-column
- tables
- misread

#### as

- lists
- if
- region['class']
- 'list':

if
has_grid_structure
(ocr_boxes,

- bbox):
- region['class']
- 'table'

return
regions

2.

# is_monospace()

Checks

whether

character

bounding

<!-- table: missing headers/rows -->
> boxes
<!-- table: missing headers/rows -->
> within

### a

region
have
roughly
equal

widths

the

hallmark

of
a

monospace

or

code
font.

def
is_monospace
(region)

widths
[b[2]

b[0]

<!-- table: missing headers/rows -->
> for

b

in

region.get
('char_boxes',

if
not

widths:
return
False
Tight
tolerance:
all
chars
nearly
the

<!-- table: missing headers/rows -->
> same

width
return

- (max(widths)

min(widths))
3

3.
has_grid_structure()

Detects
whether

OCR
boxes
within

a

bounding
region
are

arranged
in
two

or

### more

vertical
columns,
indicating

a

<!-- table: missing headers/rows -->
> table

- rather

than

- a

list.

def

- has_grid_structure
- (ocr_boxes,
- bbox):

contained

[b

for

- b
- in
- ocr_boxes

if

## is_inside

(b,

bbox)]
x_positions
sorted(

set

- (round(b[0]

10)

10

<!-- table: missing headers/rows -->
> for

- b
- in

contained)
return

len(x_positions)

2

- at
- least

2

columns

4.
Wiring

- into
- run_layout_inference()

Call

refine_classification()

at
the
end
of
the

existing
inference
function,

- just

before

returning
results.
def

- run_layout_inference
- (ocr_output)

existing
Day

4

LayoutLMv3
code

regions

model.predict

- (ocr_output)

Day

5:

apply
rule-based
corrections

regions

refine_classification(regions,

ocr_output)

return

regions