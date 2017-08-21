package main

/*
A Segment handles the logic of local biophysics, or, in the simplest case,
such as an IAFNeuron, simulates the neuron AP curve itself.
*/
type Segment interface {
	GetMembranePotential() float64
	SetMembranePotential(float64)
	IncrementMembranePotential(float64) float64
}

/*
A SimpleSegment changes mV according to a prescribed function and does not
simulate ion channels.
*/
type SimpleSegment struct {
	membranePotential float64
}

/*
GetMembranePotential returns the membrane potential at a given region.
*/
func (segment *SimpleSegment) GetMembranePotential() float64 {
	return segment.membranePotential
}

/*
SetMembranePotential sets the membrane potential at this location.
*/
func (segment *SimpleSegment) SetMembranePotential(vm float64) {
	segment.membranePotential = vm
}

/*
IncrementMembranePotential increments the membrane potential at this location.
*/
func (segment *SimpleSegment) IncrementMembranePotential(vm float64) float64 {
	segment.SetMembranePotential(vm)
	return segment.GetMembranePotential()
}

/*
Neuron is the interface for a singular biological neuron.
Likely implemented by a point-model or a full biophysical model.
*/
type Neuron interface {
	// Simulates a single timestep of a neuron.
	Step()

	// Call all actions that rely on a neuron's firing of AP:
	Fire()

	GetSegments() []Segment
}

/*
A IAFNeuron runs a neuron according to the Integrate-And-Fire formulae.
This version is "leaky": https://en.wikipedia.org/wiki/Biological_neuron_model

The neuron contains only a single segment.
*/
type IAFNeuron struct {
	// The constituent segments:
	segments []Segment
}

/*
NewIAFNeuron constructs a new IAFNeuron.
*/
func NewIAFNeuron() *IAFNeuron {
	n := IAFNeuron{}
	return &n
}

/*
Step through a single timepoint.
*/
func (neuron *IAFNeuron) Step() {
	//
}

/*
Fire is the canonical Callback for an IAF to Fire.
*/
func (neuron *IAFNeuron) Fire() {
	// TODO: Read listeners and execute
}

/*
GetSegments returns the list of segments
*/
func (neuron *IAFNeuron) GetSegments() []Segment {
	return neuron.segments
}