#include "Arc.h"
#include <iostream>
#include <string>

using namespace std;
Arc::Arc()
{
	Node* start = new Node();
	Node* end = new Node();
	weight;
}

Arc::Arc(Node* _start, Node* _end, double _weight) : start(_start), end(_end), weight(_weight) {}



//YAML::Arc toYAML() const {
//    YAML::Node node;
//    node["start"] = start->toYAML();
//    node["end"] = end->toYAML();
//    node["weight"] = weight;
//    return node;
//}
