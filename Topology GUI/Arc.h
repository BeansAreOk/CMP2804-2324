#pragma once
#include "Node.h";

class Arc
{
public:
	Node* start;
	Node* end;
	double weight;
	Arc();
	Arc(Node* Start, Node* End, double Weight);
};