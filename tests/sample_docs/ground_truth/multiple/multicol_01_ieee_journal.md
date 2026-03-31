IEEE

TRANSACTIONS
ON
NEURAL
NETWORKS

AND

LEARNING
SYSTEMS
Federated
Learning

Under

Heterogeneous
Data
Distributions:
A
Convergence
Analysis

and

Empirical
Study
Dr.

<!-- table: missing headers/rows -->
> Yin
<!-- table: missing headers/rows -->
> Zhang,

Prof.
Ahmed
Hassan,
Dr.
Sofia
Reyes,

and

Prof.
Lukas
Bauer
Department

of

Computer
Science,
Technical
University

#### of

Berlin,
Berlin,
Germany
Abstract—Federated
learning

(FL)

enables
collaborative

model

training
across
distributed

#### clients

without

sharing

raw
data,
making
it
attractive

for

privacy-sensitive
applications.
However,

statistical

heterogeneity

the
mismatch
between
local
data
distributions
across

<!-- table: missing headers/rows -->
> clients

significantly
degrades
convergence

<!-- table: missing headers/rows -->
> speed

and

final
model
accuracy.
We
present
FedProxAdam,
a
novel
FL
algorithm
combining
proximal
regularisation
with
adaptive
gradient
estimation.
Through
theoretical
analysis,

we

establish
convergence
guarantees
under
non11D
data

and

partial

client

<!-- table: missing headers/rows -->
> participation.

Experiments

on
CIFAR-10,
CIFAR-100,
and

Shakespeare

text

datasets
demonstrate

that
FedProxAdam

achieves
12-18%
accuracy
improvements
over
FedAvg
under

high
heterogencity,

while
reducing
communication
rounds

to

convergence

by

up

to

35%.

Code
is

available

at

hitps://github.com/example/fedproxadam.
Index

<!-- table: missing headers/rows -->
> Terms—

federated
learning,

non-1ID

- data,
- convergence
- analysis,

adaptive

optimisation.
1.

INTRODUCTION
Artificial

intelligence

has

fundamentally

reshaped
how

organisations
process

and

interpret

data

- at

scale.
Machine

learning
pipelines
now

underpin
everything
from
fraud

detection
in
financial
services

to

personalised

content
delivery

- across

digital
platforms.

Neural

architectures

- have

grown
increasingly

<!-- table: missing headers/rows -->
> sophisticated,

with

transformer-based

models

achieving

state-of-the-art

performance
across
natural
language,
vision,

and

multimodal
tasks.
The

attention

mechanism,
originally

- designed

for

sequence
transduction,

has

proven

remarkably

general.

<!-- table: missing headers/rows -->
> Edge

computing

complements

cloud

<!-- table: missing headers/rows -->
> infrastructure

by

processing

data
closer

to
its
source,
reducing
latency

for

time-critical

- applications.
- Autonomous

vehicles,
industrial

- ToT

sensors,

and

augmented
reality

<!-- table: missing headers/rows -->
> headsets

all

rely

- on
- real-time

inference
at
the

<!-- table: missing headers/rows -->
> edge.

Il.

RELATED
WORK

Quantum
processors
promise

exponential
speedups

for

- certain
- optimisation

and

simulation

problems.

While
fault-tolerant

quantum

- computing

remains

- years

away,

- near-term
- NISQ

#### devices

are
already
demonstrating

value

in

hybrid

- classical-quantum

workflows.
Cybersecurity

frameworks
must

evolve
continuously

- in

response

to

increasingly

- sophisticated

threat

<!-- table: missing headers/rows -->
> actors.

Zero-trust

architectures,

homomorphic

encryption,

and

Al-powered
anomaly

detection

represent
the

current

frontier

of

enterprise

defence
strategies.

0000-0000/25

2025
IEEE
Manuscript

received

January
2025

ALGORITHM
DESIGN
Recent
advances
in

CRISPR-Cas9

IEEE

TRANSACTIONS

ON

NEURAL
NETWORKS

AND

LEARNING
SYSTEMS
2
V.
EXPERIMENTAL
RESULTS
Central
bank
digital
currencies

are
being

<!-- table: missing headers/rows -->
> piloted

across
more
than
130
countries
as
monetary
authorities

seek

to

modernise
payment
infrastructure
while
maintaining
monetary
sovereignty
in

#### an

era

of

growing
private
digital
asset
adoption.
Supply
chain
resilience

has

become

#### a

board-level

priority
following

the

disruptions

of

the
pandemic
era.
Nearshoring,

dual

sourcing
strategies,

and

real-time
inventory
visibility
platforms

are
transforming

procurement
practices

- across

industries.

The

global
transition

to

renewable
energy
presents

- both

opportunity

and

dislocation.

While
solar

and

wind

<!-- table: missing headers/rows -->
> costs

- have

fallen

by

- more
- than

80

percent

over
the

- past

<!-- table: missing headers/rows -->
> decade,

the

retirement

of

fossil
fuel

<!-- table: missing headers/rows -->
> assets

and

workforce

retraining
represent
significant
economic
challenges.
Platform
economics

and

the

rise

of
two-sided

markets

- have

created
extraordinary

- concentrations

of

- market

power

- in

digital

industries.
Antitrust
regulators

on
both

#### sides

of
the

Atlantic

are

developing
new

frameworks

- adapted

to

the

dynamics

of

network

effects.

0000-0000/25

2025
IEEE

<!-- table: missing headers/rows -->
> Manuscript

received

January
2025;

act

VI.

DISCUSSION

Demographic
ageing
in
high-income
economies
is

placing

sustained
pressure
on
pension
systems,
healthcare
budgets,

and

labour
supply.
Immigration
policy,
retirement
age
reform,

and

productivity
growth

are
the

principal
levers
available
to
policymakers.

Financial

inclusion
initiatives

are

leveraging
mobile
money
platforms

to

extend
banking
services
to
the
1.4

billion

adults
globally

who

remain
unbanked.

M-PESA

in

Kenya,
UPI
in
India,

and

similar

systems
have
demonstrated
transformative
impacts
on

household

welfare.

The
labour

market
consequences

of

automation
remain
intensely

debated
among

economists.

While

routine
cognitive

and

manual

<!-- table: missing headers/rows -->
> tasks

are
increasingly

## performed

by

machines,
evidence
for
widespread

# net

job

destruction
remains
limited
in
historical
data.

ESG

investing

has

grown
from

a

niche

ethical
preference

to

a

mainstream

investment
criterion
managing
over
35

trillion

dollars

- in

assets.

The

challenge

of

standardising
sustainability
disclosures

#### and

preventing
greenwashing
remains
a

central
regulatory
priority.

- VII.

CONCLUSION
The

convergence

of
5G

connectivity,
miniaturised
sensors,

and

cloud-native

software
stacks

is
accelerating

digital
transformation

- across

healthcare,
logistics,
agriculture,

and

manufacturing

<!-- table: missing headers/rows -->
> sectors

worldwide.

<!-- table: missing headers/rows -->
> Sustainability

considerations

are

now
central

to

hardware
design

#### and

data

centre
operations.

Liquid

cooling,
renewable
energy

### procurement,

and

processor

## efficiency

improvements

are
reducing
the
carbon

intensity

of

computational
workloads.

REFERENCES
[1]
McMahan,

H.B.

et

#### al.

(2017).

Communication-efficient
learning.

- AISTATS.
- [2]

Li,

T.

et

#### al.

(2020).

Federated

optimization
in
heterogeneous
networks.

MLSys.

- [3]

Karimireddy,