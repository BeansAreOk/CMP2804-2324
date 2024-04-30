#include <iostream>
#include <fstream>
#include <string>
#include "Arc.h"
#include "Node.h"

using namespace std;
Node::Node()
{
	x_coord;
	y_coord;
	orientation;
}

Node::Node(double _x, double _y, double _orientation) : x_coord(_x), y_coord(_y), orientation(_orientation) {}

//YAML::Node toYAML() const {
//    YAML::Node node;
//    node["x_coord"] = x;
//    node["y_coord"] = y;
//    node["orientation"] = orientation;
//    return node;
//}