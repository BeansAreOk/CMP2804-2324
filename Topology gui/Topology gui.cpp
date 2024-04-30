#include <iostream>
#include <fstream>
#include <string>
//#include <yaml-cpp/yaml.h> 
#include "Node.h"
#include "Arc.h"

using namespace std;

//void writeYAML(const Node& node, const Arc& arc, const std::string& filename) {
//    YAML::Emitter emitter;
//    emitter << YAML::BeginMap;
//    emitter << YAML::Key << "Node";
//    emitter << YAML::Value << node.toYAML();
//    emitter << YAML::Key << "Arc";
//    emitter << YAML::Value << arc.toYAML();
//    emitter << YAML::EndMap;
//
//    std::ofstream fout(filename);
//    fout << emitter.c_str();
//}

int main()
{



    Node n1(0, 0, 0);
    Node n2(1, 1, 180);
    Arc a1(&n1, &n2, 1);

    cout << "Arc Start: (" << a1.start->x_coord << ", " << a1.start->y_coord << ")" << endl;
    cout << "Arc End: (" << a1.end->x_coord << ", " << a1.end->y_coord << ")" << endl;
    cout << "Arc Weight: " << a1.weight << endl;

    //writeYAML(n1, a1, "output.yaml");

    return 0;
}