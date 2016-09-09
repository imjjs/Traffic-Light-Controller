#include "config.hpp"
#include "Intersection.hpp"
#include <stdbool.h>
#include <vector>
#include <cstdlib>
#include <thread>
#include <cassert>
#include <chrono>



using namespace std;

string jsonFile = "controllers_config.json";
vector<Intersection*> intersections;
map<string, Intersection*> ins_dict;
vector<string> selected_intersections {"Controller202407913", "Controller1443088096", "Controller202514078", "Controller3010263944", "Controller1443088101"};
map<string, vector<string>> phaseCodes {
{"Controller202407913",{"GGGggGGGGgrrrr", "yyyggyyyygrrrr", "rrrGGrrrrGrrrr", "rrryyrrrryrrrr", "rrrrrrrrrrGGGG", "rrrrrrrrrryyyy"}},
{"Controller1443088096",{"GGGGggrrGGGGggrrrr", "yyyyggrryyyyggrrrr", "rrrrGGrrrrrrGGrrrr", "rrrryyrrrrrryyrrrr", "GrrrrrGGrrrrrrGGgg", "yrrrrryyrrrrrryygg", "rrrrrrrrrrrrrrrrGG", "rrrrrrrrrrrrrrrryy"}},
{"Controller202514078",{"GGGGggrrrrGGGGggrrrr", "yyyyggrrrryyyyggrrrr", "rrrrGGrrrrrrrrGGrrrr", "rrrryyrrrrrrrryyrrrr", "rrrrrrGGggrrrrrrGGgg", "rrrrrryyggrrrrrryygg", "rrrrrrrrGGrrrrrrrrGG", "rrrrrrrryyrrrrrrrryy"}},
{"Controller3010263944",{"GGggrrrrrGGggrrrrr", "yyggrrrrryyggrrrrr", "rrGGrrrrrrrGGrrrrr", "rryyrrrrrrryyrrrrr", "rrrrGGGggrrrrGGGgg", "rrrryyyggrrrryyygg", "rrrrrrrGGrrrrrrrGG", "rrrrrrryyrrrrrrryy"}},
{"Controller1443088101",{"GGGggrrrrGGGggrrrr", "yyyggrrrryyyggrrrr", "rrrGGrrrrrrrGGrrrr", "rrryyrrrrrrryyrrrr", "rrrrrGGggrrrrrGGgg", "rrrrryyggrrrrryygg", "rrrrrrrGGrrrrrrrGG", "rrrrrrryyrrrrrrryy"}}
};
extern "C" {
void test_init(int dim, int args[])
{
	for(string name : selected_intersections){
		Intersection* ins = new Intersection(name);
		ins->loadFromJson(jsonFile);
		//ins->loadPhaseCode(phaseCodes);
		intersections.push_back(ins);
		ins_dict[name] = ins;
	}

	vector<vector<int>> paraList;
	for(int i = 0; i < dim; ++i)
	{
		vector<int> tmp;
		tmp.push_back(args[i]);
		i++;
		assert(i < dim);
		tmp.push_back(args[i]);
		paraList.push_back(tmp);
	}
	assert (paraList.size() == intersections.size());

	for(int i = 0; i < intersections.size(); ++i){
		intersections[i]->setThreshold(paraList[i][0], paraList[i][1]);
	}
}


void handleTrafficSensorInput( char* _trafficSensorID, int numVehiclesInQueue, char* _controllerID) {
	string trafficSensorID(_trafficSensorID);
	string controllerID(_controllerID);
    map<string, Intersection*>::iterator it = ins_dict.find(controllerID);
	ins_dict[controllerID]->updateQLength(trafficSensorID, numVehiclesInQueue);
}

int nextClockTick(char* _controllerID){
	string controllerID(_controllerID);
	ins_dict[controllerID]->run();
	return ins_dict[controllerID]->currentStateIdx;
}

// int getIdx(char* _controllerID){
// 	string controllerID(_controllerID);
// 	return ins_dict[controllerID]->currentStateIdx;
// }

void debug(){
	for(auto i : intersections){
		i->print();
	}
}
}
// void myexec(int args[], int dim){
// 	freopen("/dev/null", "w", stderr);
// 	system("sumo -c sumo/Vanderbilt.sumo.cfg --tripinfo-output tripinfo.xml --remote-port 1337&");
// 	::std::this_thread::sleep_for(chrono::seconds(10));
// 	singleton.create_connection(port, "127.0.0.1");

// 	vector<Intersection2*> intersections;
// 	for(string name : selected_intersections){
// 		Intersection2* ins = new Intersection2(name);
// 		ins->loadFromJson(jsonFile);
// 		ins->loadPhaseCode(phaseCodes);
// 		intersections.push_back(ins);
// 	}
// 		//cout<<"here";
// 	vector<vector<int>> paraList;
// 	for(int i = 0; i < dim; ++i)
// 	{
// 		vector<int> tmp;
// 		tmp.push_back(args[i]);
// 		i++;
// 		assert(i < dim);
// 		tmp.push_back(args[i]);
// 		paraList.push_back(tmp);
// 	}
// 	assert (paraList.size() == intersections.size());

// 	for(int i = 0; i < intersections.size(); ++i){
// 		intersections[i]->setThreshold(paraList[i][0], paraList[i][1]);
// 	}
 	
// 	for(int t = singleton.simulation.getMinExpectedNumber(); 
// 		t > 0; 
// 		t = singleton.simulation.getMinExpectedNumber()){
// 		singleton.commandSimulationStep(0);
// 		for(Intersection* ins: intersections)
// 			ins->run();
// 		//::std::this_thread::sleep_for(chrono::milliseconds(2));
// 	}
	
// 	singleton.close_connection();
 
// 	//TODO:: analysis the output xmlfile
// 	::std::this_thread::sleep_for(chrono::seconds(10));
// 	system("python parse_output.py tripinfo.xml");
// }


// int main(){
// 	Py_Initialize();
// 	PyObject *pName,*pModule,*pArgs,*pValue;
// 	pName = PyString_FromString("traci");
// 	pModule = PyImport_Import(pName);
// 	Py_DECREF(pName);
// 	assert (pModule != NULL);
// 	pAreal = PyObject_GetAttrString(pModule, "areal");
// 	int a[] = {0,5 };//,4,2,3,4,3,3,3,3};
// 	myexec(a, 2); 
// 	Py_Finalize();
// 	return 0;
// }
