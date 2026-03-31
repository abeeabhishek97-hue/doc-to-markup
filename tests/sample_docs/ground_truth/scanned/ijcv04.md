Distinctive
Image
Features

from
Scale-Invariant

Keypoints

<!-- table: missing headers/rows -->
> David

G.

Lowe

<!-- table: missing headers/rows -->
> Computer

Science
Department

University

<!-- table: missing headers/rows -->
> of

British

Columbia
Vancouver,

B.C.,

Canada
lowe@cs.ubc.ca

January
5,

<!-- table: missing headers/rows -->
> 2004

Abstract

This

<!-- table: missing headers/rows -->
> paper

presents
a
method

for

extracting
distinctive
invariant
features

from

images

that
can

be

- used

to

perform

reliable

matching
between
different
views

of
an

object

or

scene.

The

<!-- table: missing headers/rows -->
> features

are

invariant

#### to

image

#### scale

and

rotation,

and

are

<!-- table: missing headers/rows -->
> shown

- to

provide
robust
matching

across

- a

#### a

#### substantial

#### range

of

affine
dis- tortion,
- change

in
3D

viewpoint,
addition

<!-- table: missing headers/rows -->
> of

noise,

and

change

in

illumination.

The

<!-- table: missing headers/rows -->
> features

are
highly

distinctive,

- in

the

<!-- table: missing headers/rows -->
> sense

that

- a

single

<!-- table: missing headers/rows -->
> feature

can

be

cor- rectly
- matched

<!-- table: missing headers/rows -->
> with

- high

probability

against

- a
- large

database

- of

features

from
many

<!-- table: missing headers/rows -->
> images.

- This

<!-- table: missing headers/rows -->
> paper

- also

<!-- table: missing headers/rows -->
> describes

#### an

approach

#### to

- using

#### these

features

for

object

recognition.

The

- recognition

proceeds

### by

matching
individual
fea- tures
- to
- a

database

- of
- features

from
known
objects

<!-- table: missing headers/rows -->
> using

#### a

fast

nearest-neighbor
algorithm,

- followed

by

- a

<!-- table: missing headers/rows -->
> Hough

transform

to

identify

clusters

## belonging

to

a
single
object,

and

finally

<!-- table: missing headers/rows -->
> performing

verification

- through

least-squares

solution

for

consistent

pose
parameters.

- This
- approach

#### to

recognition

- can

robustly
identify
objects

- among

clutter

and

occlusion
while

achieving

- near

real-time

performance.

Accepted
for

publication
in
the

International

Journal

of

Computer

Vision,
2004.

1

Introduction
Image
matching
is
a
fundamental

<!-- table: missing headers/rows -->
> aspect
<!-- table: missing headers/rows -->
> of

#### many

problems
in
computer
vision,
including
object
or

#### scene

recognition,
solving
for
3D
structure
from
multiple
images,
stereo
correspondence,

and

motion
tracking.

<!-- table: missing headers/rows -->
> This
<!-- table: missing headers/rows -->
> paper

describes
image
features

that

have
many
properties

that

make
them
suitable

for

matching

differing

images

of

#### an

object

#### or

#### scene.

The

features

are

invariant
to
image

scaling

and

rotation,

and

partially

invariant

#### to

change

in

illumination

and

3D

camera

viewpoint.

<!-- table: missing headers/rows -->
> They

- are

<!-- table: missing headers/rows -->
> well

localized

- in

both

the
spatial
and
frequency

domains,
reducing
the
probability

of

disruption

by

occlusion,
clutter,
or
noise.

- Large

numbers

- of

features
can

- be

extracted
from
typical

<!-- table: missing headers/rows -->
> images
<!-- table: missing headers/rows -->
> with

efficient
algorithms.

<!-- table: missing headers/rows -->
> In

addition,
the
features
are
highly
distinctive,
which
allows

- a
- single

<!-- table: missing headers/rows -->
> feature

- to

be
correctly
matched
with
high
probability
against
a

- large

database

- of

features,
providing

- a

basis
for
object

#### and

#### scene

recognition.

The

cost

of

extracting

these

<!-- table: missing headers/rows -->
> features

is

minimized

by

taking
a

cascade

filtering
approach,

in

which
the
more

<!-- table: missing headers/rows -->
> expensive

operations

are

applied
only

#### at

locations

that

pass

#### an

initial
test.

Following
are
the

<!-- table: missing headers/rows -->
> major
<!-- table: missing headers/rows -->
> stages

of

computation

- used

to

generate

the
set

of

image
features:

1.

Scale-space
extrema

detection:

The
first

<!-- table: missing headers/rows -->
> stage

of

computation
searches
over
all

scales

and

<!-- table: missing headers/rows -->
> image

locations.

It

is

<!-- table: missing headers/rows -->
> implemented

efficiently

by

using
a
difference-of-Gaus
function

to

identify
potential
interest
points

- that

are

invariant

#### to

scale

and

orientation.
an

- 2.

Keypoint
localization:

- At
- each

candidate

location,
a

detailed

model

is
fit

to

determine

- location

and

- scale.
- Keypoints
- are
- selected
- based
- on

measures

- of

#### their

stability.

3.

Orientation

assignment:

One

or

#### more

orientations

are

assigned

to
each

keypoint
location

- based

on

local

<!-- table: missing headers/rows -->
> image

gradient
directions.

All
future

operations

are

performed

- on

image

- data

that

- has

#### been

transformed

#### relative

to
the
assigned

orientation,

#### scale,

and

- location

for

- each

<!-- table: missing headers/rows -->
> feature,

thereby

- providing

invariance

#### to

#### these

transformations.

4.

- Keypoint

descriptor:

- The
- local

<!-- table: missing headers/rows -->
> image

gradients

are

- measured

at
the

selected

scale

- in
- the

region
around

- each
- keypoint.
- These
- are

transformed

#### into

#### a

representation

that

allows

for

- significant
- levels
- of
- local

shape

distortion

#### and

### change

#### in

illumination.

This

approach

- has
- been

<!-- table: missing headers/rows -->
> named

the
Scale

Invariant

Feature

Transform

(SIFT),

#### as

#### it

transforms
image

- data
- into

scale-invariant

coordinates

#### relative

- to

local

#### features.

An

- important
- aspect

of

- this
- approach
- is
- that
- it

generates

- large
- numbers
- of

features

- that

densely

cover

- the

<!-- table: missing headers/rows -->
> image

- over

the
full

- range
- of
- scales

#### and

locations.

#### A

typical

image

- of

size

<!-- table: missing headers/rows -->
> 500x500
<!-- table: missing headers/rows -->
> pixels

will

- give
- rise

to
about
2000
stable

<!-- table: missing headers/rows -->
> features

(although

#### this

- number

depends

- on
- both

<!-- table: missing headers/rows -->
> image

content

and

- choices

for

- various

parameters).
The
quantity

- of

features

is
particimage,
many
features
from
the
background
will
not
have

#### any

correct
match
in
the
database,
giving
rise
to
many

false

matches

- in

addition
to
the
correct
ones.
The
correct
matches
can
be
filtered
from
the
full

set

of

matches

by

identifying
subsets

of

keypoints

that

agree
on
the
object

and

its
location,
scale,

and

orientation

- in

the
new
image.

The

probability

that

several
features
will

- agree

on
these

parameters

by

chance

is

much
lower

than

the
probability

that
any

individual

<!-- table: missing headers/rows -->
> feature

match

will

#### be

- in

error.

The

determination

of

#### these

consistent
clusters

can
be

performed
rapidly

by

using

an

efficient

<!-- table: missing headers/rows -->
> hash
<!-- table: missing headers/rows -->
> table

implementation

of

the
generalized
Hough
transform.

Each

cluster

of
3

- or
- more

<!-- table: missing headers/rows -->
> features

- that
- agree
- on

#### an

object

and

#### its

pose

is

then
subject
to
further
detailed
verification.

- First,
- a
- least-squared

estimate

is

- made

for
an
affine
approxi- mation

to
the

object

<!-- table: missing headers/rows -->
> pose.

- Any
- other

<!-- table: missing headers/rows -->
> image

- features

consistent
with

#### this

pose
are
identified,

and

outliers
are

discarded.

- Finally,
- a

detailed
computation

is

- made

of

the

probability

that

a
particular

- set

of

features
indicates

- the

presence

of

#### an

object,
given
the

accuracy

of

fit

and

- number

of

probable

false

matches.

<!-- table: missing headers/rows -->
> Object

matches

- that

<!-- table: missing headers/rows -->
> pass

all

#### these

tests
can
be
identified

as

correct

with

high

confidence.

2
Related

research

The

development

of

<!-- table: missing headers/rows -->
> image

matching

by

- using
- a

set

of

local

interest
points

can

be
traced

back

to
the
work

of

Moravec

(1981)
on

<!-- table: missing headers/rows -->
> stereo

matching
using

#### a

corner
detector.

The

Moravec

detector

was

improved

by

<!-- table: missing headers/rows -->
> Harris

and

Stephens

(1988)

to

make

it

#### more

repeatable
under

small

image
variations

and

- near

<!-- table: missing headers/rows -->
> edges.
<!-- table: missing headers/rows -->
> Harris

also

<!-- table: missing headers/rows -->
> showed

its
value

for

efficient

motion

tracking

and

3D
structure

from

<!-- table: missing headers/rows -->
> motion

recovery

(Harris,

1992),

and

the
Harris

corner
detector
has

- since
- been

widely

- used

for

- many
- other

<!-- table: missing headers/rows -->
> image

matching

<!-- table: missing headers/rows -->
> tasks.

While

#### these

<!-- table: missing headers/rows -->
> feature

detectors

are
usually
called

<!-- table: missing headers/rows -->
> corner

detectors,

they
are
not
selecting

### just

corners,

- but
- rather
- any

image
location

that
has

- large

gradients

- in

all

directions

- at

#### a

predetermined

#### scale.

The
initial

applications

- were
- to

#### stereo

- and
- short-range

<!-- table: missing headers/rows -->
> motion

tracking,

but

the
approach

- was
- later
- extended
- to
- more

difficult
problems.

<!-- table: missing headers/rows -->
> Zhang

et

#### al.

<!-- table: missing headers/rows -->
> (1995)

showed

- that

it

was

possible

- to

match

<!-- table: missing headers/rows -->
> Harris

corners

- over
- a
- large

<!-- table: missing headers/rows -->
> image

- range
- by
- using

#### a

correlation
window
around

each

corner

- to
- select
- likely
- matches.

Outliers

- were
- then

removed

### by

solving

for

#### a

fundamental

matrix
describing
the
geometric

- constraints
- between
- the

#### two

views

of

rigid

#### scene

and

removing

- matches
- that
- did
- not
- agree
- with
- the

majority

solution.

At

- the

#### same

time,

#### a

similar

approach

- was

developed

by
Torr

- (1995)
- for
- long-range

motion

matching,

- in

which
geometric

- constraints
- were
- used
- to
- remove

outliers

- for
- rigid

objects

- moving

within
sensitive
to
local
image
distortions
such
as
3D
viewpoint
change.
This
current
paper
provides
amore
in-depth
development

and

analysis

<!-- table: missing headers/rows -->
> of

this
earlier
work,
while
also
presenting
a
number

of

improvements
in
stability

and

<!-- table: missing headers/rows -->
> feature

invariance.
There

is

a
considerable

body

of

previous
research

#### on

identifying
representations

that

are
stable
under
scale
change.

<!-- table: missing headers/rows -->
> Some
<!-- table: missing headers/rows -->
> of

the

first

work
in
this
area
was

### by

Crowley
and
Parker
(1984),
who
developed
a
representation

that

identified
peaks

and

ridges
in
scale
space
and
linked
these
into
a
tree
structure.

<!-- table: missing headers/rows -->
> The

- tree

structure
could
then
be
matched
between
images

with

arbitrary

<!-- table: missing headers/rows -->
> scale

change.

- More
- recent
- work
- on

graph-based
matching

by

Shokoufandeh,
Marsic

and

Dickinson

- (1999)

provides

- more

distinctive

<!-- table: missing headers/rows -->
> feature

descriptors
using
wavelet
coefficients.

The

problem

of

identifying

- an

appropriate

- and

consistent
scale

for

feature
detection

has

- been

studied

- in

depth

by

Lindeberg

(1993,

1994).

He

describes

#### this

#### as

a
problem

of

scale
selection,

and
we

make

use

of

his
results
below.
Recently,

- there
- has

been

- an

impressive
body

- of

work

#### on

extending
local
features
to
be
invariant

to
full

affine
transformations

(Baumberg,

2000;

Tuytelaars

and

Van
Gool,
2000;

Mikolajczyk

and

<!-- table: missing headers/rows -->
> Schmid,

2002;

<!-- table: missing headers/rows -->
> Schaffalitzky

and

Zisserman,

2002;

Brown

and

Lowe,

2002).

This

allows

for

invariant

matching

- to

features

- on
- a

planar

#### surface

under
changes

in

orthographic
3D
projection,

in
most

- cases

by

resampling

the
image

in
a

local

affine

frame.

However,

none
of
these

approaches

are
yet
fully
affine

invariant,

as

they
start
with

initial
feature

<!-- table: missing headers/rows -->
> scales

and

locations
selected

- in
- a

non-affine-invariant
manner
due
to
the

prohibitive
cost

of

exploring

the
full
affine
space.
The

- affine

frames
are
are
also
more

sensitive

to

noise

#### than

those

of
the

scale-invariant

<!-- table: missing headers/rows -->
> features,

so

- in

practice

the

affine
features

have
lower

repeatability

- than

the
scale-invariant

<!-- table: missing headers/rows -->
> features

unless

the

- affine

distortion

is

greater

than
about

a

40
degree
tilt
of
a

- planar

surface

(Mikolajczyk,

2002).

<!-- table: missing headers/rows -->
> Wider

- affine

invariance

may

not

be

important

for

many

applications,

as

training

views

are

- best
- taken
- at
- least

every
30

### degrees

rotation

in

viewpoint

(meaning

that

recognition

is
within
15

<!-- table: missing headers/rows -->
> degrees

of
the
closest

training
view)

in

order

to

capture

non-planar

- changes

and

occlusion

<!-- table: missing headers/rows -->
> effects

for

3D

objects.
‘While
the

method

to

be

- presented
- in
- this

<!-- table: missing headers/rows -->
> paper

is
not
fully

<!-- table: missing headers/rows -->
> affine

invariant,
a

different

approach

is

Pope

and

Lowe

(2000)

<!-- table: missing headers/rows -->
> used

features

<!-- table: missing headers/rows -->
> based

on
the
hierarchical
grouping

of

image
contours,
which

are

particularly
useful
for
objects
lacking
detailed
texture.

The

history

of

research
on
visual
recognition
contains
work
on
a
diverse
set

of

other
image
properties

that

can
be

- used

#### as

feature
measurements.
Carneiro

and

Jepson
(2002)
describe
phase-based
local
features

that

represent
the
phase
rather

than

the
magnitude
of
local
spatial
frequencies,
which

is

likely

to

provide
improved
invariance
to
illumination.
Schiele

and

Crowley

(2000)

- have

proposed

- the

use

of

multidimensional
histograms
summarizing
the
distribution

of

measurements
within

<!-- table: missing headers/rows -->
> image

regions.

#### This

type

- of

feature
may
be
particularly
useful

for

recognition

of

textured
objects

<!-- table: missing headers/rows -->
> with

deformable
shapes.
Basri

and

Jacobs
(1997)

- have

<!-- table: missing headers/rows -->
> demonstrated

- the

value

of

extracting
local
region
boundaries

for

recognition.
Other
useful
properties

to

incorporate

include

color,
motion,
figure-ground
discrimination,
region
shape
descriptors,

and

<!-- table: missing headers/rows -->
> stereo
<!-- table: missing headers/rows -->
> depth

cues.

The

local
feature
approach

can

easily
incorporate
novel

<!-- table: missing headers/rows -->
> feature

- types

because
extra
features

contribute

#### to

robustness
when

they

provide
correct
matches,

but

otherwise
do

little

<!-- table: missing headers/rows -->
> harm

- other

than

their

cost

of

computation.
Therefore,
future
systems

are
likely

to

combine

many

<!-- table: missing headers/rows -->
> feature

- types.

3

Detection

of

scale-space
extrema

As

<!-- table: missing headers/rows -->
> described

in

the
introduction,

we

will
detect

keypoints
using
a

cascade
filtering

approach

that

uses
efficient
algorithms

- to

identify

candidate

locations

that
are

then
examined
in
further
detail.

The
first

<!-- table: missing headers/rows -->
> stage

of

- keypoint

detection

is

- to

identify
locations

#### and

scales

that

can
be

- repeatably

a

invariant

to

s

ned

under
differing

views

of

- the

#### same

object.
Detecting

locations

that

are

e
change

of
the

image

can
be

accomplished

### by

searching

for

stable
features

- across

all

- possible

scales,

- using
- a

continuous
function

- of

#### scale

- known

#### as

scale

#### space

(Witkin,

1983).

It
has
been

- shown

by

Koenderink

(1984)

and
Lindeberg
(1994)

that

under
a

### variety

of

reasonable
assumptions
the

- only
- possible
- scale-space

kernel
is
the
Gaussian
function.
Therefore,

- the
- scale

<!-- table: missing headers/rows -->
> space

of

- an

<!-- table: missing headers/rows -->
> image

is

- defined
- as

#### a

function,
L(z,y,

o),

- that

is

produced

from
the

convolution

of

- a

variable-scale

- Gaussian,

G(z,y,

o),

with

#### an

input

image,
I(z,y):

G(z,y,0)
I(z,y),
where
is
the

convolution

operation

- in

and

y,

and
1
24,2

/952
—(a?+y?)/20°

To

efficiently
detect

- stable
- keypoint
- locations
- in
- scale

#### space,

we

#### have

proposed
(Lowe,
1999)
octave)
/‘KE

Scale

(first

octave)

Difference
of

- Gaussian
- Gaussian

(DOG)
Figure
1:
For
each

octave

of

<!-- table: missing headers/rows -->
> scale
<!-- table: missing headers/rows -->
> space,

the
initial

<!-- table: missing headers/rows -->
> image

is

repeatedly
convolved
with
Gaussians
to
produce

the
set

of

- scale

<!-- table: missing headers/rows -->
> space
<!-- table: missing headers/rows -->
> images
<!-- table: missing headers/rows -->
> shown

- on

the
left.

Adjacent
Gaussian

images

are

subtracted

to

produce

the

difference-of-Gaussian

<!-- table: missing headers/rows -->
> images

- on
- the

<!-- table: missing headers/rows -->
> right.

After

#### each

octave,
the
Gaussian
image

is

<!-- table: missing headers/rows -->
> down-sampled

by

- a

<!-- table: missing headers/rows -->
> factor

of
2,
and

- the

process

repeated.

In

- addition,

the

- difference-of-Gaussian

function

provides
a

close

approximation

to

the

scale-normalized

- Laplacian

of

- Gaussian,
- 0>V2G,

#### as

<!-- table: missing headers/rows -->
> studied

### by

Lindeberg

(1994).

Lindeberg

<!-- table: missing headers/rows -->
> showed

that
the

normalization

of

- the
- Laplacian

with
the
factor

o2

is

required

for

true
scale

invariance.

In

detailed

<!-- table: missing headers/rows -->
> experimental
<!-- table: missing headers/rows -->
> comparisons,

Mikolajczyk

<!-- table: missing headers/rows -->
> (2002)

found
that

the
maxima

and

minima

of
02V2G

produce

- the
- most

<!-- table: missing headers/rows -->
> stable
<!-- table: missing headers/rows -->
> image

features

- compared

to

a

#### range

of

other

- possible

image
functions,

- such
- as

the

gradient,
Hessian,

or

Harris

corner

function.
The
relationship

- between

D
and

- can

be

understood

from
the
heat

diffusion
equation

(parameterized

- in
- terms
- of

o

- rather
- than

the

- more

<!-- table: missing headers/rows -->
> usual

From

this,
we
see
that

- can

be
computed
from
the
finite
difference

approximation

to

/Do,

using
the
difference

of

nearby
scales
at

ko

and

o
ko)

2

and
therefore,
G(x,y,ko)

G(z,y,0)

(k

This

shows

that
when
the

difference-of-Gaussian
function

has

scales
differing

by

a
constant

factor

it

already
incorporates
the

o2

scale
normalization

required

for

the

scale-invariant
Figure
2:
Maxima

and

- minima

of

- the

difference-of-Gaussian
images

are

detected

by

comparing
a

pixel

(marked

<!-- table: missing headers/rows -->
> with

X)

to

its

26
neighbors

- in

3x3

regions
at
the

current

#### and

adjacent
scales
(marked
with
circles).
Laplacian.

The
factor

(k

1)
in
the

equation

is

a

constant

over

all
scales

and

therefore
does

not

influence
extrema

location.

The
approximation

<!-- table: missing headers/rows -->
> error

will
go

to

zero

as

k
goes

to

1,

but

in
practice

we

have

<!-- table: missing headers/rows -->
> found

that

the
approximation

has

almost

no

<!-- table: missing headers/rows -->
> impact

on

the

stability
of
extrema
detection

or

localization

for

even
significant

differences

- in

scale,

such
as
k
V2.

An

efficient
approach

to

construction

of

D(z,y,0)

is

- shown

in

Figure
1.

The

initial
image

is

incrementally
convolved

<!-- table: missing headers/rows -->
> with

Gaussians

- to

produce
images
separated

by

a
constant
factor
k

- in

scale

<!-- table: missing headers/rows -->
> space,

shown

<!-- table: missing headers/rows -->
> stacked

- in

the
left

column.

We

choose
to

divide

each
octave

of

- scale

<!-- table: missing headers/rows -->
> space

(i.e.,

doubling

of

- into
- an

integer
number,

s,

of

intervals,
so
k

We

must

produce
s

3

<!-- table: missing headers/rows -->
> images

- in
- the

stack

of

blurred

images

for

#### each

octave,

so
that

final
extrema
detection
covers

- a

complete
octave.

Adjacent

<!-- table: missing headers/rows -->
> image
<!-- table: missing headers/rows -->
> scales

are
subtracted
to

produce
the
difference-of-Gaussian

<!-- table: missing headers/rows -->
> images
<!-- table: missing headers/rows -->
> shown

- on
- the

<!-- table: missing headers/rows -->
> right.

Once

#### a

complete
octave
has

#### been

processed,

we

- resample

the

- Gaussian

<!-- table: missing headers/rows -->
> image

- that
- has

twice
the

initial
value

of

o

(it

will

be

2
images

from
the

- top

of

the
stack)

by

- taking

every
second
pixel

- in

#### each

row

and

column.

The

accuracy

of

sampling

- relative
- to

o

is
no
different

#### than

for

- the

start

of

- the

previous
octave,

while
computation
is

- greatly
- reduced.

3.1

Local
extrema

detection

In

- order
- to

detect

- the

local

- maxima

and

- minima

of

<!-- table: missing headers/rows -->
> D(z,y,

o),

#### each

sample

point

is

- compared

to
its
eight
neighbors

- in
- the

current

<!-- table: missing headers/rows -->
> image

#### and

#### nine

neighbors

- in
- the

scale

#### above

and

below

(see

Figure

- 2).
- It

is

- selected
- only
- if
- it
- is
- larger
- than

all

- of

#### these

neighbors

or

- smaller

#### than

all
of

them.

The
cost
of
this

check

is

reasonably

- low
- due

to

the
fact
that

most

sample

points
will

be

eliminated

following

- the

first
few

<!-- table: missing headers/rows -->
> checks.

An

- important

<!-- table: missing headers/rows -->
> issue

- is
- to

determine

- the

frequency

of

sampling

- in

the
image

and

scale

domains

that
is

- needed

to

reliably
detect

- the

extrema.
Unfortunately,
it
turns
out

that

there

is

no

minimum
spacing

of

- samples
- that

will

detect

all

extrema,

as
the

extrema
can

be

arbitrarily

close
together.

This

- can
- be
- seen

by

Repeatabilty
100
3500
T
o
80

1

g
3000

E

<!-- table: missing headers/rows -->
> 2500

60

2

2000
40

2

5

1500

Matching

location

and

2

- Nearest

doscriptor
n
database

Total
number

of

keypoints

2

Nearest
descriptor
in
database
0

<!-- table: missing headers/rows -->
> 500

1
2
3
4

5

- 6
- 7

8
T
2

8
4

5
6

7

Number

of

<!-- table: missing headers/rows -->
> scales

- sampled

<!-- table: missing headers/rows -->
> per

octave

Number

- of

scales
sampled
per
octave

Figure

3:

The

- top

line

of

- the
- first

<!-- table: missing headers/rows -->
> graph
<!-- table: missing headers/rows -->
> shows

- the

<!-- table: missing headers/rows -->
> percent
<!-- table: missing headers/rows -->
> of

keypoints

that
are

repeatably
detected
at
the

same

location

and

<!-- table: missing headers/rows -->
> scale

- in

#### a

transformed

<!-- table: missing headers/rows -->
> image

- as
- a

function
of
the

- number

of

scales

sampled
per
octave.

The
lower
line

shows

- the

percent

- of

keypoints

- that

have

#### their

descriptors
correctly
matched
to

- a

large

database.

- The

second

<!-- table: missing headers/rows -->
> graph

shows

- the

total

- number
- of

keypoints
detected
in
a
typical
image

- as
- a

function

of

- the
- number
- of
- scale
- samples.

each
other
near
the
transition.

Therefore,

we

must

<!-- table: missing headers/rows -->
> settle

for

- a

solution

that

trades
off
efficiency

with

completeness.

In
fact,
as

might
be
expected

and

is

- confirmed

by

our
experiments,
extrema

that

are

close

together
are

- quite

unstable

to
small
perturbations

of

the

image.

We
can

determine
the
best
choices
experimentally

by

- studying
- a
- range
- of

sampling

frequencies

and

using
those

that

provide

- the
- most

<!-- table: missing headers/rows -->
> reliable

results

<!-- table: missing headers/rows -->
> under

- a

realistic
simulation

- of
- the

matching
task.

3.2

Frequency

of

- sampling
- in
- scale

The

<!-- table: missing headers/rows -->
> experimental

- determination
- of
- sampling

frequency

that

maximizes
extrema
stability

is

- shown

in
Figures

3
and

- 4.
- These
- figures

(and

- most

#### other

simulations

- in

this
paper)

are

based

on

- a

matching

<!-- table: missing headers/rows -->
> task
<!-- table: missing headers/rows -->
> using

- a

collection

- of

32

real

<!-- table: missing headers/rows -->
> images

- drawn

from

#### a

#### diverse

#### range,

including

outdoor
scenes,

human

<!-- table: missing headers/rows -->
> faces,

aerial

<!-- table: missing headers/rows -->
> photographs,

#### and

industrial

<!-- table: missing headers/rows -->
> images

(the

image
domain

was

- found
- to
- have
- almost

no

- influence
- on
- any
- of
- the

results).

#### Each

<!-- table: missing headers/rows -->
> image

#### was

- then

<!-- table: missing headers/rows -->
> subject

to
a

- range

of

transformations,

- including

rotation,
scaling,

affine
stretch,

### change

in

brightness

and

contrast,

and

- addition
- of

<!-- table: missing headers/rows -->
> image

noise.

- Because
- the

changes

- were

synthetic,
it

was

possible

- to

precisely

predict
where

- each

<!-- table: missing headers/rows -->
> feature

- in
- an

original

<!-- table: missing headers/rows -->
> image

should

appear

- in

the
transformed

<!-- table: missing headers/rows -->
> image,

allowing

for

- measurement
- of
- correct

repeatability

and

positional
accuracy
for
each
feature.

Figure

3

shows

these

simulation

<!-- table: missing headers/rows -->
> results
<!-- table: missing headers/rows -->
> used

#### to

examine

- the

effect

of

varying
the

number

<!-- table: missing headers/rows -->
> les

- per

octave

at
which

- the

<!-- table: missing headers/rows -->
> image

function

mpled
prior

#### to

extrema
detection.
In

this

- case,

each

<!-- table: missing headers/rows -->
> image

was

resampled
following

rotation

### by

#### a

random

angle

and

scaling

by

a
random

<!-- table: missing headers/rows -->
> amount

- between

0.2

of

0.9
times

- the

original

#### size.

Keypoints
from
the
reduced
resolution

<!-- table: missing headers/rows -->
> image

were

- matched

against

- those

#### from

- the

original

<!-- table: missing headers/rows -->
> image

#### so

that

the
scales
100

g

<!-- table: missing headers/rows -->
> 60

3

T

g
40

Matching

location

- and

#### scale

- Nearest

descriptor

- in

database

20

1
1.2
1.4
1.6

1.8

2
Prior
smoothing
for

#### each

octave

(sigma)
Figure

4:

The

- top

line

- in
- the

<!-- table: missing headers/rows -->
> graph

- shows
- the

percent

- of

keypoint
locations

that
are

repeatably
detected
in
a

transformed

<!-- table: missing headers/rows -->
> image

- as
- a

function

<!-- table: missing headers/rows -->
> of

the
prior

<!-- table: missing headers/rows -->
> image

smoothing
for

the

first

level

<!-- table: missing headers/rows -->
> of

each
octave.

The
lower
line

shows

- the

percent

of

descriptors

correctly

- matched

against

a

large

database.

The

- top

<!-- table: missing headers/rows -->
> line

- in
- the

first

<!-- table: missing headers/rows -->
> graph
<!-- table: missing headers/rows -->
> of

Figure

3

<!-- table: missing headers/rows -->
> shows

- the

<!-- table: missing headers/rows -->
> percent

- of

keypoints

- that

are
detected
at
a

matching

location

and

- scale
- in

the
transformed

<!-- table: missing headers/rows -->
> image.
<!-- table: missing headers/rows -->
> For

all
examples

<!-- table: missing headers/rows -->
> in

this
paper,
we
define
a
matching

<!-- table: missing headers/rows -->
> scale

- as
- being

<!-- table: missing headers/rows -->
> within

- a

factor

<!-- table: missing headers/rows -->
> of

/2

of
the

correct
scale,

and

a
matching
location

- as

being

- within

o
pixels,

<!-- table: missing headers/rows -->
> where

o

is
the

- scale

of

the
keypoint

(defined

from

equation

(1)

as
the
standard

deviation

of

the
smallest
Gaussian

- used

in
the

difference-of-Gaussian

function).
The
lower
line

<!-- table: missing headers/rows -->
> on

- this

<!-- table: missing headers/rows -->
> graph

- shows
- the
- number
- of

keypoints

- that

are

correctly

- matched
- to
- a

database

of
40,000

- keypoints

<!-- table: missing headers/rows -->
> using

- the

nearest-neighbor

matching
procedure

to

be

<!-- table: missing headers/rows -->
> described

in
Section
6

(this

- shows
- that

once
the

### keypoint

is

repeatably
located,
it

is

- likely
- to
- be
- useful

for

recognition

- and
- matching

<!-- table: missing headers/rows -->
> tasks).

- As
- this

<!-- table: missing headers/rows -->
> graph

shows,
the
highest

- repeatability

is

obtained

when
sampling

#### 3

- scales

<!-- table: missing headers/rows -->
> per

octave,

and

- this

is
the

- number
- of

scale

- samples
- used

for
all

other

<!-- table: missing headers/rows -->
> experiments

throughout

#### this

#### paper.

It

might

<!-- table: missing headers/rows -->
> seem

- surprising

that

the

- repeatability

does

not

continue
to
improve

as

#### more

- scales

are

- sampled.

The

- reason
- is
- that
- this

results

- in

many

#### more

local

extrema

## being

detected,

but
these

- extrema
- are
- on

#### average

- less
- stable
- and

therefore

are
less

- likely
- to
- be
- detected
- in
- the

transformed

<!-- table: missing headers/rows -->
> image.

- This
- is
- shown
- by
- the

second

<!-- table: missing headers/rows -->
> graph

in
Figure

#### 3,

which

shows

- the
- average
- number
- of
- keypoints
- detected
- and
- correctly
- matched
- in

#### each

image.

- The
- number
- of
- keypoints

rises
with
increased

- sampling
- of
- scales

and

- the

#### total

#### number

of

correct
matches
also

rises.

Since
the

success

of

object

recognition

often

depends

- more

on

- the

quantity

of

correctly

- matched
- keypoints,
- as
- opposed

to

their
percentage

#### correct

matching,

for

#### many

applications
it

will

be

optimal

- to

use

- a

larger

- number
- of
- scale
- samples.
- However,

the

cost

of

computation

ses
with
this

- number,
- so

for
the

<!-- table: missing headers/rows -->
> experiments

- in

#### this

#### paper

we

#### have

chosen
to
use
just
3

mples
per

octave.

To

summarize,

these

<!-- table: missing headers/rows -->
> experiments

show

- that

the
scale-space

difference-of-Gaussian

function

has

3.3
Frequency

of

sampling
in
the

spatial

domain
Just
as
we
determined
the
frequency

of

sampling
per
octave

of

scale

#### space,

so
we
must
determine
the
frequency

of

sampling

- in
- the

<!-- table: missing headers/rows -->
> image

domain
relative

to

the

scale

of

smoothing.

Given

that

extrema
can
be

arbitrarily

close
together,
there
will
be
a
similar
trade-off
between

sampling

frequency

and

rate

of

detection.

Figure

4
shows

#### an

experimental
determination
of
the
amount

of

prior

<!-- table: missing headers/rows -->
> smoothing,

o,

that

is

applied

#### to

each

<!-- table: missing headers/rows -->
> image

level

before

building
the

scale

<!-- table: missing headers/rows -->
> space

representation

<!-- table: missing headers/rows -->
> for

#### an

octave.

- Again,
- the
- top

line

is
the

repeatability

of

keypoint
detection,

and

- the

results

<!-- table: missing headers/rows -->
> show

- that

the

repeatability
continues
to
increase
with
However,
there

is

a
cost
to
using
a

<!-- table: missing headers/rows -->
> large

o

- in

terms

of

efficiency,

- so

we
have
chosen
to
use
0
1.6,
which
provides

- close
- to

optimal
repeatability.

- This

value

is

- used

throughout
this
paper

and
was

- used

for

- the

results

in
Figure

3.
Of

course,

if
we

pre-smooth

the

<!-- table: missing headers/rows -->
> image

before

extrema
detection,
we

are

effectively
discarding
the
highest

spatial

frequencies.

- Therefore,

to
make
full

use

of

the

input,

the
image

can

be
expanded

to

create

- more

sample

points

- than

were

present
in
the
original.
We

double
the
size

of
the

input

<!-- table: missing headers/rows -->
> image

using
linear
interpolation

## prior

#### to

building
the

first

level

of

the

pyramid.
While
the

equivalent
operation

<!-- table: missing headers/rows -->
> could

effectively
have

#### been

performed

by

using
sets

of

subpixel-offset

filters

on

the

original

<!-- table: missing headers/rows -->
> image,

the

image

doubling
leads
to
a

more

efficient
implementation.

We

assume

that

- the

original

<!-- table: missing headers/rows -->
> image

has

a

blur

of

at

least

0
0.5

(the

minimum

- needed

to

prevent

## significant

aliasing),

and
that

therefore
the
doubled

image

has

o

1.0
relative

to

its
new
pixel
spacing.
This

- means

that
little

#### additional

smoothing
is

needed

- prior

to

creation

of

- the

first

octave

of

scale

#### space.

The
image
doubling
increases

the

number

of

stable

- keypoints

by

almost

- a

factor

<!-- table: missing headers/rows -->
> of

4,

but
no

## significant

further

improvements

were

<!-- table: missing headers/rows -->
> found

with

a

larger
expansion

<!-- table: missing headers/rows -->
> factor.

4

Accurate

- keypoint

localization

Once

- a
- keypoint

candidate

- has

#### been

- found
- by
- comparing

#### a

pixel
to

#### its

neighbors,
the

next

<!-- table: missing headers/rows -->
> step

- is
- to

perform

- a

detailed
fit

- to
- the

nearby

- data
- for

location,

#### scale,

and

ratio

of

principal

curvatures.

This

information

- allows
- points
- to

be

rejected

that

#### have

low

contrast

(and

are

- therefore
- sensitive

to

noise)

or

are
poorly

- localized
- along

#### an

### edge.

The
initial

<!-- table: missing headers/rows -->
> implementation

of

- this

approach

(Lowe,

1999)

simply

located
keypoints
at

- the

location

and

- scale
- of
- the

central

- sample

### point.

- However,

recently
Brown
has
developed

- a

method

(Brown

Figure
5:

<!-- table: missing headers/rows -->
> This

figure

shows

the

stages

<!-- table: missing headers/rows -->
> of

- keypoint

selection.
(a)

The

<!-- table: missing headers/rows -->
> 233x189

pixel

original
image.

(b)

The
initial
832

- keypoints
- locations
- at

maxima

<!-- table: missing headers/rows -->
> and

minima

of
the

difference-of-Gaussian
function.

- Keypoints

are

- displayed
- as

vectors

indicating
scale,
orientation,

#### and

location.

(c)

After

applying
a

threshold

on

minimum

contrast,

- 729
- keypoints

remain.

(d)

The
final
536

keypoints

that

remain

following

an

additional
threshold

- on

ratio

of

principal
curvatures.

- As
- suggested

<!-- table: missing headers/rows -->
> by

Brown,
the

<!-- table: missing headers/rows -->
> Hessian

and

derivative

<!-- table: missing headers/rows -->
> of

D

are

approximated

by

using
differences
of

neighboring
sample

- points.
- The

resulting

3x3

linear

system

- can

be
solved
with
minimal
cost.

If

- the

<!-- table: missing headers/rows -->
> offset
<!-- table: missing headers/rows -->
> X

- is
- larger

<!-- table: missing headers/rows -->
> than

- 0.5
- in
- any

dimension,

- then
- it
- means

that

the
extremum

lies

- closer

to
a

different

- sample
- point.
- In
- this
- case,
- the

sample

point

is

changed

and
the

interpolation
performed
instead

about

- that
- point.
- The

final

offset
X

is

- added
- to

the

location

of
its

- sample
- point

to
get

- the

interpolated

estimate

- for
- the

location

of
the

extremum.

The

function

value

- at
- the

extremum,

<!-- table: missing headers/rows -->
> D(X),

is

- useful

for

rejecting
unstable
extrema
with

low

contrast.

This
can
be

- obtained

by

- substituting

equation

(3)

into

(2),

giving
190"

For
the

experiments

in
this

paper,

all

extrema

with

#### a

value

of

|D(%)|

less
than

0.03

were

discarded

(as

before,

we

assume
image
pixel

values

- in

the

range
[0,1]).
Figure

5

shows

the
effects
of

- keypoint

selection

on

#### a

natural

image.

In

order
to
avoid
too

much
clutter,

a

low-resolution

233

by

#### 189

pixel

<!-- table: missing headers/rows -->
> image

is

used

and

keypoints

are

shown

#### as

vectors

giving
the

location,

scale,

and

orientation

of

each

## keypoint

(orientation

assignment

is

described
below).

Figure
5

(a)

shows
the
original

image,
which

#### is

shown

#### at

reduced
contrast
behind

the

subsequent

<!-- table: missing headers/rows -->
> figures.

Figure
5

(b)

shows
the
832

keypoints

#### at

all

detected

maxima

=D+

11
and
minima

of

the
difference-of-Gaussian
function,

while

(c)
shows
the
729
keypoints
that
remain
following
removal

of

those

<!-- table: missing headers/rows -->
> with

a
value

of

|D(%)|

less

than
0.03.

Part

(d)
will
be
explained
in
the
following
section.
4.1
Eliminating

<!-- table: missing headers/rows -->
> edge

responses

For

stability,
it

is

not

sufficient

to

reject
keypoints
with
low
contrast.
The
difference-of- Gaussian

function

will

- have
- a

strong
response
along
edges,
even
if

the

location
along
the

<!-- table: missing headers/rows -->
> edge

is

poorly
determined

and

therefore
unstable

to

- small

amounts

of

noise.

A

<!-- table: missing headers/rows -->
> poorly

defined

peak

- in
- the

difference-of-Gaussian
function
will
have
a

### large

principal
curvature
across
the

<!-- table: missing headers/rows -->
> edge
<!-- table: missing headers/rows -->
> but

a

<!-- table: missing headers/rows -->
> small

#### one

- in

the
perpendicular
direction.

The

principal
curva- tures
- can

be

- computed

from

a

2x2
Hessian
matrix,

H,
computed
at
the
location
and
scale

of

the
keypoint:

D,,
D,

zy

The

derivatives

are

estimated

by

taking

differences

of
neighboring
sample

points.

The

eigenvalues
of

H

are
proportional
to
the

principal

curvatures

of

D.

Borrowing

from
the
approach

<!-- table: missing headers/rows -->
> used

by

<!-- table: missing headers/rows -->
> Harris

and

Stephens

(1988),

we

can

avoid
explicitly
computing
the

eigenvalues,

- as

we

are
only
concerned
with
their

ratio.

- Let

be

the

eigenvalue

with
the

- largest

magnitude

and
3

be

- the
- smaller

#### one.

- Then,
- we
- can

compute
the

sum

of

the
eigenvalues

from
the
trace

of
H
and

their

product

from

- the

determinant:

Dy
6,

Det(H)

(Dyy)?

In
the

unlikely

event
that

- the

<!-- table: missing headers/rows -->
> determinant

is

- negative,

the

curvatures

#### have

different
signs

so

the

point

is

discarded

#### as

not

being

an

extremum.

- Let

r
be

- the
- ratio

#### between

- the

### largest

### magnitude

- eigenvalue

and

- the
- smaller

#### one,

- so
- that

r3.

- Then,
- (r+1)?
- DetH)

a8
which

depends

- only
- on
- the
- ratio
- of
- the
- eigenvalues
- rather
- than

their

individual
values.

The
quantity

- (r+1)2/r

is
at

- a

minimum
when

- the

two

- eigenvalues

are

- equal

and

it
increases

with

r.

- Therefore,
- to
- check
- that
- the
- ratio
- of
- principal
- curvatures

is
below

#### some

threshold,

r,
we

only

- need

to

check
Tr(H

- (r+1)?
- Det(H)

This

is
very

efficient

to

compute,

with
less

<!-- table: missing headers/rows -->
> than

20
floating

point
operations
required
to
test

each

keypoint.
The

experiments

<!-- table: missing headers/rows -->
> in

#### this

paper

<!-- table: missing headers/rows -->
> use

#### a

value

of

7

10,

which

eliminates
keypoints

that

- have
- a
- ratio

between

- the

principal
curvatures

#### greater

#### than

10.

The

transition

from
Figure
5

(c)
to

5
Orientation
assignhment

By

assigning
a
consistent
orientation

- to

#### each

### keypoint

based

#### on

local
image
properties,
the
keypoint
descriptor

- can

be
represented
relative

- to

#### this

orientation

and

therefore
achieve
invariance
to
image
rotation.

This

approach
contrasts

with

the
orientation
invariant
descriptors

of

Schmid

and

Mohr

(1997),

in

which

#### each

<!-- table: missing headers/rows -->
> image

property
is
based

#### on

a
rotationally
invariant
measure.

The

disadvantage

of
that

approach

is

- that

it

limits

the
descriptors

that

can
be
used

and

discards
image
information

by

not

requiring
all
measures

- to

be

based
on
a
consistent
rotation.

Following

experimentation

<!-- table: missing headers/rows -->
> with

- a

#### number

- of

approaches

- to

assigning

#### a

local

orientation,
the

following

approach

<!-- table: missing headers/rows -->
> was
<!-- table: missing headers/rows -->
> found

- to

give

- the
- most

stable
results.
The
scale

of

the
keypoint

is

- used

to

select
the

Gaussian
smoothed

<!-- table: missing headers/rows -->
> image,

L,

with
the
closest

scale,

so
that

all

compu- tations

are

performed
in
a

scale-invariant

manner.

For

#### each

<!-- table: missing headers/rows -->
> image

sample,
L(z,y),
at
this

scale,

the

gradient
magnitude,

and

orientation,

is

precomputed
using

pixel
differences:

/(L@
1,y)

1,)?

1)

1))*

An

orientation

- histogram

is

- formed

from
the

gradient
orientations

of

sample
points
within
aregion

around
the

- keypoint.
- The

orientation

- histogram

has

36

bins
covering
the
360
degree
range

of

orientations.

- Each
- sample
- added
- to
- the
- histogram

is

weighted

by
its

gradient
magni- tude

and
by

a

Ga

n-weighted

circular

window

with

a

o
that
is
1.5
times
that
of

the

scale

of
the

- keypoint.

Peaks

- in
- the

orientation

- histogram

correspond
to

dominant
directions

of

local
gradients.

The
highest
peak

- in
- the
- histogram

is

detected,

and

then
any
other
local

peak

that

#### is

within
80%

of

- the
- highest
- peak

is

- used

to

- also

create

#### a

### keypoint

#### with

#### that

orientation.
Therefore,

for

locations

with

- multiple
- peaks
- of
- similar
- magnitude,

#### there

will
be
multiple

keypoints
created

#### at

- the
- same
- location
- and
- scale
- but
- different

orientations.

Only
about

15%

of

points

are

assigned

- multiple
- orientations,

but

- these

contribute

- significantly

to
the

stability

of

matching.
Finally,
a

parabola
is
fit
to

- the

3

- histogram

values

- closest
- to

#### each

peak

to

interpolate

the
peak
position

for

better

accuracy.

Figure
6
shows

- the

experimental

stability

- of

location,

#### scale,

#### and

orientation
assignment

under
differing

- amounts

of

<!-- table: missing headers/rows -->
> image

noise.

- As

before
the

<!-- table: missing headers/rows -->
> images

are

rotated

and

scaled
by
random

- amounts.
- The
- top

line

- shows
- the
- stability
- of

### keypoint

location

- and

scale

assign- ment.
- The

second
line

- shows
- the
- stability
- of

matching
when

- the

orientation
assignment

is

100
80
o

S

- 60

3

8

3

2

40
g
o

Matching

- location

#### and

#### scale

20
Matching

- location,
- scale,

#### and

orientation
Nearest
descriptor

- in

database

00%

2%

4%
6%
8%
10%

Image
noise
Figure
6:
The

- top

line

in
the

<!-- table: missing headers/rows -->
> graph
<!-- table: missing headers/rows -->
> shows

- the

percent

of

keypoint
locations

#### and

scales

that

are

repeatably
detected

as

- a

function

of

pixel
noise.
The
second
line

shows

the

repeatability

after
also

requiring
agreement

in

orientation.

The

<!-- table: missing headers/rows -->
> bottom
<!-- table: missing headers/rows -->
> line
<!-- table: missing headers/rows -->
> shows

the
final

<!-- table: missing headers/rows -->
> percent

of

descriptors
correctly
matched
to
alarge
database.

6
The
local

<!-- table: missing headers/rows -->
> image

descriptor

The
previous

operations

have

assigned

- an

<!-- table: missing headers/rows -->
> image

location,

- scale,

and

orientation
to
each
keypoint.

<!-- table: missing headers/rows -->
> These
<!-- table: missing headers/rows -->
> parameters

impose

a
repeatable

local
2D

coordinate

system
in

which
to
describe

the
local

<!-- table: missing headers/rows -->
> image

region,

and

therefore

provide

invariance

- to

#### these

parameters.

The

next
step
is

to

compute

- a

descriptor

for

- the
- local

<!-- table: missing headers/rows -->
> image

- region

that

#### is

highly

distinctive

yet

is

#### as

invariant

- as
- possible

to

remaining
variations,

- such
- as

### change

- in

illumination

or

3D
viewpoint.

One

- obvious
- approach

<!-- table: missing headers/rows -->
> would

- be
- to
- sample
- the
- local

image
intensities
around

the

keypoint

- at

the

appropriate

<!-- table: missing headers/rows -->
> scale,

and

- to
- match

#### these

- using

a
normalized
correlation
measure.

- However,

simple

- correlation
- of

<!-- table: missing headers/rows -->
> image

patches

is

- highly

#### sensitive

#### to

- changes

that

cause
mi
registration

of

samples,

- such
- as

affine

- or
- 3D

viewpoint

- change

or

non-rigid
deformations.
A

better

- approach

has

- been
- demonstrated

by
Edelman,

Intrator,

and

Poggio

(1997).

Their

proposed
representation

- was
- based
- upon
- a

model

- of

biological
vision,

- in

particular

- of
- complex

neurons

- in

primary
visual
cortex.

These

- complex

#### neurons

respond

to

#### a

gradient

#### at

#### a

particular

orientation

and

spatial
frequency,

- but
- the
- location
- of
- the

gradient

#### on

#### the

retina

is

allowed

- to

shift
over

- a

small

receptive

field

- rather

#### than

being
precisely

localized.

Edelman
et

al.

hypoth- esized

that

- the

function

of

#### these

- complex

#### neurons

- was

to

allow

#### for

matching

#### and

recognition

of
3D

objects

from

- a
- range

of

viewpoints.

They

#### have

<!-- table: missing headers/rows -->
> performed

detailed

experiments
using

3D

computer

- models
- of

object

and

animal
shapes
which

#### show

- that

matching
gradients
while

- allowing

for

shifts

- in

their

- position

results
in

much
better

classification
under
3D
rotation.

For

- example,

recognition
accuracy

for
3D

objects

- rotated

#### in

depth

by

20

degrees
increased

from

35%

for

correlation

of

gradients

to

94%

using
the

complex

cell
model.
Our

implementation
described
below

was

inspired

by
this

idea,

but

allows

for

positional

#### shift

using

#### a

different

computational
mechanism.

#### 14

<!-- table: missing headers/rows -->
> Image

- gradients

Keypoint
descriptor

Figure

- 7:
- A

keypoint
descriptor

is

created

by

first
computing

the
gradient
magnitude

and

orientation
at

each

<!-- table: missing headers/rows -->
> image

- sample
- point
- in
- a

region
around
the

#### keypoint

location,

- as
- shown

on
the
left.
These

are

weighted

by

a

Gaussian

window,
indicated

by
the

overlaid

circle.
These

samples

are
then

accumulated

into

orientation

- histograms

summarizing

the
contents
over
4x4
subregions,

#### as

shown
on
the
right,
with

- the

length

of

- each

<!-- table: missing headers/rows -->
> arrow

- corresponding
- to
- the

sum
of
the

gradient
magnitudes
near
that
direction
within
the

region.

This

figure

<!-- table: missing headers/rows -->
> shows

a

2x2
descriptor

array

- computed

from

#### an

8x8
set

of

samples,
whereas

the

experiments

<!-- table: missing headers/rows -->
> in

this
paper

<!-- table: missing headers/rows -->
> use

4x4

<!-- table: missing headers/rows -->
> descriptors

- computed

from

#### a

16x16
sample

array.

6.1

<!-- table: missing headers/rows -->
> Descriptor

representation

Figure
7

illustrates

the

computation

<!-- table: missing headers/rows -->
> of

- the

keypoint
descriptor.

First

the
image
gradient
magnitudes

and

orientations

- are

sampled

- around

the

## keypoint

location,
using
the

scale

of

the
keypoint

to

select

- the
- level

of

- Gaussian

blur
for

- the

image.

<!-- table: missing headers/rows -->
> In

order
to
achieve
orientation
invariance,

the

coordinates

- of
- the

descriptor

and

- the

gradient
orientations

are

rotated
relative

to
the

keypoint
orientation.

For

efficiency,

- the

gradients

are
precomputed
for

all
levels

- of

the
pyramid

- as

<!-- table: missing headers/rows -->
> described

- in

Section
5.

- These
- are
- illustrated

<!-- table: missing headers/rows -->
> with

- small

arrows

- at

#### each

sample

- location
- on
- the
- left

<!-- table: missing headers/rows -->
> side
<!-- table: missing headers/rows -->
> of

Figure

- 7.

A

- Gaussian

weighting

function

<!-- table: missing headers/rows -->
> with

<!-- table: missing headers/rows -->
> equal

- to

one
half
the
width

of

- the

descriptor
window

is

- used

to

assign

- a
- weight
- to
- the
- magnitude
- of

#### each

- sample

## point.

This

is

illustrated

with

- a

circular

window

- on
- the
- left

<!-- table: missing headers/rows -->
> side
<!-- table: missing headers/rows -->
> of

Figure

- 7,

although,

of

- course,

the

weight
falls
off
smoothly.

The

- purpose

of

- this
- Gaussian

window

- is
- to

avoid
sudden

- changes
- in
- the

descriptor

with

- small
- changes
- in
- the
- position
- of
- the

#### window,

and

- to

give
less

emphasis

to

gradients

that

are
far
from

- the

center

of

- the
- descriptor,
- as
- these
- are
- most
- affected

by

misregistration

errors.

- The
- keypoint

descriptor

- is
- shown
- on
- the
- right

<!-- table: missing headers/rows -->
> side

of
Figure

- 7.

It

allows

for

significant
shift

- in

gradient
positions

by

- creating

orientation

- histograms

#### over

4x4

sample

regions.

The
figure
shows
eight

directions

- for
- each

orientation

- histogram,

with
the

length

of

#### each

arrow

- corresponding
- to
- the
- magnitude

of

- that
- histogram

entry.

#### A

gradient
sample

on

the
left
can

shift

- up
- to

4

- sample
- positions

while
still

## contributing

#### to

- the

#### same

histogram

#### on

the
right,

thereby
achieving
the

objective

of

allowing

#### for

### larger

local

positional
shifts.

It

is

important

to

avoid

all

boundary
affects
in

which
the
descriptor
abruptly
changes

#### as

#### a

sample

shifts
smoothly

from
being

- within

#### one

histogram
to

The
descriptor
is
formed

from

a
vector
containing
the
values

of

all
the
orientation
histogram
entries,
corresponding

to

the
lengths

<!-- table: missing headers/rows -->
> of

the
arrows
on
the
right
side

of

Figure
7.
The
figure
shows
a
2x2
array

of

orientation

- histograms,

whereas
our
experiments
below
show
that
the
best
results

are

achieved
with
a
4x4

- array

of

histograms

with

8
orientation
bins
in
each.

Therefore,
the

experiments

<!-- table: missing headers/rows -->
> in

this
paper
use
a
4x4x8

128
element

feature
vector

for

each
keypoint.
Finally,
the

<!-- table: missing headers/rows -->
> feature

vector

is

modified

to

reduce

- the

effects

of

illumination
change.
First,
the
vector

is

normalized

- to

unit
length.

- A
- change
- in

image
contrast

in

which
each

pixel

value
is
multiplied

by

a
constant

will

multiply

gradients

by

- the

#### same

constant,
so
this
contrast
change

will

be

canceled

by

vector

normalization.

- A

brightness
change

- in

which
a
constant

is

- added

to

each

<!-- table: missing headers/rows -->
> image

- pixel

will
not

affect

- the

gradient
values,

#### as

### they

are

computed

from
pixel

differences.

- Therefore,

the

descriptor

is

invariant

to

affine
changes
in
illumination.
However,

non-linear

illumination

- changes

can

also
occur

#### due

to

camera

saturation

or
due
to

illumination

changes
that

affect

3D
surfaces

<!-- table: missing headers/rows -->
> with

differing

orientations

by

different
amounts.

These
effects
can
cause

- a
- large
- change
- in

relative

- magnitudes

for

some
gradients,
but

are
less
likely

- to

affect
the

gradient
orientations.

- Therefore,

we

reduce

- the

influence
of

- large

gradient

- magnitudes

by

thresholding
the

values

<!-- table: missing headers/rows -->
> in

the

unit
feature

vector
to
each

be

no

larger
than

0.2,

and

then
renormalizing
to

- unit

length.

This

- means

that

matching
the

magnitudes

for

- large

gradients

is
no

longer

as

important,

and

that
the

distribution

of

orientations

has

greater
emphasis.

The

value

of
0.2
was

determined
experimentally
using
images

containing
differing

illuminations

for

- the
- same

3D

objects.
6.2
Descriptor
testing
There
are

- two

<!-- table: missing headers/rows -->
> parameters

that

- can
- be
- used
- to

vary

- the

complexity

of

the
descriptor:
the

- number

of

orientations,

- 7,
- in
- the
- histograms,

and

- the

width,

n,

of
the

n

x

n

#### array

of

orientation

- histograms.

The

- size
- of
- the

resulting

descriptor
vector

is
As
the

complexity

of

- the

descriptor

grows,

- it

will

be

- able
- to

discriminate

- better
- in

#### a

### large

database,
but

it

will

also

be
nsitive

to

shape
distortions

and

occlusion.
Figure
8
shows

<!-- table: missing headers/rows -->
> experimental
<!-- table: missing headers/rows -->
> results

- in
- which
- the
- number
- of

orientations

and

#### size

- of
- the

descriptor

- were
- varied.

The

<!-- table: missing headers/rows -->
> graph

- was

### generated

<!-- table: missing headers/rows -->
> for

#### a

viewpoint

transformation

in

which
a

planar

surface

is
tilted
by

<!-- table: missing headers/rows -->
> 50

degrees
away
from
the
viewer

and

4%

image

noise

is

#### added.

This

is
near
the
limits

of

reliable
matching,

- as

60

<!-- table: missing headers/rows -->
> S

T

50
5

I3

5

<!-- table: missing headers/rows -->
> S

40
8
8
g
30
8

<!-- table: missing headers/rows -->
> With

16

orientations

<!-- table: missing headers/rows -->
> S

2

<!-- table: missing headers/rows -->
> With

8

orientations

5

o

<!-- table: missing headers/rows -->
> With

4
orientations

5

<!-- table: missing headers/rows -->
> S

10
0

1

2
3

4

5
Width

n

of

descriptor

(angle

<!-- table: missing headers/rows -->
> 50

deg,
noise

4%)

Figure

8:

This

<!-- table: missing headers/rows -->
> graph

shows
the
percent

<!-- table: missing headers/rows -->
> of

keypoints

<!-- table: missing headers/rows -->
> giving

the
correct
match
to

#### a

database

of

40,000
keypoints

- as
- a

function

of

width

of

the
n
x
n
keypoint
descriptor

and

the
number

of

orientations
in
each
histogram.

The

<!-- table: missing headers/rows -->
> graph

is

computed

for

images

<!-- table: missing headers/rows -->
> with

affine
viewpoint
change

- of

50
degrees

and

addition

of

4%

noise.
6.3
Sensitivity
to

affine
change

The

sensitivity

<!-- table: missing headers/rows -->
> of

- the

descriptor

<!-- table: missing headers/rows -->
> to

- affine
- change

is

<!-- table: missing headers/rows -->
> examined

in

Figure

9.

The

graph
shows

the

reliability

of

- keypoint

location

- and

scale

selection,

orientation

assignment,

and

nearestneighbor

matching

- to
- a

database

- as
- a

function

- of

rotation

- in

depth

of

#### a

plane

away

from

#### a

viewer.

It
can
be

- seen

that

each

<!-- table: missing headers/rows -->
> stage

of

computation

has

reduced
repeatability
with
increasing

affine
distortion,

but

- that
- the

final
matching

accuracy
remains
above
50%
out

to

a

<!-- table: missing headers/rows -->
> 50

- degree
- change
- in

viewpoint.

To

achieve
reliable

- matching
- over
- a

#### wider

## viewpoint

angle,

#### one

of

the

affine-invariant
detectors

- could
- be
- used
- to

select

- and
- resample

<!-- table: missing headers/rows -->
> image

regions,

- as
- discussed

in
Section
2.

- As

<!-- table: missing headers/rows -->
> mentioned

there,

none
of

- these
- approaches

is
truly

- affine-invariant,

#### as

they

all

start
from
initial
feature

locations

- determined
- in
- a

non-affine-invariant
manner.

In
what

<!-- table: missing headers/rows -->
> appears

to
be

the
most

- affine-invariant

method,

Mikolajczyk

(2002)

- has

proposed

#### and

run

detailed
experiments
with

the
Harris-affine
detector.
He

found

- that

its

- keypoint

repeatability

is
below
that
given

here

- out
- to

about

- a

<!-- table: missing headers/rows -->
> 50

- degree
- viewpoint
- angle,
- but
- that

it

- then

retains

- close

to

40%
repeatability

- out

to

- an

angle

of

70

- degrees,

which

provides

- better

performance

for

extreme
affine
changes.

The

disadvantages

are

- a

much
higher
computational

<!-- table: missing headers/rows -->
> cost,

#### a

reduction
in
the

- number

of

keypoints,

and

poorer

stability

for

- small
- affine
- changes
- due

#### to

errors

in

assigning

#### a

consistent
affine

frame

under

noise.

In
practice,

the
allowable

- range
- of

rotation

for

3D

object

considerably

less
than
for

planar

surfaces,

so

- affine

invariance

is
usually
not
the
limiting
factor

in
the
ability

to

match

#### across

## viewpoint

- change.

If

#### a

#### wide

#### range

#### of

#### affine

invariance

is

desired,
such

- as

for

#### a

surface

that
is

- known
- to

be
planar,

- then

#### a

simple

solution

is

#### to

adopt

the
approach

of

Pritchard
100
80

<!-- table: missing headers/rows -->
> S

x

<!-- table: missing headers/rows -->
> 60

3
s
8

g

40

Matching

location

<!-- table: missing headers/rows -->
> and

#### scale

20

- Matching
- location,
- scale,

#### and

orientation

Nearest
descriptor

- in

database

0
10

20

30
40
50
Viewpoint
angle

(degrees)
Figure

9:

This

<!-- table: missing headers/rows -->
> graph

shows
the

stability

<!-- table: missing headers/rows -->
> of

detection

for

keypoint
location,
orientation,

and

final
matching

to

- a

database

- as
- a

function

of

affine

distortion.
The
degree

of

affine
distortion

is

expressed

in

terms

of
the

equivalent

viewpoint

rotation

- in

depth

for

a

planar

surface.

6.4
Matching

to

large

databases

An

important

remaining

is
ue

for
measuring

the
distinctiveness

of

features
is
how
the
reliability

of

matching

- varies
- as
- a

function

- of
- the
- number
- of

features

- in

the
database

being

matched.

Most
of
the

<!-- table: missing headers/rows -->
> examples
<!-- table: missing headers/rows -->
> in

- this

<!-- table: missing headers/rows -->
> paper

are

### generated

using

#### a

database

of

32
images

<!-- table: missing headers/rows -->
> with

about

40,000

- keypoints.

<!-- table: missing headers/rows -->
> Figure

10

- shows
- how
- the

matching
reliability
varies

#### as

a
function

- of
- database
- size.
- This

<!-- table: missing headers/rows -->
> figure

- was

### generated

<!-- table: missing headers/rows -->
> using

#### a

### larger

database

of

112
images,
with
a
viewpoint

<!-- table: missing headers/rows -->
> depth

rotation

of

#### 30

- degrees

and

2%

<!-- table: missing headers/rows -->
> image

noise

- in

addition

to
the
usual

random

<!-- table: missing headers/rows -->
> image

rotation

and

- scale

change.
The

<!-- table: missing headers/rows -->
> dashed

line

- shows
- the
- portion
- of

<!-- table: missing headers/rows -->
> image

- features

for

which
the

nearest

neighbor

- in
- the
- database
- was
- the

<!-- table: missing headers/rows -->
> correct

match,

- as
- a

function

- of
- database
- size

<!-- table: missing headers/rows -->
> shown

on
a

logarithmic
scale.
The

- leftmost
- point
- is
- matching

against

- features
- from
- only

#### a

single

<!-- table: missing headers/rows -->
> image

while
the

- rightmost
- point

is

selecting

- matches
- from
- a
- database
- of

all

- features

from
the

112
images.

It

can
be

- seen

that

- matching

reliability
does

decrease

- as
- a

function

of

- the
- number

of

distractors,

yet

all

- indications
- are

that

- many
- correct
- matches

will

continue

- to

be

- found
- out

to
very

- large
- database
- sizes.

The

<!-- table: missing headers/rows -->
> solid

line
is

- the

percentage

- of

## keypoints

- that
- were

identified

#### at

the

correct
matching

location

and

#### orientation

- in

the
transformed

<!-- table: missing headers/rows -->
> image,

#### so

- it

is
only

#### these

points

that

have

any

chance

of

- having
- matching

descriptors

- in
- the

database.

- The
- reason

this
line

is

flat

is

that
the

test

was

run

over

the
full

database

- for

#### each

value,

while

### only

varying

- the

portion

of

- the

database

- used

for

distractors.

- It

is
of

interest

that

- the

gap

between
the

two

lines

is
small,
indicating

that

matching

failures

are

#### due

#### more

to

#### issues

with

initial

feature

localization

and

orientation
assignment

than
to

problems

with

feature

distinctiveness,
even
out

to

large
database

sizes.

18
100
80
g

<!-- table: missing headers/rows -->
> 60

3

s
3
40

Matching

location,

- scale,

and

orientation

I3

Nearest
descriptor

- in

database
o«
20
1000

10000

100000

- Number
- of

keypoints

- in

database

(log
scale)
Figure

10:

The

<!-- table: missing headers/rows -->
> dashed

line

<!-- table: missing headers/rows -->
> shows

the

<!-- table: missing headers/rows -->
> percent
<!-- table: missing headers/rows -->
> of

keypoints
correctly
matched
to

#### a

database

#### as

a

function

of

database
size

(using

a

logarithmic
scale).
The

<!-- table: missing headers/rows -->
> solid

line

shows

the
percent

of

keypoints
assigned

the

correct
location,

- scale,

and

orientation.

<!-- table: missing headers/rows -->
> Images
<!-- table: missing headers/rows -->
> had

random
scale

and

rotation
changes,

an

affine
transform

of

30
degrees,

and

<!-- table: missing headers/rows -->
> image
<!-- table: missing headers/rows -->
> noise
<!-- table: missing headers/rows -->
> of

2%

<!-- table: missing headers/rows -->
> added

prior
to

matching.

7

Application

to
object

recognition

The

<!-- table: missing headers/rows -->
> major
<!-- table: missing headers/rows -->
> topic
<!-- table: missing headers/rows -->
> of

this

<!-- table: missing headers/rows -->
> paper

is

the
derivation

of

distinctive
invariant
keypoints,

- as

described
above.

- To

demonstrate

their

application,
we

<!-- table: missing headers/rows -->
> will

now

give

- a

brief
description

- of

#### their

use

for

object

recognition

- in
- the
- presence

of

clutter

and

occlusion.

More

details

#### on

applications

- of
- these

<!-- table: missing headers/rows -->
> features

- to

recognition

- are
- available
- in

#### other

<!-- table: missing headers/rows -->
> papers

(Lowe,

1999;
Lowe,
2001;
Se,
Lowe

and

Little,
2002).
Object

recognition

is

performed

- by
- first
- matching

#### each

### keypoint

independently

#### to

the

- database

of

- keypoints

extracted

from

training

<!-- table: missing headers/rows -->
> images.

- Many
- of

#### these

initial
matches
will
be
incorrect

- due

to

ambiguous

- features
- or
- features
- that
- arise

#### from

background

#### clutter.

- Therefore,

clusters

- of
- at
- least

3

<!-- table: missing headers/rows -->
> features

- are
- first
- identified
- that

<!-- table: missing headers/rows -->
> agree

- on

#### an

object

and

#### its

pose,

- as

#### these

- clusters

have

- a
- much

higher

- probability
- of

### being

- correct

#### than

individual

feature

matches.

- Then,

each
cluster

is

- checked

by

## performing

- a
- detailed

geometric
fit

- to

the

model,

and

the
result

is

- used

to

- accept

or

- reject
- the

interpretation.

- 7.1
- Keypoint
- matching
- The
- best

candidate

match

for

- each
- keypoint
- is
- found
- by

identifying

#### its

nearest
neighbor

in
the

- database

of

- keypoints

from

training

<!-- table: missing headers/rows -->
> images.

- The

nearest
neighbor
is

defined

#### as

the

keypoint

<!-- table: missing headers/rows -->
> with

minimum
Euclidean
distance
for

- the

invariant
descriptor
vector

#### as

was
described
in

Section

6.

- However,

many

<!-- table: missing headers/rows -->
> features
<!-- table: missing headers/rows -->
> from

#### an

<!-- table: missing headers/rows -->
> image

will

- not

#### have

#### any

correct

match

- in

the
training
database

because

### they

arise
from
background

#### clutter

or

#### were

#### not

#### detected

in
the
training
images.

Therefore,
it
would

be

useful

- to
- have
- a

#### way

- to

discard
features

that

do

not

have

#### any

good
match

to
the

database.

A

global
threshold

#### on

distance

#### to

#### the

#### closest

feature
does

not

perform

well,
as

#### some

descriptors

are

#### much

#### more

discriminative

#### than

#### others.

A

#### more

effective

measure

is

obtained

by

### comparing

- the

distance

of

#### the

#### closest

neighbor

to
that
of

the
19
0.8
0.7

- 0.6

<!-- table: missing headers/rows -->
> PDF

for

correct
matches

<!-- table: missing headers/rows -->
> PDF

for

incorrect
matches

- 0.5
- 0.4

PDF

<!-- table: missing headers/rows -->
> 03

- 02

0.1

e
0
01
02

<!-- table: missing headers/rows -->
> 03

- 04

<!-- table: missing headers/rows -->
> 05

06
07
08

09

1
Ratio
of

distances

(closest/next

closest)

Figure

11:

The

probability

- that
- a

match

- is

correct

- can

be

determined

by

taking
the
ratio

of

distance

from
the
closest
neighbor
to
the

distance

<!-- table: missing headers/rows -->
> of

- the

second

closest.

Using

#### a

database
of

40,000
keypoints,
the

<!-- table: missing headers/rows -->
> solid

line

shows

- the

<!-- table: missing headers/rows -->
> PDF

of
this

- ratio

<!-- table: missing headers/rows -->
> for

correct
matches,

while
the

<!-- table: missing headers/rows -->
> dotted

line

is

for

matches

- that

were

incorrect.
second-closest

neighbor.

If

<!-- table: missing headers/rows -->
> there

are

multiple

training

<!-- table: missing headers/rows -->
> images
<!-- table: missing headers/rows -->
> of

the

#### same

object,

then
we
define
the

- second-closest

neighbor

- as

being

- the
- closest

neighbor
that

is
known
to
come

from

a
different

object

than
the

first,

- such
- as
- by

only
using
images
known
to
contain
different
ob- jects.

This

<!-- table: missing headers/rows -->
> measure

performs

- well
- because

correct
matches

- need

to

- have
- the

closest

neighbor
significantly

- closer
- than
- the
- closest

#### incorrect

- match
- to

achieve
reliable
matching.

For

false

matches,

there
will

likely

be

- a
- number
- of
- other

false

matches

- within

similar
distances
due

to

the

high

dimensionality

of

- the

<!-- table: missing headers/rows -->
> feature

#### space.

We

- can

think

- of

the
second-closest
match

#### as

providing

- an
- estimate
- of
- the

<!-- table: missing headers/rows -->
> density

- of

false

- matches
- within

#### this

### portion

of

the
feature

#### space

and

at

- the
- same

time
identifying

- specific
- instances
- of

<!-- table: missing headers/rows -->
> feature

ambiguity.

Figure

11

- shows
- the
- value
- of
- this
- measure
- for
- real

<!-- table: missing headers/rows -->
> image

data.

The

probability
density
functions

for

- correct

and

- incorrect
- matches
- are
- shown
- in
- terms

<!-- table: missing headers/rows -->
> of

- the
- ratio
- of

closest

- to
- second-closest

neighbors

- of
- each
- keypoint.
- Matches

#### for

- which

#### the

#### nearest

neighbor

#### was

- a
- correct
- match

have

- a

PDF

that

is
centered
at

- a

much
lower
ratio

#### than

- that

for

incorrect
matches.

For
our

object

recognition
implementation,

we

reject

all
matches

- in

which

- the

distance

- ratio

is

- greater
- than
- 0.8,

which

eliminates
90%

- of
- the

false

matches

while

discarding

- less
- than

5%

- of
- the
- correct
- matches.
- This

figure
was

### generated

by

matching
images

following
random
scale

and

orientation

change,

- a

depth

rotation

of
30
degrees,

and

addition

of

2%

image
noise,
against

- a

database

of
40,000

- keypoints.

7.2

Efficient

nearest
neighbor
indexing
No

algorithms

are
known
that

- can

identify

- the

exact

nearest
neighbors

of

points
in

high

dimensional

that

are

any

#### more

efficient

#### than

exhaustive
search.
Our
keypoint
descriptor

has

a

128-dimensional
feature
vector,

and

the
best

algorithms,
such

#### as

the
k-d

tree

(Friedman

et

al.,
1977)
provide
no

speedup

<!-- table: missing headers/rows -->
> over

exhaustive
search

#### for

#### more

#### than

about
10
neighbor

with

high
probability.

The

BBF
algorithm
uses
a
modified
search
ordering
for
the
k-d

tree

algorithm
so
that
bins
in
feature
space

are

searched
in
the
order

- of

#### their

closest
distance
from
the

query

location.
This
priority
search
order

was

first

<!-- table: missing headers/rows -->
> examined

by

Arya

and

Mount
(1993),

and

they
provide
further
study

of

its
computational
properties
in
(Arya

et

al.,
1998).
This
search
order
requires
the
use

of

a
heap-based
priority
queue

for

efficient
determination

of

the
search
order.
An
approximate
answer

can
be

returned

<!-- table: missing headers/rows -->
> with

low
cost

### by

- cutting

#### off

further
search
after
a
specific
number

- of
- the
- nearest
- bins

have

- been

explored.

<!-- table: missing headers/rows -->
> In

our
implementation,
we
cut
off
search
after
checking
the

- first

<!-- table: missing headers/rows -->
> 200

- nearest-neighbor

candidates.

<!-- table: missing headers/rows -->
> For

a
database

of

100,000
keypoints,
this
provides
a
speedup
over
exact

- nearest

neighbor
search

by

about
2
orders

of

magnitude
yet
results
in

- less

than

a
5%
loss

- in
- the
- number
- of

correct
matches.

One

reason
the
BBF
algorithm
works
particularly

- well

for
this

problem

is

- that

we
only
consider
matches

- in

which
the

nearest
neighbor
is

less
than
0.8

times
the

distance

to
the
second-nearest
neighbor

(as

described
in
the
previous
section),

and

therefore

there
is
no

- need
- to

exactly
solve
the

most

difficult
cases

in

which

many

neighbors

- are
- at
- very
- similar

distances.

7.3
Clustering

with

the

<!-- table: missing headers/rows -->
> Hough

transform

To

maximize

the

performance

of

object

recognition

for

- small

or

highly

occluded
objects,
we

wish
to

identify
objects

with

- the
- fewest
- possible
- number
- of

#### feature

matches.

We

have
found

that

reliable
recognition

is

- possible

with

- as
- few

#### as

3

features.

#### A

typical

image
contains
2,000

or
more

features

which

- may
- come

from

- many

#### different

objects

#### as

- well

#### as

background

clutter.

While
the

distance
ratio

test

<!-- table: missing headers/rows -->
> described

in
Section
7.1
will
allow

us
to
discard

many
of

the

false

matches

arising

from

background
clutter,

#### this

<!-- table: missing headers/rows -->
> does

not

remove
matches

from

#### other

valid
objects,

and
we

often
still

- need
- to
- identify
- correct
- subsets
- of

matches
containing

- less

than

1%
inliers

among

99%

outliers.
Many
well-known
robust
fitting

methods,

- such

#### as

RANSAC

or

Least

<!-- table: missing headers/rows -->
> Median

of

Squares,
perform

- poorly

when
the
percent

of

inliers

falls

- much

below

50%.
Fortunately,

- much

better

performance

- can

be

obtained

### by

clustering
features

- in

pose

#### space

using

- the

Hough

transform

(Hough,

- 1962;

Ballard,

1981;

Grimson

1990).

The

Hough

transform
identifies

- clusters
- of
- features

<!-- table: missing headers/rows -->
> with

#### a

consistent

interpretation

by

using

each

<!-- table: missing headers/rows -->
> feature

- to
- vote
- for

all
object

- poses

that

- are

consistent
with

- the

feature.
When

- clusters
- of
- features

are

- found
- to
- vote
- for
- the
- same
- pose

#### of

#### an

object,

the
dependency

of

location
discretization
on
the
selected
scale).
These
problems
can
be
avoided

by

using
a
pseudo-random

<!-- table: missing headers/rows -->
> hash

function

<!-- table: missing headers/rows -->
> of

the

bin
values

to
insert
votes
into
a
onedimensional
hash
table,
in
which
collisions

are

easily
detected.
7.4
Solution

for

affine
parameters
The
Hough
transform
is
used

to

identify
all
clusters
with
at

- least

3
entries
in
a

bin.

Each
such
cluster

is

then

<!-- table: missing headers/rows -->
> subject

to

- a

geometric
verification
procedure

in

which
a
least-squares
solution

is

performed

for

- the
- best

affine
projection

parameters
relating

the
training
image

to

the
new
image.

An

affine
transformation
correctly
accounts

- for

3D
rotation
of
a
planar
surface
under
orthographic
projection,

but

the

approximation

- can

be

poor

for

3D
rotation

of

non-planar
objects.

- A
- more

general
solution

<!-- table: missing headers/rows -->
> would

- be
- to

solve

for

the
fundamental
matrix
(Luong

and

Faugeras,
1996;
Hartley
and

Zisserman,

2000).

However,
a
fundamental
matrix
solution
requires

- at
- least

7
point

matches

as

- compared

to

only
3

for

the

affine
solution

and

in
practice
requires
even

more

matches

for

good

stability.

We

<!-- table: missing headers/rows -->
> would

like
to
perform
recognition
with

- as

few

- as

3

feature

matches,

so
the

affine
solution
provides
a

better
starting

point

and

we

- can

account

for

errors

- in
- the

affine

approximation

by

allowing
for

large

residual
errors.
If
we

imagine

<!-- table: missing headers/rows -->
> placing

a

sphere
around

#### an

object,
then

rotation

of

the

sphere
by

30

degrees

will

move

no

- point

within
the
sphere

by

- more

than
0.25
times
the
projected
diameter

of

the
sphere.

For

the

examples

of

typical
3D

objects

<!-- table: missing headers/rows -->
> used
<!-- table: missing headers/rows -->
> in

this
paper,

#### an

affine
solution
works

well
given

that
we

allow

residual
errors

- up

to
0.25
times
the
maximum

projected
dimension

of
the

object.

A
more

- general

approach

is

<!-- table: missing headers/rows -->
> given

in
(Brown
and

Lowe,

2002),
in

which
the

initial

solution

is

- based

on

- a

similarity
transform,
which
then

progresses

#### to

solution

for

the

#### fundamental

<!-- table: missing headers/rows -->
> matrix

- in

those
cases

- in
- which
- a

sufficient

#### number

of

matches

are

found.

The

affine
transformation

of

# a

model

<!-- table: missing headers/rows -->
> point

[z

y]”

to

#### an

image

<!-- table: missing headers/rows -->
> point

[u

- can

be

written

where

- the

model
translation
is
[t,

- sented

by

- the

m;
parameters.
‘We
wish

- to
- solve

for

- the

transformation

#### parameters,

#### so

- the

equation
above

- can

be

rewritten

to

gather

the

unknowns

- into
- a

column
vector:

and

the

- affine

rotation,
scale,

and

stretch

are

repremy

z

- y

0

- 010

ma

w

0
0

#### y

01
ma
7,.-|
l
ma

J

t,
This

equation
shows
a

single
match,

but

- any

number

of

further

Figure

12:

The

training

<!-- table: missing headers/rows -->
> images

for

two
objects
are

- shown

<!-- table: missing headers/rows -->
> on

the

left.
These

- can

be

recognized
in
a

cluttered

image

with

extensive

occlusion,

- shown
- in

the
middle.

The

results

of

recognition

are

shown

on

the

<!-- table: missing headers/rows -->
> right.

A

parallelogram
is

drawn

around
each

#### recognized

object

showing
the
boundaries

of

the
original
training
image

<!-- table: missing headers/rows -->
> under

the

affine
transformation

<!-- table: missing headers/rows -->
> solved

#### for

during

recognition.
Smaller
squares
indicate

the

keypoints

that
were

- used

for

recognition.

The
least-squares

solution

for
the

<!-- table: missing headers/rows -->
> parameters

X

- can

be

determined

by

solving
the
corresponding
normal
equations,
which

minimizes
the
sum

<!-- table: missing headers/rows -->
> of

- the

<!-- table: missing headers/rows -->
> squares

- of
- the

distances

from
the

projected
model
locations
to

the
corresponding

<!-- table: missing headers/rows -->
> image

locations.

<!-- table: missing headers/rows -->
> This

- least-squares

approach
could
readily
be
extended
to
solving

for

3D

<!-- table: missing headers/rows -->
> pose

and

internal
parameters

- of

articulated

and

flexible
objects

(Lowe,

1991).
Outliers

- can

now

be

removed

by

checking

for

agreement
between

#### each

image
feature

and

the

model.

- Given

the
more

accurate

- least-squares

solution,

we

now
require
each
match
to

<!-- table: missing headers/rows -->
> agree

- within

half

the

<!-- table: missing headers/rows -->
> error

range

- that
- was
- used
- for
- the

parameters
in
the
Hough
transform

- bins.

If

- fewer
- than

3

- points

remain
after

- discarding

outliers,

- then
- the

match

is

rejected.

- As

outliers

- are
- discarded,
- the
- least-squares
- solution
- is
- re-solved

with

- the

remaining

points,

and

- the

process
iterated.

- In
- addition,
- a
- top-down

matching

phase

is

- used

to

add

- any

further
matches

- that
- agree
- with
- the

projected

<!-- table: missing headers/rows -->
> model

- position.
- These
- may
- have

#### been

missed

from

the

Hough

transform

- bin

due

- to
- the

similarity

transform

approximation

or

#### other

errors.

The

- final
- decision
- to
- accept
- or
- reject
- a

model

hypothesis

is

- based

on

- a

detailed

probabilistic

model

- given
- in
- a

previous

<!-- table: missing headers/rows -->
> paper

(Lowe,

2001).

- This

method

first
computes
the

expected

- number
- of

false

- matches
- to
- the

model

- pose,
- given
- the

projected

#### size

of

the
model,

- the
- number

of

- features
- within

the

region,

and

- the

#### accuracy

of

- the

fit.
A
Bayesian

analysis
then

gives
the

probability

- that
- the

object

is

present

- based
- on
- the

actual

- number
- of

matching
features
found.

We
accept

- a

model

if

- the

final

probability

- for
- a

correct
interpretation

is
greater
than

0.98.

For

objects

- that

project

- to
- small
- regions

of

#### an

image,

3

features

- may

be
sufficient

for

reli- able

recognition.

For

- large

objects
covering

#### most

#### of

#### a

heavily

#### textured

image,

the

expected

- number

of
false

matches

is

higher,

and

#### as

- many

#### as

10

feature

matches

may

be
necessary.

8

Recognition
examples

Figure

12

shows

an

### example

of

object

recognition

for

#### a

cluttered

#### and

occluded
image
containing

3D
objects.

The

training

<!-- table: missing headers/rows -->
> images

of

#### a

toy

train

Figure

13:

<!-- table: missing headers/rows -->
> This
<!-- table: missing headers/rows -->
> example

shows
location

recognition

<!-- table: missing headers/rows -->
> within

a

complex
scene.
The

training
images
for
locations

- are
- shown
- at

the

<!-- table: missing headers/rows -->
> upper
<!-- table: missing headers/rows -->
> left

and

the
640x315
pixel

<!-- table: missing headers/rows -->
> test
<!-- table: missing headers/rows -->
> image

- taken

#### from

#### a

different
viewpoint

is

- on

the

<!-- table: missing headers/rows -->
> upper
<!-- table: missing headers/rows -->
> right.

The

recognized

- regions

are

- shown
- on

the
lower

<!-- table: missing headers/rows -->
> image,

with

keypoints
shown

as

- squares

and
an

outer
parallelogram
showing

- the

#### boundaries

- of
- the

training
images
under
the
affine

transform

- used

for

recognition.

The

middle

<!-- table: missing headers/rows -->
> image

(of

size

<!-- table: missing headers/rows -->
> 600x480

- pixels)

contains

instances

- of

#### these

objects
hidden
behind
others

and
with

extensive

background
clutter
so
that

detection

of

the
objects

may

not

be

immediate
even

for

human
vision.

- The

<!-- table: missing headers/rows -->
> image

- on
- the

<!-- table: missing headers/rows -->
> right

shows

- the

final
correct
identification
superimposed

- on
- a

reduced
contrast
version

- of
- the

image.

- The

keypoints

that

were
used

for

recognition

- are
- shown
- as
- squares

<!-- table: missing headers/rows -->
> with

- an

<!-- table: missing headers/rows -->
> extra

line

- to

indicate
orientation.

- The

sizes

of

the
squares

correspond

- to
- the

image

- regions
- used

#### to

construct
the
descriptor.

An

outer
parallelogram

is

also
drawn
around
each

- instance

of

recognition,

with

#### its

sides

corresponding
to

the

boundaries

of
the

training

<!-- table: missing headers/rows -->
> images

projected

under

- the

final

affine
transformation
determined

during

recognition.

Another

potential
application

of
the

approach

is

- to

## place

recognition,

in

which
a
mobile
device

or

vehicle

could

identify

its

location

by

recognizing
familiar
locations.

Figure

13

gives

an

- example

of
this

application,

- in
- which

training
images

are

- taken

#### of

#### a

#### number

#### of

locations.

As

- shown

on

the

<!-- table: missing headers/rows -->
> upper

- left,

these

- can

even

be

of

such

seemingly

non-distinctive
items

#### as

a
wooden

<!-- table: missing headers/rows -->
> wall

or

a

tree

with

trash

bins.

The
test

image

(of

size
640
by
315
pixels)

on
the

upper

<!-- table: missing headers/rows -->
> right

was

- taken

from

#### a

viewpoint

rotated
about

30

degrees
around

the

#### scene

from

the
original
positions,

yet

the

training

<!-- table: missing headers/rows -->
> image

locations

are
easily

recognized.
24

All

steps

of

the
recognition
process
can
be
implemented
efficiently,
so
the
total
time
to
recognize
all
objects
in
Figures
12
or
13

is

<!-- table: missing headers/rows -->
> less
<!-- table: missing headers/rows -->
> than

0.3
seconds
on
a

2GHz

Pentium
4
processor.
We
have
implemented
these
algorithms

<!-- table: missing headers/rows -->
> on

a

laptop

computer
with
attached
video
camera,

and

have

<!-- table: missing headers/rows -->
> tested

them
extensively
over
a

#### wide

#### range

#### of

conditions.

In

general,
textured
planar
surfaces
can
be
identified
reliably
over

#### a

rotation
in
depth

of

up
to
50
degrees
in
any
direction

and

under
almost

#### any

illumination
conditions

that

provide
sufficient
light
and
do

not

produce
excessive
glare.

For

3D
objects,
the

- range
- of

rotation

- in

depth

#### for

reliable
recognition
is
only
about
30

- degrees
- in
- any

direction

- and

illumination
change
is

#### more

disruptive.

For

these
reasons,
3D

<!-- table: missing headers/rows -->
> object

recognition

- is
- best

performed

### by

integrating
features
from
multiple
views,

- such
- as

with
local

<!-- table: missing headers/rows -->
> feature

view
clustering

(Lowe,

<!-- table: missing headers/rows -->
> 2001).

These

keypoints

- have
- also
- been
- applied
- to
- the

problem

of

robot

localization

and

mapping,

which
has

- been
- presented
- in

detail

- in

other

<!-- table: missing headers/rows -->
> papers

(Se,

Lowe

and

Little,

2001).
In
this
application,

a

trinocular

<!-- table: missing headers/rows -->
> stereo
<!-- table: missing headers/rows -->
> system

is

- used

to

determine
3D
estimates

for

keypoint
locations.

Keypoints

are

- used
- only
- when
- they

<!-- table: missing headers/rows -->
> appear

- in

all
3
images

<!-- table: missing headers/rows -->
> with

consistent
disparities,
resulting
in
very

few
outliers.
As
the

<!-- table: missing headers/rows -->
> robot
<!-- table: missing headers/rows -->
> moves,

it
localizes

itself
using

feature

matches
to
the

existing

3D
map,

and

then
incrementally
adds

features

- to

the
map

while

updating

their

3D
positions
using

a
Kalman
filter.

This

provides

#### a

robust

and

accurate
solution
to
the
problem

of

robot

localization

in

unknown
environments.

#### This

work

has

also

addressed
the
problem

of

place

recognition,

in
which

#### a

robot
can
be
switched

#### on

#### and

recognize

#### its

location
anywhere
within

a

large
map

(Se,

Lowe

and

Little,
2002),
which
is

equivalent

to
a
3D

implementation

of

object

recognition.

9

Conclusions
The

<!-- table: missing headers/rows -->
> SIFT

- keypoints

<!-- table: missing headers/rows -->
> described

- in
- this

<!-- table: missing headers/rows -->
> paper

are
particularly

useful

- due
- to

their

distinctiveness,

which

enables

the

<!-- table: missing headers/rows -->
> correct

match

- for
- a
- keypoint
- to

be

selected

from

#### a

large
database
of
other

- keypoints.

This

- distinctiveness

is

- achieved

by
assembling

#### a

high-dimensional

vector
representing

the
image

gradients

- within
- a

local

- region
- of
- the

image.
The

keypoints
have

#### been

<!-- table: missing headers/rows -->
> shown

- to

be
invariant
to
image
rotation

- and

#### scale

- and

robust

across

#### a

#### substantial

#### range

of

affine

distortion,

- addition
- of

noise,

and

- change
- in

illumination.

<!-- table: missing headers/rows -->
> Large

- numbers

of

keypoints

- can
- be

extracted

from
typical

<!-- table: missing headers/rows -->
> images,

- which
- leads

#### to

robustness
in

extracting

- small

objects

among
clutter.

- The

fact

- that
- keypoints
- are
- detected
- over
- a

complete

#### range

#### of

scales

- means

that

- small
- local
- features
- are
- available
- for

matching

(Funt

and

Finlayson,
1995;
Brown

<!-- table: missing headers/rows -->
> and

Lowe,

2002).

Similarly,
local
texture
measures
appear
to

<!-- table: missing headers/rows -->
> play

an

important

<!-- table: missing headers/rows -->
> role

in
human
vision

and

could
be
incorporated
into
feature
descriptors
in
a
more
general
form

than

the

single

spatial
frequency
used

### by

the
current
descriptors.
An
attractive

<!-- table: missing headers/rows -->
> aspect

of
the

invariant
local
feature
approach

#### to

matching

is

that

there

is

no
need

to

select
just
one

<!-- table: missing headers/rows -->
> feature

type,

and

the

<!-- table: missing headers/rows -->
> best

results

are

likely

#### to

be
obtained

### by

using
many
different
features,

all
of

which

- can

contribute
useful
matches

and

improve
overall
robustness.

Another

direction

for

future
research
will
be

#### to

individually
learn
features

that

#### are

suited
to
recognizing
particular
objects

- categories.
- This

will
be
particularly
important
for
generic
object
classes

- that

must
cover
a

- broad
- range
- of

possible
appearances.

The

research

of

Weber,
Welling,

and

<!-- table: missing headers/rows -->
> Perona

(2000)
and

Fergus,

<!-- table: missing headers/rows -->
> Perona,

and

Zisserman
(2003)
has
shown
the
potential

of
this

approach

by

learning

- small
- sets
- of

local
features

that

are

suited
to
recogniz## ing

generic

- classes

of

objects.

- In

the

- long

term,

<!-- table: missing headers/rows -->
> feature

sets

are
likely

to
contain
both
prior

and

learned

- features

that
will

- be
- used

according
to
the
amount

of

training
data

that

has
been
available

for

various

object

classes.

Acknowledgments

particularly

- like
- to

<!-- table: missing headers/rows -->
> thank

Matthew
Brown,

- who
- has

<!-- table: missing headers/rows -->
> suggested

numerous
improvements
to
both

the

content

and

presentation

of
this

paper

and

whose

#### own

work
on

feature

localization

and

invariance

has

contributed

to
this

approach.

In

- addition,

I

<!-- table: missing headers/rows -->
> would

like

to

thank

many
others

for

#### their

valuable

suggestions,
including

<!-- table: missing headers/rows -->
> Stephen

Se,

<!-- table: missing headers/rows -->
> Jim

Little,
Krystian
Mikolajczyk,

Cordelia
Schmid,
Tony

Lindeberg,

and

Andrew

Zisserman.

This

research
was
supported
by
the
Natural

Sciences

and

Engineering
Research

<!-- table: missing headers/rows -->
> Council

of

Canada

(NSERC)
and

through
the

Institute

for
Robotics

and

Intelligent

Systems

(IRIS)

Network
of

<!-- table: missing headers/rows -->
> Centres

of

Excellence.

References
Arya,

S.,
and

Mount,

<!-- table: missing headers/rows -->
> D.M.

1993.

- Approximate

nearest
neighbor
queries

in

fixed

dimensions.

In
Fourth
Annual

- ACM-SIAM

<!-- table: missing headers/rows -->
> Symposium

- on

Discrete
Algorithms
(SODA’93),

- pp.

271-280.

Arya,

- S.,

Mount,

- D.M.,

Netanyahu,

- N.S.,

Silverman,

- R.,

and

#### Wu,

- A.Y.

1998.

An

optimal
algorithm

for

approximate
nearest
neighbor
searching.
Journal
of
the

ACM,
45:891-923.

Ballard,

D.H.

- 1981.
- Generalizing

the

<!-- table: missing headers/rows -->
> Hough

transform

to

detect
arbitrary

patterns.

Pattern

Recognition,
13(2):111-122.
Basri,

Edelman,
S.,
Intrator,
N.

and

Poggio,

<!-- table: missing headers/rows -->
> T.

1997.
Complex
cells
and
object
recognition.
Unpublished
manuscript:
http://kybele.psych.cornell.edu/~edelman/archive.html
Fergus,
R.,
Perona,
P,

and

Zisserman,

#### A.

2003.

Object

class
recognition

by

unsupervised
scaleinvariant
learning.

In
IEEE

Conference

on

Computer
Vision

and

Pattern
Recognition,
Madison,
‘Wisconsin,

- pp.

<!-- table: missing headers/rows -->
> 264-271.

Friedman,
J.H.,
Bentley,
J.L.

<!-- table: missing headers/rows -->
> and

Finkel,
R.A.
1977.

- An

algorithm

for

finding
best
matches
in
logarithmic
expected
time.
ACM

<!-- table: missing headers/rows -->
> Transactions

on
Mathematical
Software,
3(3):209-226.
Funt,

- B.V.

and

Finlayson,

- G.D.

1995.

<!-- table: missing headers/rows -->
> Color

constant
color
indexing.

IEEE

Trans.

on

Pattern
Analysis

and

Machine
Intelligence,
17(5):522-529.
Grimson,

E.

1990.

Object

Recognition

by

Computer:

- The

Role

of

Geometric
Constraints,
The
MIT

<!-- table: missing headers/rows -->
> Press:

Cambridge,
MA.

<!-- table: missing headers/rows -->
> Harris,

C.

1992.

Geometry

from

visual
motion.

- In

Active

Vision,

- A.

Blake

and

- A.

Yuille

(Eds.),

MIT

<!-- table: missing headers/rows -->
> Press,

- pp.

263-284.

Harris,

C.
and

Stephens,

M.

1988.

A

combined

corner

and

edge
detector.

In
Fourth

Alvey
Vision
Conference,

Manchester,

UK,

- pp.

147-151.
Hartley,
R.

and
Zisserman,

- A.

2000.

Multiple

view

geomeltry
in

computer
vision,
Cambridge
University

Press:
Cambridge,

UK.

Hough,

P.V.C.

1962.

<!-- table: missing headers/rows -->
> Method

and

- means

for

recognizing
complex
patterns.
U.S.

Patent

3069654.
Koenderink,

J.J.

1984.
The

structure

of

images.
Biological
Cybernetics,

50:363-396.

Lindeberg,

T.
1993.

Detecting

salient

blob-like
image

structures

and

their
scales
with

a

scale-space
primal
sketch:

a

method

for

focus-of-attention.

International

Journal

of

Computer

Vision,
11(3):

283-318.
Lindeberg,

T.
1994.

Scale-space
theory:

A

basic

<!-- table: missing headers/rows -->
> tool

for

analysing
structures
at
different

scales.
Journal

of

Applied
Statistics,

21(2):224-270.

Lowe,

D.G.

- 1991.

Fitting
parameterized
three-dimensional
models
to

images.

IEEE
Trans.

on

Pattern

Analysis

- and

Machine
Intelligence,
13(5):441-450.

Pritchard,
D.,

and

Heidrich,

W.

2003.
Cloth
motion
capture.
Computer
Graphics
Forum
(Eurographics
2003),22(3):263-271.

<!-- table: missing headers/rows -->
> Schaffalitzky,

F.,
and

Zisserman,
A.
2002.

Multi-view

matching

for

unordered
image
sets,
or
do
T
organize
my

holiday
In

European
Conference

#### on

Computer
Vision,
Copenhagen,
Denmark,
pp.
414-431.

<!-- table: missing headers/rows -->
> Schiele,

B.,
and

Crowley,

<!-- table: missing headers/rows -->
> J.L.

2000.
Recognition
without
correspondence
using
multidimensional
receptive
field
histograms.
International

<!-- table: missing headers/rows -->
> Journal

of

Computer
Vision,
36(1):31-50.

<!-- table: missing headers/rows -->
> Schmid,

C.,
and

Mohr,

- R.

1997.

<!-- table: missing headers/rows -->
> Local

grayvalue

invariants

for

image
retrieval.

IEEE

Trans.

on

Pattern
Analysis

and

Machine
Intelligence,

19(5):530-534.

Se,

S.,

Lowe,

D.G.,
and

<!-- table: missing headers/rows -->
> Little,

- J.
- 2001.

Vision-based

mobile
robot

localization

and

mapping
using
scale-invariant
features.

- In

International
Conference

#### on

Robotics

and

Automation,
Seoul,
Korea,

Pp.

2051-58.

Se,

S.,

Lowe,

D.G.,
and

<!-- table: missing headers/rows -->
> Little,

- J.
- 2002.

Global

localization
using
distinctive
visual
features.

In

International

<!-- table: missing headers/rows -->
> Conference

on

Intelligent
Robots

and

Systems,

IROS
2002,

Lausanne,
Switzerland,
Pp.

226-231.

<!-- table: missing headers/rows -->
> Shokoufandeh,

- A.,

Marsic,

1.,
and

Dickinson,

S.J.
1999.

View-based

object

recognition
using
saliency
maps.

<!-- table: missing headers/rows -->
> Image

and

Vision

Computing,
17:445-460.
Torr,

P.

1995.

Motion
Segmentation

and

Outlier

Detection,

Ph.D.
Thesis,

Dept.

of

Engineering

Science,

University

of

Oxford,

UK.

Tuytelaars,

T.,
and

Van

Gool,
L.
2000.

Wide
baseline
stereo

<!-- table: missing headers/rows -->
> based

#### on

local,

affinely
invariant
regions.

In
British
Machine

<!-- table: missing headers/rows -->
> Vision

Conference,
Bristol,

UK,

- pp.

412-422.

Weber,

M.,
Welling,

- M.

and

Perona,

- P.

2000.

Unsupervised

learning

of

models

for

recognition.

In
European
Conference

on

Computer

Vision,

Dublin,

Ireland,

- pp.

18-32.
Witkin,

A.P.
1983.

Scale-space
filtering.
In
International
Joint

Conference

on

Intelligence,

Karlsruhe,

Germany,

- pp.

1019-1022.
Zhang,

Z.,

<!-- table: missing headers/rows -->
> Deriche,
<!-- table: missing headers/rows -->
> R.,

Faugeras,

<!-- table: missing headers/rows -->
> O.,
<!-- table: missing headers/rows -->
> and
<!-- table: missing headers/rows -->
> Luong,
<!-- table: missing headers/rows -->
> Q.T.

1995.
A
robust

technique